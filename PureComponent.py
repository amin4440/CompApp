import pickle

from Component import Component


class PureComponent(Component):

    def __init__(self, initial_prop_dict):
        super().__init__()
        if len(PureComponent.required_props_name) != len(initial_prop_dict):
            raise Exception("check initial properties dict")
        for prop_name in PureComponent.required_props_name:
            if prop_name in initial_prop_dict:
                if prop_name == "name":
                    self.__name = initial_prop_dict["name"]
                if prop_name == "Tc":
                    self.__Tc = initial_prop_dict["Tc"]
                if prop_name == "Pc":
                    self.__Pc = initial_prop_dict["Pc"]
                if prop_name == "omega":
                    self.__omega = initial_prop_dict["omega"]
                if prop_name == "Tnb":
                    self.__Tnb = initial_prop_dict["Tnb"]
                if prop_name == "MW":
                    self.__MW = initial_prop_dict["MW"]
                if prop_name == "viscosity25":
                    self.__visco25 = initial_prop_dict["viscosity25"]
                if prop_name == "Cp coefficients":
                    self.__Cp_coeff = initial_prop_dict["Cp coefficients"]
                if prop_name == "Antoine coeff":
                    self.__Antoine_coeffs = initial_prop_dict["Antoine coeffs"]
        self.__all_props = initial_prop_dict.copy()  # this line must be deleted after saving pure components

    @staticmethod
    def load_component(name):
        path = "components\\{}.dat".format(name)
        with open(path, "rb") as file:
            all_initial_props = pickle.load(file)
            component = PureComponent(all_initial_props)
            return component

    @staticmethod
    def save_component(properties_dict):
        name = properties_dict["name"]
        path = "components\\{}.dat".format(name)
        with open(path, "wb") as file:
            pickle.dump(properties_dict, file)
        print("file saved")


# todo
"""
we must create some components and save theme
"""
