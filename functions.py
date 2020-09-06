import numpy as np
import pandas as pd


def calcD_db(r, L, n):
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

def calcD_sl(r, L):
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

def calcD_econ(r, pi, delta):
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

def calcITCpv(c, r, L):
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

def calcZ1(method, r, tau, itcrt, itcdb, itclife, s179, bonus, 
           pi=None, delta=None, life = None, accl = None,):
    """
    Calculate tax shield from capital cost recovery assuming constant tax
    rates.
    """
    # Compute PV of depreciation
    assert method in ['DB', 'SL', 'EXP', 'ECON']
    if method == 'DB':
        D = calcD_db(r, life, accl)
    elif method == 'SL':
        D = calcD_sl(r, life)
    elif method == 'ECON':
        D = calcD_econ(r, pi, delta)
    else:
        D = 1.0
    # Compute effective expensing share
    b = s179 + (1 - s179) * bonus
    # Compute CCR tax shield
    Z = tau * (1 - itcrt*itcdb) * (b + (1 - b) * D) + calcITCpv(itcrt, r, itclife)
    return Z

def calcF1(r, rd, pi, delta, Delta, tau, phi):
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

def calcCOC1(r, pi, rd, delta, Delta, tau, phi,
             method, itcrt, itcdb, itclife, s179, bonus, life, accl):
    """
    Calculate cost of capital assuming constant tax rates.
    """
    Z = calcZ1(method, r, tau, itcrt, itcdb, itclife, s179, bonus, pi, delta, life, accl)
    F = calcF1(r, rd, pi, delta, Delta, tau, phi)
    rho = (1 - Z - F) / (1 - tau) * (r - pi + delta) - delta
    return rho

