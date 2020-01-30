import ProperyContainer


class Component(ProperyContainer):
    required_props_name = ["name", "Tc", "Pc", "omega", "MW", "Tnb", "viscosity25"]
    all_props = dict()

    def __init__(self, initial_prop_dict):
        if len(Component.required_props_name) != len(initial_prop_dict):
            raise
        for prop_name in Component.required_props_name:
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

        # now other properties must be calculate from initial properties

    @property
    def Tc(self):
        return self.__Tc

    @Tc.setter
    def Tc(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        raise Exception("you are not allowed to change this property")

    @property
    def Pc(self):
        return self.__Pc

    @Pc.setter
    def Pc(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def omega(self):
        return self.__omega

    @omega.setter
    def omega(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def Tnb(self):
        return self.__Tnb

    @Tnb.setter
    def Tnb(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def MW(self):
        return self.__MW

    @MW.setter
    def MW(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def visco25(self):
        return self.__visco25

    @visco25.setter
    def visco25(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def Cp_coeff(self):
        return self.__Cp_coeff

    @Cp_coeff.setter
    def Cp_coeff(self, value):
        raise Exception("you are not allowed to change this property")
