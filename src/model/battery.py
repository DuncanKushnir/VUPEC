from functools import partial
from model.constants import *


def process_battery_demand(global_parameters, vehicle, model_df):
    if vehicle.battery:
        soc, losses = [], []
        batt = vehicle.battery_obj
        for row in model_df.itertuples():
            ett, lhb = batt.attempt_charge_change(row.energy_draw_battery * -1, 1)
            soc.append(batt.soc)
            losses.append(lhb)
        model_df["soc"] = soc
        model_df["loss_thermal_battery"] = losses

    else:
        model_df["soc"] = 0.0
    return model_df


def constant_eff(c_val, c_eff=0.95):
    return c_eff


class Battery:
    def __init__(
        self, capacity_kwh, chemistry, ucl=0.9, lcl=0.1, efficiency_curve=None
    ):
        """
        A tier 1 battery implementation that can use either a constant or varying
        efficiency curve to calculate internal soc changes and heat losses for
        varying demands at the terminal.

        Most external use should be through the attempt_charge_change function,
        which will report the actual energy through the terminal as well as heat
        losses.

        :param capacity_kwh: float e.g. 16.4  for kWh GROSS capacity
        :param chemistry: any string
        :param ucl: upper charge limit (e.g. 0.9)
        :param lcl: lower charge limit (e.g. 0.1
        :param efficiency_curve: if None, uses default, if float, applies constant,
        or can be passed a curve object that must report a decimal efficiency (0 ->
        1.0) when given a c value.
        """
        self.capacity_kwh = float(capacity_kwh)
        self.name = f"{capacity_kwh} kWh: {chemistry}"
        self.capacity_j = capacity_kwh * KWH_J
        self.ucl = ucl
        self.lcl = lcl
        self._soc = 0.0

        # efficiency can be constant, default, or a curve based on power.
        if isinstance(efficiency_curve, float):
            self.get_efficiency = partial(constant_eff, c_eff=efficiency_curve)
        elif efficiency_curve is None:
            self.get_efficiency = constant_eff
        else:
            self.get_efficiency = efficiency_curve

        self.soc = 1.0

    @property
    def soc(self):
        return self._soc

    @soc.setter
    def soc(self, pct):
        pct = max(self.lcl, pct)
        pct = min(self.ucl, pct)
        self._soc = pct

    @property
    def max_in_pct(self):
        return self.ucl - self.soc

    @property
    def max_out_pct(self):
        return self.soc - self.lcl

    @property
    def max_in_j(self):
        return self.max_in_pct * self.capacity_kwh * KWH_J

    @property
    def max_out_j(self):
        return (self.max_out_pct * self.capacity_kwh * KWH_J) * -1

    def _change_charge(self, energy_j):
        charge_pct = energy_j / (KWH_J * self.capacity_kwh)
        self.soc = self.soc + charge_pct

    def attempt_charge_change(self, energy_j_terminal, duration_s):
        req_power = energy_j_terminal / duration_s
        req_c = self.get_c_value(req_power)
        req_eff = self.get_efficiency(req_c)
        if energy_j_terminal > 0:
            req_internal_j = energy_j_terminal * req_eff
            actual_j = min(self.max_in_j, req_internal_j)
            energy_through_terminal = actual_j / req_eff

        else:
            req_internal_j = energy_j_terminal / req_eff
            actual_j = max(self.max_out_j, req_internal_j)
            energy_through_terminal = actual_j * req_eff

        self._change_charge(actual_j)
        losses_heat = abs(actual_j - energy_through_terminal)

        return (energy_through_terminal, losses_heat)

    def get_c_value(self, power_w):
        return power_w * 3600 / self.capacity_j

    def recharge_given_c(self, c_val):
        req_eff = self.get_efficiency(c_val)
        energy_terminal = self.max_in_j / req_eff
        return self.attempt_charge_change(energy_terminal, 1 / c_val)

    def recharge_given_power(self, power_w):
        req_c = self.get_c_value(power_w)
        return self.recharge_given_c(req_c)

    def recharge_given_time(self, time_s):
        req_power = self.max_in_j / time_s
        return self.recharge_given_power(req_power)


if __name__ == "__main__":
    B = Battery(20, "LiFEPO4", 0.90, 0.1, 0.9)
    print(B.soc)
    B.soc = 0.5
    print(B.attempt_charge_change(5000000, 1))
    print(B.soc)
    print(B.attempt_charge_change(5000000, 1))
    print(B.soc)
    print(B.attempt_charge_change(-5000000, 1))
    print(B.soc)
    B.soc = 0.11
    print(B.attempt_charge_change(-5000000, 1))
    print(B.soc)
    print(B.max_in_j)
    print(B.recharge_given_power(10000))
