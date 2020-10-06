import numpy as np


def _calcD_db(r, L, n):
    """
    Calculate present value of depreciation deductions by declining balance
    method.
        r: Nominal discount rate
        L: Recovery period
        n: Declining balance rate
    """
    assert r > 0
    assert L >= 0
    assert n >= 1
    term1= n / (r * L + n) * (1 - np.exp(-(r * L + n) * (n - 1) / n))
    term2 = n / r / L * np.exp(1 - n - r * L) * (np.exp(r * L / n) - 1)
    D = term1 + term2
    return D

def _calcD_sl(r, L):
    """
    Calculate present value of depreciation deductions by straight-line
    method.
        r: Nominal discount rate
        L: Recovery period
    """
    assert r > 0
    assert L >= 0
    if L == 0:
        D = 1
    else:
        D = (1.0 - np.exp(-r * L)) / (r * L)
    return D

def _calcD_dbsl_per(r, L, n, a, b):
    """
    Calculates PV of depreciation deductions during [a,b] for declining
    balance and straight-line depreciation.
        n: exponential depreciation:
            2 for double-declining balance
            1.5 for 150% declining balance
            1 for straight-line
        L: tax life
        r: discount rate
    """
    # Ensure N is not an int
    n = n * 1.0
    # Switching point
    t1 = L * (1 - 1 / n)
    # End of tax life
    t2 = L
    if b <= t1:
        # If entirely subject to exponential depreciation
        D = (n / L / (r + n / L) * np.exp(-(r + n / L) * a) *
             (1 - np.exp(-(r + n / L) * (b - a))))
    elif b <= t2:
        if a < t1:
            # If period splits exponential and straight-line depreciation
            Ddb = (n / L / (r + n / L) *
                   np.exp(-(r + n / L) * a) *
                   (1 - np.exp(-(r + n / L) * (t1 - a))))
            if r == 0:
                # Special case of zero nominal discount rate
                Dsl = np.exp(1 - n) * (b - t1) / (t2 - t1)
            else:
                Dsl = (n / L / r * np.exp(1 - n) *
                       np.exp(-r * t1) *
                       (1 - np.exp(-r * (b - t1))))
            D = Ddb + Dsl
        else:
            # If entirely subject to straight-line depreciation
            if r == 0:
                D = np.exp(1 - n) * (b - a) / (t2 - t1)
            else:
                D = (n / L / r * np.exp(1 - n) *
                     np.exp(-r * a) *
                     (1 - np.exp(-r * (b - a))))
    else:
        # end of period occurs after tax life ends
        if a < t2:
            # If tax life ends during period
            if r == 0:
                D = np.exp(1 - n) * (t2 - a) / (t2 - t1)
            else:
                D = (n / L / r * np.exp(1 - n) *
                     np.exp(-r * a) *
                     (1 - np.exp(-r * (t2 - a))))
        else:
            # If period occurs entirely after tax life has ended
            D = 0
    return D

def _calcDlist_dbsl(r, L, n, exprt, length=50):
    """
    Calculates present value of depreciation deductions over lifetime
    for declining balance and straight-line depreciation.
        N: exponential depreciation:
            2 for double-declining balance
            1.5 for 150% declining balance
            1 for straight-line
        L: tax life
        r: discount rate
        exprt: effective expensing rate
        length: number of periods to use
    """
    Dlist = np.zeros(length)
    Dlist[0] = exprt + (1 - exprt) * _calcD_dbsl_per(r, L, n, 0, 0.5)
    for j in range(1, length):
        Dlist[j] = (1 - exprt) * _calcD_dbsl_per(r, L, n, j-0.5, j+0.5)
    return Dlist

def _calcD_econ(r, pi, delta):
    """
    Calculate present value of depreciation deductions by economic
    depreciation.
        r: Nominal discount rate
        pi: Inflation rate
        delta: Economic depreciation rate
    """
    assert r - pi > 0
    D = delta / (r - pi + delta)
    return D

def _calcD_econ_per(r, pi, delta, a, b):
    """
    Calculates PV of depreciation deduction during [a,b] using economic
    depreciation method.
        delta: depreciation rate
        r: discount rate
    """
    if r - pi + delta == 0:
        D = delta * (b - a)
    else:
        D = (delta / (r - pi + delta) * np.exp(-(r - pi + delta) * a) *
             (1 - np.exp(-(r - pi + delta) * (b - a))))
    return D

