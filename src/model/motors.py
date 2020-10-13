class Motor:
    pass


class ElectricMotor(Motor):
    def __init__(
        self,
        eff_peak=0.94,
        rpm_plateau_start=2400,
        rpm_plateau_end=4000,
        torque_plateau_start=50,
        torque_plateau_end=150,
        eff_rpm_0=0.70,
        eff_rpm_8000=0.75,
    ):
        self.eff_peak = eff_peak
        self.rpm_plateau_start = rpm_plateau_start
        self.rpm_plateau_end = rpm_plateau_end
        self.torque_plateau_start = torque_plateau_start
        self.torque_plateau_end = torque_plateau_end
        self.eff_rpm_0 = eff_rpm_0
        self.eff_rpm_8000 = eff_rpm_8000

    def instant_efficiency(self, torque, rpm):
        if rpm < self.rpm_plateau_start:
            eff_rpm = self.eff_rpm_0 + (rpm / self.rpm_plateau_start) * (
                self.eff_peak - self.eff_rpm_0
            )
        elif rpm > self.rpm_plateau_start:
            eff_rpm = self.eff_peak + (
                (rpm - self.rpm_plateau_end) / (8000 - self.rpm_plateau_end)
            ) * (self.eff_rpm_8000 - self.eff_peak)
        else:
            eff_rpm = self.eff_peak

        if torque < self.torque_plateau_start:
            eff_torque = 0.91 + (0.09 * torque / self.torque_plateau_start)

        elif torque > self.torque_plateau_end:
            eff_torque = 1 - (0.25 * (torque-self.torque_plateau_end) /
                              self.torque_plateau_end)
        else:
            eff_torque = 1

        return eff_rpm * eff_torque

    def instant_efficiencies(self, torque_series, rpm_series):
        return [
            self.instant_efficiency(torque, rpm)
            for (torque, rpm) in zip(torque_series, rpm_series)
        ]


class PetrolMotor(Motor):
    pass
