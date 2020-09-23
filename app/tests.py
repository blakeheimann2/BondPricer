import unittest
from app.Bond import Bond
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TestBond(unittest.TestCase):
    def testBPV(self):
        bond = Bond(price = 100, face_value=100, ytm=0.03, coupon_rate=0.03, coupon_freq=2, years=5)
        bond.calc_cashflows()
        bond.calc_macaulay_duration()
        bond.calc_modified_duration()
        bond.calc_convexity()
        bpv = np.round(bond.bpv(),5)
        new_price = bond.reprice(.005)
        self.assertEqual(new_price, 97.72)
        self.assertEqual(bpv, 0.04611)

    def testPlot(self):
        bond = Bond(price = 100, face_value=100, ytm=0.04, coupon_rate=0.05, coupon_freq=2, years=5)
        bond.calc_cashflows()
        bond.calc_macaulay_duration()
        bond.calc_modified_duration()
        bond.calc_convexity()
        bond_ps = []
        cf_ps = []
        ytm_chg = [-.005 + (.001 * i) for i in range(11)] + [-.05 + (0.01 * x) for x in range(11)]
        for chg in ytm_chg:
            new_price = bond.reprice(chg)
            bond_ps.append(new_price)
            new_ytm = .04 + chg
            newbond = Bond(price=100, face_value=100, ytm=new_ytm, coupon_rate=0.05, coupon_freq=2, years=5)
            newbond.calc_cashflows()
            price = newbond.get_total_PVcash_flow()
            cf_ps.append(price)
        results = pd.DataFrame(bond_ps, index=ytm_chg).sort_index()
        cf_results = pd.DataFrame(cf_ps, index=ytm_chg).sort_index()
        plt.plot(results, linestyle='--', marker='o', color='b', label="Duration & Convexity Price")
        plt.plot(cf_results, linestyle='--', marker='o', color='r', label= "NPV of Cash Flow Price")
        plt.annotate("BPV: {}".format(bond.bpv()), (0,results.loc[0.001]))
        plt.legend()
        plt.show()
        print(results)
        print(cf_results)
        bond.bpv()