def _calcDlist_econ(r, pi, delta, exprt, length=50):
    """
    Calculates present value of depreciation deductions over lifetime
    for economic depreciation.
        delta: depreciation rate
        r: discount rate
        exprt: effective expensing rate
    """
    # Calculate for fist (half) year
    Dlist = np.zeros(length)
    Dlist[0] = exprt + (1 - exprt) * _calcD_econ_per(r, pi, delta, 0, 0.5)
    for j in range(1, length-1):
        Dlist[j] = (1 - exprt) * _calcD_econ_per(r, pi, delta, j-0.5, j+0.5)
    # Calculate from last period to infinity
    Dlist[length-1] = ((1 - exprt) *
                       _calcD_econ_per(r, pi, delta, length-1-0.5, 9e99))
    return Dlist

def _calcITCpv(c, r, L):
    """
    Calculate present value of investment tax credit.
        c: Statutory rate
        r: Nominal discount rate
        L: Period over which to amortize it
    """
    assert r > 0
    assert L >= 0
    if L == 0:
        pvc = c
    else:
        pvc = c / r / L * (1 - np.exp(-r * L))
    return pvc

def _calcZ1(method, r, tau, itcrt, itcdb, itclife, s179, bonus, 
            pi=None, delta=None, life = None, accl = None):
    """
    Calculate tax shield from capital cost recovery assuming constant tax
    rates.
    """
    # Compute PV of depreciation
    assert method in ['DB', 'SL', 'EXP', 'ECON']
    if method == 'DB':
        D = _calcD_db(r, life, accl)
    elif method == 'SL':
        D = _calcD_sl(r, life)
    elif method == 'ECON':
        D = _calcD_econ(r, pi, delta)
    else:
        D = 1.0
    # Compute effective expensing share
    b = s179 + (1 - s179) * bonus
    # Compute CCR tax shield
    Z = (tau * (1 - itcrt*itcdb) * (b + (1 - b) * D) +
         _calcITCpv(itcrt, r, itclife))
    return Z

def _calcD_list(method, r, pi, delta, life, accl, exprt, length=50):
    """
    Build array of present values of depreciation deductions taken in each
    period, using mid-year convention.
    """
    assert method in ['DB', 'SL', 'EXP', 'ECON']
    if method == 'DB':
        Dlist = _calcDlist_dbsl(r, life, accl, exprt, length)
    elif method == 'SL':
        Dlist = _calcDlist_dbsl(r, life, 1.0, exprt, length)
    elif method == 'ECON':
        Dlist = _calcDlist_econ(r, pi, delta, exprt, length)
    else:
        Dlist = np.zeros(length)
        Dlist[0] = 1.0
    return Dlist

def _calcZ2(method, r, taulist, itcrt, itcdb, itclife, s179, bonus, 
            pi=None, delta=None, life = None, accl=None, length=50):
    """
    Calculate tax shield from capital cost recovery assuming constant tax
    rates.
    """
    # Compute effective expensing rate (ignoring actual expensing)
    exprt = s179 + (1 - s179) * bonus
    # Produce Dlist
    Dlist = _calcD_list(method, r, pi, delta, life, accl, exprt, length)
    # Compute PV of tax shield from depreciation
    PVD = sum(taulist * Dlist)
    # Compute CCR tax shield
    Z = (1 - itcrt*itcdb) * PVD + _calcITCpv(itcrt, r, itclife)
    return Z

def _calcF1(r, rd, pi, delta, Delta, tau, phi):
    """
    Calculate tax shield from debt financing assuming constant tax rates.
        r: Nominal discount rate
        rd: Nominal interest rate on debt
        pi: Expected inflation rate
        delta: Depreciation rate
        Delta: Debt financing share
        tau: Tax rate
        phi: Fraction of interest deductible
    """
    F = Delta * rd * phi * tau / (r - pi + delta)
    return F

def _calcF_per(r, rd, pi, delta, Delta, a, b):
    """
    Calculates present value of interest accruing during period [a,b]
        Delta: ratio of debt to assets
        r: discount rate
        rd: interest rate on debt
        pi: inflation rate
        delta: depreciation rate
    """
    F = (Delta * rd / (r - pi + delta) * np.exp(-(r - pi + delta) * a) *
         (1 - np.exp(-(r - pi + delta) * (b - a))))
    return F

def _calcF2(r, rd, pi, delta, Delta, taulist, philist, length=50):
    """
    Calculates present value of interest deduction over lifetime
        Delta: ratio of debt to assets
        r: discount rate
        rd: interest rate on debt
        pi: inflation rate
        delta: depreciation rate
        taulist: array of tax rates per period
        philist: array of deductible shares of interest per period
        length: number of periods to use
    """
    assert len(taulist) == length
    assert len(philist) == length
    Flist = np.zeros(length)
    # Calcuate for first (half) year
    Flist[0] = _calcF_per(r, rd, pi, delta, Delta, 0, 0.5)
    for j in range(1, length-1):
        Flist[j] = _calcF_per(r, rd, pi, delta, Delta, j-0.5, j+0.5)
    # Calculate from final period to infinity
    Flist[length-1] = _calcF_per(r, rd, pi, delta, Delta, length-1-0.5, 9e99)
    F = sum(Flist * philist * taulist)
    return F

