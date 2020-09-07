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
        # Extract policy parameters for the given year
        tau_c = self.pol.fetch('taxrt_ccorp', year)
        tau_sc = self.pol.fetch('taxrt_scorp', year)
        tau_sp = self.pol.fetch('taxrt_soleprop', year)
        tau_p = self.pol.fetch('taxrt_partner', year)
        phi_c = self.pol.fetch('intded_c', year)
        phi_nc = self.pol.fetch('intded_nc', year)
        drules = self.pol.read_ccr(year)
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
                
                # Compute costs of capital
                coc_ccorp[i,j] = calcCOC1(r_c, self.parm.pi, self.parm.rd,
                                          delta, Delta_c, tau_c, phi_c,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_c, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'])
                coc_scorp[i,j] = calcCOC1(r_nc, self.parm.pi, self.parm.rd,
                                          delta, Delta_nc, tau_sc, phi_nc,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_nc, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'])
                coc_soleprop[i,j] = calcCOC1(r_nc, self.parm.pi, self.parm.rd,
                                             delta, Delta_nc, tau_sp, phi_nc,
                                             drules.loc[ast, 'method'],
                                             drules.loc[ast, 'itcrt'],
                                             drules.loc[ast, 'itc_base'],
                                             drules.loc[ast, 'itc_life'],
                                             s179_nc, drules.loc[ast, 'bonus'],
                                             drules.loc[ast, 'life'],
                                             drules.loc[ast, 'acclrt'])
                coc_partner[i,j] = calcCOC1(r_nc, self.parm.pi, self.parm.rd,
                                            delta, Delta_nc, tau_p, phi_nc,
                                            drules.loc[ast, 'method'],
                                            drules.loc[ast, 'itcrt'],
                                            drules.loc[ast, 'itc_base'],
                                            drules.loc[ast, 'itc_life'],
                                            s179_nc, drules.loc[ast, 'bonus'],
                                            drules.loc[ast, 'life'],
                                            drules.loc[ast, 'acclrt'])
                # Compute METRs
                metr_ccorp[i,j] = (coc_ccorp[i,j] - r_c + self.parm.pi) / coc_ccorp[i,j]
                metr_scorp[i,j] = (coc_scorp[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_soleprop[i,j] = (coc_soleprop[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_partner[i,j] = (coc_partner[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
        print('Cost of capital calculations complete')
        results1 = {'corp': coc_ccorp, 'scorp': coc_scorp,
                    'soleprop': coc_soleprop, 'partner': coc_partner}
        self.results_coc[str(year)] = results1
        results2 = {'corp': metr_ccorp, 'scorp': metr_scorp,
                    'soleprop': metr_soleprop, 'partner': metr_partner}
        self.results_metr[str(year)] = results2
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
        ucoc_ccorp = np.zeros((ntype, nind))
        ucoc_scorp = np.zeros((ntype, nind))
        ucoc_soleprop = np.zeros((ntype, nind))
        ucoc_partner = np.zeros((ntype, nind))
        # Extract policy parameters for the given year
        (taulist_c, philist_c) = make_lists(self.pol.policies, 'ccorp', year, length=50)
        (taulist_sc, philist_nc) = make_lists(self.pol.policies, 'scorp', year, length=50)
        (taulist_sp, _) = make_lists(self.pol.policies, 'soleprop', year, length=50)
        (taulist_p, _) = make_lists(self.pol.policies, 'partner', year, length=50)
        drules = self.pol.read_ccr(year)
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
                
                # Compute costs of capital
                coc_ccorp[i,j] = calcCOC2(r_c, self.parm.pi, self.parm.rd,
                                          delta, Delta_c, taulist_c, philist_c,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_c, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'], 50)
                coc_scorp[i,j] = calcCOC2(r_nc, self.parm.pi, self.parm.rd,
                                          delta, Delta_nc, taulist_sc, philist_nc,
                                          drules.loc[ast, 'method'],
                                          drules.loc[ast, 'itcrt'],
                                          drules.loc[ast, 'itc_base'],
                                          drules.loc[ast, 'itc_life'],
                                          s179_nc, drules.loc[ast, 'bonus'],
                                          drules.loc[ast, 'life'],
                                          drules.loc[ast, 'acclrt'], 50)
                coc_soleprop[i,j] = calcCOC2(r_nc, self.parm.pi, self.parm.rd,
                                             delta, Delta_nc, taulist_sp, philist_nc,
                                             drules.loc[ast, 'method'],
                                             drules.loc[ast, 'itcrt'],
                                             drules.loc[ast, 'itc_base'],
                                             drules.loc[ast, 'itc_life'],
                                             s179_nc, drules.loc[ast, 'bonus'],
                                             drules.loc[ast, 'life'],
                                             drules.loc[ast, 'acclrt'], 50)
                coc_partner[i,j] = calcCOC2(r_nc, self.parm.pi, self.parm.rd,
                                            delta, Delta_nc, taulist_p, philist_nc,
                                            drules.loc[ast, 'method'],
                                            drules.loc[ast, 'itcrt'],
                                            drules.loc[ast, 'itc_base'],
                                            drules.loc[ast, 'itc_life'],
                                            s179_nc, drules.loc[ast, 'bonus'],
                                            drules.loc[ast, 'life'],
                                            drules.loc[ast, 'acclrt'], 50)
                # Compute METRs
                metr_ccorp[i,j] = (coc_ccorp[i,j] - r_c + self.parm.pi) / coc_ccorp[i,j]
                metr_scorp[i,j] = (coc_scorp[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_soleprop[i,j] = (coc_soleprop[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                metr_partner[i,j] = (coc_partner[i,j] - r_nc + self.parm.pi) / coc_ccorp[i,j]
                ucoc_ccorp[i,j] = coc_ccorp[i,j] + delta
                ucoc_scor[i,j] = coc_scorp[i,j] + delta
                ucoc_soleprop[i,j] = coc_soleprop[i,j] + delta
                ucoc_partner[i,j] = coc_partner[i,j] + delta
        print('Cost of capital calculations complete')
        results1 = {'corp': coc_ccorp, 'scorp': coc_scorp,
                    'soleprop': coc_soleprop, 'partner': coc_partner}
        self.results_coc[str(year)] = results1
        results2 = {'corp': metr_ccorp, 'scorp': metr_scorp,
                    'soleprop': metr_soleprop, 'partner': metr_partner}
        self.results_metr[str(year)] = results2
        results3 = {'corp': ucoc_ccorp, 'scorp': ucoc_scorp,
                    'soleprop': ucoc_soleprop, 'partner': ucoc_partner}
        self.results_ucoc[str(year)] = results3
        self.calc_all_called = True
