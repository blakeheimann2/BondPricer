import pandas as pd
import warnings
import numpy as np

class Bond(object):
    def __init__(self, price, face_value, ytm, coupon_rate, coupon_freq, years):
        self._price = price
        self._face_value = face_value
        self._ytm = ytm
        self._coupon_rate = coupon_rate
        self._coupon_freq = coupon_freq
        self._lifetime = years
        self._periods = int(self._lifetime * self._coupon_freq) + 1 #for period zero
        self._coupon_amt = self._face_value * self._coupon_rate / self._coupon_freq
        self.convexity = None
        self.duration = None
        self.modified_duration = None
        self.cash_flow = None

    def get_lifetime(self):
        return self._lifetime

    def set_YTM(self, yield_to_maturity):
        warnings.warn("Resetting Yield to Maturity Requires Recalculating Cash Flows, Durations, and Convexity. It is best to instantiate a new Bond.", UserWarning)
        self._ytm = yield_to_maturity

    def set_price(self, prc):
        warnings.warn("Resetting Price Requires Recalculating Cash Flows, Durations, and Convexity. It is best to instantiate a new Bond.", UserWarning)
        self._price = prc

    def get_current_price(self):
        return self._price

    def get_current_YTM(self):
        return self._ytm

    def get_face_value(self):
        return self._face_value

    def get_coupon_rate(self):
        return self._coupon_rate

    def get_coupon_freq(self):
        return self._coupon_freq

    def calc_cashflows(self):
        cf_list = []
        pvcf_list = []
        for i in range(self._periods):
            if i == 0:
                cf = -self._face_value
            elif i == self._periods -1:
                cf = self._face_value + self._coupon_amt
            else:
                cf = self._coupon_amt
            cf_list.append((i,cf))
            if i != 0:
                denom = (1 + self._ytm/self._coupon_freq)**i
                pvcf_list.append((i, cf/denom))
        self.cash_flow = pd.DataFrame(cf_list)
        self.cash_flow.columns = ['period', 'cash flow']
        self.PVcash_flow = pd.DataFrame(pvcf_list)
        self.PVcash_flow.columns = ['period', 'PV cash flow']

    def get_cashflow(self):
        return self.cash_flow

    def get_PVcashflow(self):
        return self.PVcash_flow

    def calc_macaulay_duration(self):
        duration_calc = sum(self.PVcash_flow['period'] * self.PVcash_flow['PV cash flow'])
        self.duration = (duration_calc / self._price)/self._coupon_freq

    def calc_modified_duration(self):
        self.modified_duration = self.duration/ (1 + (self._ytm/self._coupon_freq))

    def calc_convexity(self):
        convexity_list = []
        for i in range(1, self._periods):
            pvcfi = self.PVcash_flow['PV cash flow'][self.PVcash_flow['period'] == i].item()
            convexity = 1/(1+self._ytm/self._coupon_freq)**2 * pvcfi * (i**2 + i)
            convexity_list.append(convexity)
        convexity_calc = sum(convexity_list)
        self.convexity = (convexity_calc / self._price)/self._coupon_freq**2

    def reprice(self, ytm_chg):
        mod_duration_adj = -ytm_chg * self.modified_duration * self._price
        convexity_adj = 0.5*self.convexity*ytm_chg**2*self.PVcash_flow['PV cash flow'].iloc[-1]
        return np.round(mod_duration_adj + convexity_adj + self.PVcash_flow['PV cash flow'].sum(),2)

    def bpv(self):
        return self.modified_duration / 100

    def get_total_PVcash_flow(self):
        return self.PVcash_flow['PV cash flow'].sum()

