def _calcT(r, pi, delta, taulist):
    """
    Calculate weighted average tax rate over life of the asset.
        r: discount rate
        pi: inflation rate
        delta: depreciation rate
        taulist: array of tax rates per period
    """
    T = taulist[0] * (1 - np.exp(-(r - pi + delta) * 0.5))
    for j in range(1, len(taulist) - 1):
        T += taulist[j] * (np.exp(-(r - pi + delta) * (j - 0.5)) -
                           np.exp(-(r - pi + delta) * (j + 0.5)))
    T += (taulist[len(taulist) - 1] *
          np.exp(-(r - pi + delta) * (len(taulist) - 1.5)))
    return T

def calcCOC1(r, pi, rd, delta, Delta, tau, phi,
             method, itcrt, itcdb, itclife, s179, bonus, life, accl, tau_prop):
    """
    Calculate cost of capital assuming constant tax rates.
    """
    Z = _calcZ1(method, r, tau, itcrt, itcdb, itclife, s179, bonus, pi, delta,
                life, accl)
    F = _calcF1(r, rd, pi, delta, Delta, tau, phi)
    rho = (1 - Z - F) / (1 - tau) * (r - pi + delta) - delta + tau_prop
    return rho

def calcCOC2(r, pi, rd, delta, Delta, taulist, philist,
             method, itcrt, itcdb, itclife, s179, bonus, life, accl,
             taulist_prop, length = 50):
    """
    Calculate cost of capital allowing for tax rates that vary by year.
    """
    Z = _calcZ2(method, r, taulist, itcrt, itcdb, itclife, s179, bonus, pi,
                delta, life, accl, length)
    F = _calcF2(r, rd, pi, delta, Delta, taulist, philist, length)
    T = _calcT(r, pi, delta, taulist)
    Tp = _calcT(r, pi, delta, taulist_prop)
    rho = (1 - Z - F) / (1 - T) * (r - pi + delta) - delta + Tp
    return rho

def calcEATRd1(r, pi, rd, delta, Delta, tau, phi, exFDII, tang, p,
               method, itcrt, itcdb, itclife, s179, bonus, life, accl,
               tau_prop):
    """
    Calculate EATR on domestic investment with foreign sales,
    assuming constant tax rates.
        exFDII: FDII exclusion rate
        tang: indicator for asset tangibility
        p: Income rate (generally 20%, at least 10%)
    """
    assert tang in [0, 1]
    assert p > 0.1
    assert exFDII >= 0
    assert exFDII <= 1
    coc = calcCOC1(r, pi, rd, delta, Delta, tau, phi,
                   method, itcrt, itcdb, itclife, s179, bonus, life, accl,
                   tau_prop)
    eatr = ((coc - r + pi) / p + (p - coc) / p * tau -
            (p - 0.1*tang) / p * exFDII * tau)
    return eatr

def calcEATRd2(r, pi, rd, delta, Delta, taulist, philist, exFDII, tang, p,
               method, itcrt, itcdb, itclife, s179, bonus, life, accl,
               taulist_prop):
    """
    Calculate EATR on domestic investment with foreign sales,
    allowing for tax rates that vary by year.
        exFDII: FDII exclusion rate
        tang: indicator for asset tangibility
        p: Income rate (generally 20%, at least 10%)
    """
    assert tang in [0, 1]
    assert p > 0.1
    assert exFDII >= 0
    assert exFDII <= 1
    coc = calcCOC2(r, pi, rd, delta, Delta, taulist, philist,
                   method, itcrt, itcdb, itclife, s179, bonus, life, accl,
                   taulist_prop)
    T = _calcT(r, pi, delta, taulist)
    eatr = ((coc - r + pi) / p + (p - coc) / p * T -
            (p - 0.1*tang) / p * exFDII * T)
    return eatr

def calcEATRf1(r, pi, rd, delta, Delta, tau, exGILTI, tang, p, tauf,
               method, itcrt, itcdb, itclife, s179, bonus, life, accl,
               tau_prop):
    """
    Calculate EATR on domestic investment with foreign sales,
    assuming constant tax rates.
        exGILTI: FDII exclusion rate
        tang: indicator for asset tangibility
        p: Income rate (generally 20%, at least 10%)
        tauf: foreign tax rate
    """
    assert tang in [0, 1]
    assert p > 0.1
    assert exGILTI >= 0
    assert exGILTI <= 1
    coc = calcCOC1(r, pi, rd, delta, Delta, tauf, 1.0,
                   method, itcrt, itcdb, itclife, s179, bonus, life, accl, 0.0)
    eatr = ((coc - r + pi) / p + (p - coc) / p * tauf +
            (p - 0.1*tang) / p * max(tau * (1.0 - exGILTI) - 0.8*tauf, 0))
    return eatr

