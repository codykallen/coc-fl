import copy
import numpy as np
import pandas as pd
from policy import Policy
from parameter import Parameter
from config import *
from functions import *

class Calculator():
    """
    Calculator class.

    Computes and stores results.
    """

    def __init__(self, parm, pol):
        """
            parm: Parameter class object
            pol: Policy class object
        """
        # Store affiliated objects
        self.parm = copy.deepcopy(parm)
        self.pol = copy.deepcopy(pol)
        self.calc_all_called = False
        self.results_coc = dict()
        self.results_metr = dict()
        self.results_ucoc = dict()
        self.results_international = dict()
        self.results_mettr = dict()
    
    def calc_all(self, year):
        """
        Checks what type of equations to use, and calls the relevant
        calc_all_* function.
        """
        if self.parm.forwardLooking:
            self.calc_all_forward(year)
        else:
            self.calc_all_basic(year)
    
    def calc_all_basic(self, year):
        """
        Calculate cost of capital by asset type, industry and firm type.
        Takes naive view that present tax rates persist indefinitely.
        """
        assert year >= 2020
        # Create empty arrays for results
        coc_ccorp = np.zeros((ntype, nind))
        coc_scorp = np.zeros((ntype, nind))
        coc_soleprop = np.zeros((ntype, nind))
        coc_partner = np.zeros((ntype, nind))
        metr_ccorp = np.zeros((ntype, nind))
        metr_scorp = np.zeros((ntype, nind))
        metr_soleprop = np.zeros((ntype, nind))
        metr_partner = np.zeros((ntype, nind))
        mettr_ccorp = np.zeros((ntype, nind))
        mettr_scorp = np.zeros((ntype, nind))
        mettr_soleprop = np.zeros((ntype, nind))
        mettr_partner = np.zeros((ntype, nind))
        ucoc_ccorp = np.zeros((ntype, nind))
        ucoc_scorp = np.zeros((ntype, nind))
        ucoc_soleprop = np.zeros((ntype, nind))
        ucoc_partner = np.zeros((ntype, nind))
        eatr_dom = np.zeros((ntype, nind))
        eatr_for = np.zeros((ntype, nind))
        # Extract policy parameters for the given year
        tau_c = self.pol.fetch('taxrt_ccorp', year)
        tau_sc = self.pol.fetch('taxrt_scorp', year)
        tau_sp = self.pol.fetch('taxrt_soleprop', year)
        tau_p = self.pol.fetch('taxrt_partner', year)
        phi_c = self.pol.fetch('intded_c', year)
        phi_nc = self.pol.fetch('intded_nc', year)
        drules = self.pol.read_ccr(year)
        drulesf = self.pol.read_ccr('foreign')
        FDIIrt = self.pol.fetch('fdii_ex', year)
        GILTIrt = self.pol.fetch('gilti_ex', year)
        # Potentially include state and local taxes
        if self.parm.include_slt:
            sub_slti = self.pol.fetch('sub_slti', year)
            sub_sltp = self.pol.fetch('sub_sltp', year)
            tau_c += self.parm.sltaxes['corp'] * (1 - tau_c)
            tau_sc += self.parm.sltaxes['soleprop'] * (1 - sub_slti)
            tau_sp += self.parm.sltaxes['partner'] * (1 - sub_slti)
            tau_p += self.parm.sltaxes['partner'] * (1 - sub_slti)
            tau_prop_c = self.parm.sltaxes['property'] * (1 - tau_c)
            tau_prop_sc = self.parm.sltaxes['property'] * (1 - tau_sc)
            tau_prop_sp = self.parm.sltaxes['property'] * (1 - tau_sp)
            tau_prop_p = self.parm.sltaxes['property'] * (1 - tau_p)
        else:
            tau_prop_c = 0.0
            tau_prop_nc = 0.0
        # Run calculations
        for i in range(ntype):
            ast = ast_codes[i]
            for j in range(nind):
                ind = ind_codes[j]
                # Extract relevant parameters
                Delta_c = self.parm.Deltas.loc[ind, 'corp']
                Delta_nc = self.parm.Deltas.loc[ind, 'noncorp']
                r_c = self.parm.rd * Delta_c + self.parm.re * (1 - Delta_c)
                r_nc = self.parm.rd * Delta_nc + self.parm.re * (1 - Delta_nc)
                delta = self.parm.deltas.loc[ast, 'delta']
                s179_c = self.parm.s179.loc[ast, 'corp']
                s179_nc = self.parm.s179.loc[ast, 'noncorp']
                tauf = self.parm.foreign.loc[ind, 'tauf']
                # Only use property tax for tangibles
                if ast[0:2] in ['EN', 'RD', 'AE']:
                    tau_prop_c2 = 0.0
                    tau_prop_sc2 = 0.0
                    tau_prop_sp2 = 0.0
                    tau_prop_p2 = 0.0
                else:
                    tau_prop_c2 = copy.deepcopy(tau_prop_c)
                    tau_prop_sc2 = copy.deepcopy(tau_prop_sc)
                    tau_prop_sp2= copy.deepcopy(tau_prop_sp)
                    tau_prop_p2 = copy.deepcopy(tau_prop_p)
                # Compute costs of capital
                coc_ccorp[i,j] = calcCOC1(r_c, self.parm.pi, self.parm.rd,
                                          delta, Delta_c, tau_c, phi_c,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_c, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'], tau_prop_c2)
                coc_scorp[i,j] = calcCOC1(r_nc, self.parm.pi, self.parm.rd,
                                          delta, Delta_nc, tau_sc, phi_nc,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_nc, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'], tau_prop_sc2)
                coc_soleprop[i,j] = calcCOC1(r_nc, self.parm.pi, self.parm.rd,
                                             delta, Delta_nc, tau_sp, phi_nc,
                                             drules.loc[ast, 'method'],
                                             drules.loc[ast, 'itcrt'],
                                             drules.loc[ast, 'itc_base'],
                                             drules.loc[ast, 'itc_life'],
                                             s179_nc, drules.loc[ast, 'bonus'],
                                             drules.loc[ast, 'life'],
                                             drules.loc[ast, 'acclrt'], tau_prop_sp2)
                coc_partner[i,j] = calcCOC1(r_nc, self.parm.pi, self.parm.rd,
                                            delta, Delta_nc, tau_p, phi_nc,
                                            drules.loc[ast, 'method'],
                                            drules.loc[ast, 'itcrt'],
                                            drules.loc[ast, 'itc_base'],
                                            drules.loc[ast, 'itc_life'],
                                            s179_nc, drules.loc[ast, 'bonus'],
                                            drules.loc[ast, 'life'],
                                            drules.loc[ast, 'acclrt'], tau_prop_p2)
                # Compute METRs
                metr_ccorp[i,j] = (coc_ccorp[i,j] - r_c + self.parm.pi) / coc_ccorp[i,j]
                metr_scorp[i,j] = (coc_scorp[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_soleprop[i,j] = (coc_soleprop[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_partner[i,j] = (coc_partner[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                # Compute user cost of capital
                ucoc_ccorp[i,j] = coc_ccorp[i,j] + delta
                ucoc_scorp[i,j] = coc_scorp[i,j] + delta
                ucoc_soleprop[i,j] = coc_soleprop[i,j] + delta
                ucoc_partner[i,j] = coc_partner[i,j] + delta
                # Compute returns to savers
                taxrt_int = self.pol.fetch('taxrt_int', year)
                taxrt_div = self.pol.fetch('taxrt_div', year)
                taxrt_scg = self.pol.fetch('taxrt_scg', year)
                taxrt_lcg = self.pol.fetch('taxrt_lcg', year)
                if self.parm.include_slt:
                    # Include state and local taxes
                    subi = self.pol.fetch('sub_slti', year)
                    taxrt_int += self.parm.sltaxes['int'] * (1 - subi)
                    taxrt_div += self.parm.sltaxes['qdiv'] * (1 - subi)
                    taxrt_scg += self.parm.sltaxes['scg'] * (1 - subi)
                    taxrt_lcg += self.parm.sltaxes['lcg'] * (1 - subi)
                s_c = calcSc(self.parm.rd, self.parm.re, self.parm.pi, Delta_c,
                             self.parm.shares, taxrt_int, taxrt_div, taxrt_scg,
                             taxrt_lcg, self.pol.fetch('stepup', year))
                s_nc = calcSnc(self.parm.rd, self.parm.re, self.parm.pi, Delta_nc,
                               self.parm.shares, taxrt_int)
                # Compute METTRs
                mettr_ccorp[i,j] = (coc_ccorp[i,j] - s_c) / coc_ccorp[i,j]
                mettr_scorp[i,j] = (coc_scorp[i,j] - s_nc) / coc_scorp[i,j]
                mettr_soleprop[i,j] = (coc_soleprop[i,j] - s_nc) / coc_soleprop[i,j]
                mettr_partner[i,j] = (coc_partner[i,j] - s_nc) / coc_partner[i,j]
                # Compute EATRs
                if ast[0:2] in ['EN', 'RD', 'AE']:
                    tang = 0
                else:
                    tang = 1
                eatr_dom[i,j] = calcEATRd1(r_c, self.parm.pi, self.parm.rd,
                                           delta, Delta_c, tau_c, phi_c,
                                           FDIIrt, tang, self.parm.p,
                                           drulesf.loc[ast, 'method'],
                                           drulesf.loc[ast, 'itcrt'],
                                           drulesf.loc[ast, 'itc_base'],
                                           drulesf.loc[ast, 'itc_life'],
                                           0.0, drules.loc[ast, 'bonus'],
                                           drulesf.loc[ast, 'life'],
                                           drulesf.loc[ast, 'acclrt'], tau_prop_c2)
                eatr_for[i,j ] = calcEATRf1(r_c, self.parm.pi, self.parm.rd,
                                           delta, Delta_c, tau_c,
                                           GILTIrt, tang, self.parm.p, tauf,
                                           drulesf.loc[ast, 'method'],
                                           drulesf.loc[ast, 'itcrt'],
                                           drulesf.loc[ast, 'itc_base'],
                                           drulesf.loc[ast, 'itc_life'],
                                           0.0, drules.loc[ast, 'bonus'],
                                           drulesf.loc[ast, 'life'],
                                           drulesf.loc[ast, 'acclrt'], tau_prop_c2)
        print('Calculations complete for ' + str(year))
        results1 = {'corp': coc_ccorp, 'scorp': coc_scorp,
                    'soleprop': coc_soleprop, 'partner': coc_partner}
        self.results_coc[str(year)] = results1
        results2 = {'corp': metr_ccorp, 'scorp': metr_scorp,
                    'soleprop': metr_soleprop, 'partner': metr_partner}
        self.results_metr[str(year)] = results2
        results3 = {'corp': ucoc_ccorp, 'scorp': ucoc_scorp,
                    'soleprop': ucoc_soleprop, 'partner': ucoc_partner}
        self.results_ucoc[str(year)] = results3
        results4 = {'domestic': eatr_dom, 'foreign': eatr_for}
        self.results_international[str(year)] = results4
        results5 = {'corp': mettr_ccorp, 'scorp': mettr_scorp,
                    'soleprop': mettr_soleprop, 'partner': mettr_partner}
        self.results_mettr[str(year)] = results5
        self.calc_all_called = True
        
    def calc_all_forward(self, year):
        """
        Calculate cost of capital by asset type, industry and firm type.
        Uses forward-looking equations for future tax policies.
        """
        assert year >= 2020
        # Create empty arrays for results
        coc_ccorp = np.zeros((ntype, nind))
        coc_scorp = np.zeros((ntype, nind))
        coc_soleprop = np.zeros((ntype, nind))
        coc_partner = np.zeros((ntype, nind))
        metr_ccorp = np.zeros((ntype, nind))
        metr_scorp = np.zeros((ntype, nind))
        metr_soleprop = np.zeros((ntype, nind))
        metr_partner = np.zeros((ntype, nind))
        mettr_ccorp = np.zeros((ntype, nind))
        mettr_scorp = np.zeros((ntype, nind))
        mettr_soleprop = np.zeros((ntype, nind))
        mettr_partner = np.zeros((ntype, nind))
        ucoc_ccorp = np.zeros((ntype, nind))
        ucoc_scorp = np.zeros((ntype, nind))
        ucoc_soleprop = np.zeros((ntype, nind))
        ucoc_partner = np.zeros((ntype, nind))
        eatr_dom = np.zeros((ntype, nind))
        eatr_for = np.zeros((ntype, nind))
        # Extract policy parameters for the given year
        (taulist_c, philist_c) = make_lists(self.pol.policies, 'ccorp', year, length=50)
        (taulist_sc, philist_nc) = make_lists(self.pol.policies, 'scorp', year, length=50)
        (taulist_sp, _) = make_lists(self.pol.policies, 'soleprop', year, length=50)
        (taulist_p, _) = make_lists(self.pol.policies, 'partner', year, length=50)
        (sublist_i, _) = make_lists(self.pol.policies, 'slti', year, length=50)
        (sublist_p, _) = make_lists(self.pol.policies, 'sltp', year, length=50)
        drules = self.pol.read_ccr(year)
        drulesf = self.pol.read_ccr('foreign')
        FDIIrt = self.pol.fetch('fdii_ex', year)
        GILTIrt = self.pol.fetch('gilti_ex', year)
        # Potentially include state and local taxes
        if self.parm.include_slt:
            taulist_c += self.parm.sltaxes['corp'] * (1 - taulist_c)
            taulist_sc += self.parm.sltaxes['soleprop'] * (1 - sublist_i)
            taulist_sp += self.parm.sltaxes['partner'] * (1 - sublist_i)
            taulist_p += self.parm.sltaxes['partner'] * (1 - sublist_i)
            taulist_prop_c = self.parm.sltaxes['property'] * (1 - taulist_c)
            taulist_prop_sc = self.parm.sltaxes['property'] * (1 - taulist_sc)
            taulist_prop_sp = self.parm.sltaxes['property'] * (1 - taulist_sp)
            taulist_prop_p = self.parm.sltaxes['property'] * (1 - taulist_p)
        else:
            taulist_prop_c = np.zeros(len(taulist_c))
            taulist_prop_sc = np.zeros(len(taulist_sc))
            taulist_prop_sp = np.zeros(len(taulist_sp))
            taulist_prop_p = np.zeros(len(taulist_p))
        # Run calculations
        for i in range(ntype):
            ast = ast_codes[i]
            for j in range(nind):
                ind = ind_codes[j]
                # Extract relevant parameters
                Delta_c = self.parm.Deltas.loc[ind, 'corp']
                Delta_nc = self.parm.Deltas.loc[ind, 'noncorp']
                r_c = self.parm.rd * Delta_c + self.parm.re * (1 - Delta_c)
                r_nc = self.parm.rd * Delta_nc + self.parm.re * (1 - Delta_nc)
                delta = self.parm.deltas.loc[ast, 'delta']
                s179_c = self.parm.s179.loc[ast, 'corp']
                s179_nc = self.parm.s179.loc[ast, 'noncorp']
                tauf = self.parm.foreign.loc[ind, 'tauf']
                # Only use property tax for tangibles
                if ast[0:2] in ['EN', 'RD', 'AE']:
                    taulist_prop_c2 = np.zeros(len(taulist_prop_c))
                    taulist_prop_sc2 = np.zeros(len(taulist_prop_sc))
                    taulist_prop_sp2 = np.zeros(len(taulist_prop_sp))
                    taulist_prop_p2 = np.zeros(len(taulist_prop_p))
                else:
                    taulist_prop_c2 = copy.deepcopy(taulist_prop_c)
                    taulist_prop_sc2 = copy.deepcopy(taulist_prop_sc)
                    taulist_prop_sp2 = copy.deepcopy(taulist_prop_sp)
                    taulist_prop_p2 = copy.deepcopy(taulist_prop_p)
                # Compute costs of capital
                coc_ccorp[i,j] = calcCOC2(r_c, self.parm.pi, self.parm.rd,
                                          delta, Delta_c, taulist_c, philist_c,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_c, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'], taulist_prop_c2, 50)
                coc_scorp[i,j] = calcCOC2(r_nc, self.parm.pi, self.parm.rd,
                                          delta, Delta_nc, taulist_sc, philist_nc,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_nc, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'], taulist_prop_sc2, 50)
                coc_soleprop[i,j] = calcCOC2(r_nc, self.parm.pi, self.parm.rd,
                                             delta, Delta_nc, taulist_sp, philist_nc,
                                             drules.loc[ast, 'method'],
                                             drules.loc[ast, 'itcrt'],
                                             drules.loc[ast, 'itc_base'],
                                             drules.loc[ast, 'itc_life'],
                                             s179_nc, drules.loc[ast, 'bonus'],
                                             drules.loc[ast, 'life'],
                                             drules.loc[ast, 'acclrt'], taulist_prop_sp2, 50)
                coc_partner[i,j] = calcCOC2(r_nc, self.parm.pi, self.parm.rd,
                                            delta, Delta_nc, taulist_p, philist_nc,
                                            drules.loc[ast, 'method'],
                                            drules.loc[ast, 'itcrt'],
                                            drules.loc[ast, 'itc_base'],
                                            drules.loc[ast, 'itc_life'],
                                            s179_nc, drules.loc[ast, 'bonus'],
                                            drules.loc[ast, 'life'],
                                            drules.loc[ast, 'acclrt'], taulist_prop_p2, 50)
                # Compute METRs
                metr_ccorp[i,j] = (coc_ccorp[i,j] - r_c + self.parm.pi) / coc_ccorp[i,j]
                metr_scorp[i,j] = (coc_scorp[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_soleprop[i,j] = (coc_soleprop[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_partner[i,j] = (coc_partner[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                # Compute user cost of capital
                ucoc_ccorp[i,j] = coc_ccorp[i,j] + delta
                ucoc_scorp[i,j] = coc_scorp[i,j] + delta
                ucoc_soleprop[i,j] = coc_soleprop[i,j] + delta
                ucoc_partner[i,j] = coc_partner[i,j] + delta
                # Compute returns to savers
                taxrt_int = self.pol.fetch('taxrt_int', year)
                taxrt_div = self.pol.fetch('taxrt_div', year)
                taxrt_scg = self.pol.fetch('taxrt_scg', year)
                taxrt_lcg = self.pol.fetch('taxrt_lcg', year)
                if self.parm.include_slt:
                    # Include state and local taxes
                    subi = self.pol.fetch('sub_slti', year)
                    taxrt_int += self.parm.sltaxes['int'] * (1 - subi)
                    taxrt_div += self.parm.sltaxes['qdiv'] * (1 - subi)
                    taxrt_scg += self.parm.sltaxes['scg'] * (1 - subi)
                    taxrt_lcg += self.parm.sltaxes['lcg'] * (1 - subi)
                s_c = calcSc(self.parm.rd, self.parm.re, self.parm.pi, Delta_c,
                             self.parm.shares, taxrt_int, taxrt_div, taxrt_scg,
                             taxrt_lcg, self.pol.fetch('stepup', year))
                s_nc = calcSnc(self.parm.rd, self.parm.re, self.parm.pi, Delta_nc,
                               self.parm.shares, taxrt_int)
                # Compute METTRs
                mettr_ccorp[i,j] = (coc_ccorp[i,j] - s_c) / coc_ccorp[i,j]
                mettr_scorp[i,j] = (coc_scorp[i,j] - s_nc) / coc_scorp[i,j]
                mettr_soleprop[i,j] = (coc_soleprop[i,j] - s_nc) / coc_soleprop[i,j]
                mettr_partner[i,j] = (coc_partner[i,j] - s_nc) / coc_partner[i,j]
                # Compute EATRs
                if ast[0:2] in ['EN', 'RD', 'AE']:
                    tang = 0
                else:
                    tang = 1
                eatr_dom[i,j] = calcEATRd2(r_c, self.parm.pi, self.parm.rd,
                                           delta, Delta_c, taulist_c, philist_c,
                                           FDIIrt, tang, self.parm.p,
                                           drulesf.loc[ast, 'method'],
                                           drulesf.loc[ast, 'itcrt'],
                                           drulesf.loc[ast, 'itc_base'],
                                           drulesf.loc[ast, 'itc_life'],
                                           0.0, drules.loc[ast, 'bonus'],
                                           drulesf.loc[ast, 'life'],
                                           drulesf.loc[ast, 'acclrt'], taulist_prop_c2)
                eatr_for[i,j ] = calcEATRf2(r_c, self.parm.pi, self.parm.rd,
                                           delta, Delta_c, taulist_c,
                                           GILTIrt, tang, self.parm.p, tauf,
                                           drulesf.loc[ast, 'method'],
                                           drulesf.loc[ast, 'itcrt'],
                                           drulesf.loc[ast, 'itc_base'],
                                           drulesf.loc[ast, 'itc_life'],
                                           0.0, drules.loc[ast, 'bonus'],
                                           drulesf.loc[ast, 'life'],
                                           drulesf.loc[ast, 'acclrt'], taulist_prop_c2)
        print('Calculations complete for ' + str(year))
        results1 = {'corp': coc_ccorp, 'scorp': coc_scorp,
                    'soleprop': coc_soleprop, 'partner': coc_partner}
        self.results_coc[str(year)] = results1
        results2 = {'corp': metr_ccorp, 'scorp': metr_scorp,
                    'soleprop': metr_soleprop, 'partner': metr_partner}
        self.results_metr[str(year)] = results2
        results3 = {'corp': ucoc_ccorp, 'scorp': ucoc_scorp,
                    'soleprop': ucoc_soleprop, 'partner': ucoc_partner}
        self.results_ucoc[str(year)] = results3
        results4 = {'domestic': eatr_dom, 'foreign': eatr_for}
        self.results_international[str(year)] = results4
        results5 = {'corp': mettr_ccorp, 'scorp': mettr_scorp,
                    'soleprop': mettr_soleprop, 'partner': mettr_partner}
        self.results_mettr[str(year)] = results5
        self.calc_all_called = True
