from model.common import ObjDict
from model.drive_cycles import DriveCycle

class Model:
    init_type = 'base'

    def __init__(self, make, model):



    def make_variation(self, variation_dict):
        pass


    def calculate_dc(self, drivecycle):
        pass


    def __call__(self, drive_cycle_df):
        if isinstance(drive_cycle_df, DriveCycle):
            drive_cycle_df = DriveCycle.to_df()




    @staticmethod
    def from_manu_model(manufacturer, model):
        pass