def calcEATRf2(r, pi, rd, delta, Delta, taulist, exGILTI, tang, p, tauf,
               method, itcrt, itcdb, itclife, s179, bonus, life, accl,
               taulist_prop):
    """
    Calculate EATR on domestic investment with foreign sales,
    assuming constant tax rates.
        exGILTI: FDII exclusion rate
        tang: indicator for asset tangibility
        p: Income rate (generally 20%, at least 10%)
        tauf: foreign tax rate
    """
    assert tang in [0, 1]
    assert p > 0.1
    assert exGILTI >= 0
    assert exGILTI <= 1
    coc = calcCOC1(r, pi, rd, delta, Delta, tauf, 1.0,
                   method, itcrt, itcdb, itclife, s179, bonus, life, accl, 0.0)
    T = _calcT(r, pi, delta, taulist)
    eatr = ((coc - r + pi) / p + (p - coc) / p * tauf +
            (p - 0.1*tang) / p * max(T * (1.0 - exGILTI) - 0.8*tauf, 0))
    return eatr

def make_lists(poldf, ptype, syear, length):
    """
    Make arrays of given length of tax rates or deductible interest shares.
        policies: regular policy DataFrame
        ptype: Policy parameter to convert into forward-looking list
        syear: year to begin array
    """
    assert ptype in ['taxrt_ccorp', 'taxrt_scorp', 'taxrt_soleprop',
                     'taxrt_partner', 'sub_slti', 'intded_c', 'intded_nc']
    assert syear >= 2020
    assert type(length) is int
    assert length >= 1
    pollist = np.zeros(length)
    for year in range(syear, syear + length):
        pollist[year-syear] = poldf.loc[min(year, 2029), ptype]
    return pollist

def calcSc(rd, re, pi, Delta, shares, tau_int, tau_div, tau_scg, tau_lcg,
           stepup):
    """
    Calculate return to saving through corporations.
        rd: Rate of return on debt (nominal)
        re: Rate of return on equity (nominal)
        pi: Inflation rate
        shares: Dict() of holding shares (from Parameter class)
        tau_int: Tax rate on interest income
        tau_div: Tax rate on dividend income
        tau_scg: Tax rate on short-term capital gains
        tau_lcg: Tax rate on long-term capital gains
        stepup: Indicator for whether step-up basis is used.
    """
    # After-tax return to lenders
    sd = (shares['txshr_d_c'] * rd * (1 - tau_int) +
          (1 - shares['txshr_d_c']) * rd - pi)
    # After-tax return through capital gains
    if stepup == 1:
        tau_xcg = 0.
    else:
        tau_xcg = tau_lcg
    hl = shares['h_lcg']
    hx = shares['h_xcg']
    m = shares['divshr']
    s_scg = re * (1 - tau_scg)
    s_lcg = (1.0 / (hl * (1 - m)) *
             np.log(np.exp(hl * (1 - m) * re) * (1 - tau_lcg) + tau_lcg))
    s_xcg = (1.0 / (hx * (1 - m)) *
             np.log(np.exp(hx * (1 - m) * re) * (1 - tau_xcg) + tau_xcg))
    s_cg = (shares['wt_scg'] * s_scg + shares['wt_lcg'] * s_lcg +
            (1 - shares['wt_scg'] - shares['wt_lcg']) * s_xcg - pi)
    # After-tax return through equity
    se = (shares['txshr_e'] * (m * re * (1 - tau_div) +
          (1 - m) * (s_cg + pi)) + (1 - shares['txshr_e']) * re - pi)
    s = Delta * sd + (1 - Delta) * se
    return s

def calcSnc(rd, re, pi, Delta, shares, tau_int):
    """
    Calculate return to saving through corporations.
        rd: Rate of return on debt (nominal)
        re: Rate of return on equity (nominal)
        pi: Inflation rate
        shares: Dict() of holding shares (from Parameter class)
        tau_int: Tax rate on interest income
    """
    # After-tax return to lenders
    sd = (shares['txshr_d_nc'] * rd * (1 - tau_int) +
          (1 - shares['txshr_d_nc']) * rd - pi)
    se = re - pi
    s = Delta * sd + (1 - Delta) * se
    return s

