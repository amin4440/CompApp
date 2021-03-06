from math import log, exp


class Component:
    required_props_name = ["name", "Tc", "Pc", "omega", "MW", "Tnb", "viscosity25", "Antoine coeffs"]

    def __init__(self):
        pass

    def calc_Dam_Dni(self, fluid, am, compositions):
        n = fluid.n
        ai = self.__a
        ans1 = 2 / n
        ans2 = 0
        for j in range(len(fluid.components)):
            component = fluid.components[j]
            composition = compositions[j]
            aj = component.a
            ans2 += composition * ((ai * aj) ** 0.5) - am
        return ans1 * ans2

    def calc_Dbm_Dni(self, fluid, bm):
        return (self.b - bm) / fluid.n

    def calc_Dq_Dni(self, Dam_Dni, Dbm_Dni, am, bm):
        term1 = Dam_Dni / bm
        term2 = am * Dbm_Dni / (bm ** 2)
        return term1 - term2

    def calc_DI_Dni(self, EoS, T, P, z, bm, Dbm_Dni):
        ro = P / (T * EoS.R * z)
        term1 = (ro * EoS.sigma) / (1 + EoS.sigma * ro * bm)
        term2 = (ro * EoS.eps) / (1 + EoS.eps * ro * bm)
        return Dbm_Dni * (term1 - term2)

    def calc_Dz_Dni(self, Dbm_Dni, EoS, Dq_Dni, am, bm, T, P, z):
        q = EoS.calc_q(am, bm, T)
        ro = P / (T * EoS.R * z)
        term1 = ro * Dbm_Dni / (1 - ro * bm) ** 2
        term2 = ro * bm * Dq_Dni / ((1 + EoS.eps * ro * bm) * (1 + EoS.sigma * ro * bm))
        term3 = ro * Dbm_Dni / ((1 + EoS.eps * ro * bm) * (1 + EoS.sigma * ro * bm))
        term4 = (ro ** 2) * bm * (EoS.eps ** 2) / (
                ((1 + EoS.eps * ro * bm) ** 2) * (1 + EoS.sigma * ro * bm))
        term5 = (ro ** 2) * bm * EoS.sigma * Dbm_Dni / (
                (1 + EoS.eps * ro * bm) * ((1 + EoS.sigma * ro * bm) ** 2))
        term6 = q * (term3 - term4 - term5)
        term7 = term1 - term2 - term6
        return term7

    def calcu_DGr_Dni(self, Dz_Dni, Dbm_Dni, EoS, Dq_Dni, DI_Dni, T, P, z, am, bm):
        ro = P / (T * EoS.R * z)
        term1 = ro * Dbm_Dni * z / (1 - ro * bm)
        term2 = 1 / (EoS.sigma - EoS.eps)
        I = term2 * log((1 + EoS.sigma * ro * bm) / (1 + EoS.eps * ro * bm))
        q = EoS.calc_q(am, bm, T)
        term3 = Dz_Dni * log(1 - ro * bm - I * Dq_Dni - q * DI_Dni)
        ans = EoS.R * T * (Dz_Dni + term1 - term3)
        return ans

    def calc_z_i(self, T, P, EoS):
        a = self.__a
        b = self.__b
        q = EoS.calc_q(a, b, T)
        beta = EoS.calc_beta(b, P, T)
        z = EoS.calc_z_liquid(q, beta)
        return z

    def calc_Gr(self, EoS, T, P, z):
        a = self.__a
        b = self.__b
        Gr = EoS.calc_Gr(z, T, P, a, b)
        return Gr

    def calc_a(self, EoS):
        a = EoS.a_coeff * 0.45724 * (EoS.R ** 2) * (self.Tc ** 2) / self.Pc
        self.__a = self.__alpha * a

    def calc_b(self, EoS):
        self.__b = EoS.b_coeff * EoS.R * self.Tc / self.Pc

    def calc_k(self, EoS):
        a = EoS.alpha_coeffs[0]
        b = EoS.alpha_coeffs[1]
        c = EoS.alpha_coeffs[2]
        self.__k = a + b * self.omega - c * (self.omega ** 2)
        return self.__k

    def calc_alpha(self, k, T):
        Tr = T / self.Tc
        a = 1 - (Tr ** 0.5)
        b = k * a
        c = 1 + b
        self.__alpha = c ** 2
        return self.__alpha

    def calc_Psat(self, T):
        A = self.Antoine_coeffs[0]
        B = self.Antoine_coeffs[1]
        C = self.Antoine_coeffs[2]
        Psat = exp(A - B / (T + C))
        self.__Psat = Psat
        return Psat

    def set_yi_bubble(self, composition, gama, Psat, bubble_P, PHI):
        y_i = composition * gama * Psat / (PHI * bubble_P)
        return y_i


    @property
    def Antoine_coeffs(self):
        return self.__Antoine_coeffs

    @Antoine_coeffs.setter
    def Antoine_coeffs(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def Psat(self):
        return self.__Psat

    @Psat.setter
    def Psat(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def k(self):
        return self.__k

    @k.setter
    def k(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def all_props(self):
        return self.__all_props

    @all_props.setter
    def all_props(self, value):
        raise Exception("you are not allowed to change this property")

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
