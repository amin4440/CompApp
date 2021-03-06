import math


def alpha_calculator(component):
    T = component.fluid.T
    Tr = T / component.Tc
    a = 1 - Tr ** 0.5
    b = component.k * a
    c = 1 + b
    return c ** 2


class EoS:
    R = 8.3145

    def __init__(self, a_coeff, b_coeff, alpha_coeffs, eps, omega, sigma):
        self.__a_coeff = a_coeff
        self.__b_coeff = b_coeff
        self.__alpha_coeffs = alpha_coeffs
        self.__eps = eps
        self.__omega = omega
        self.__sigma = sigma

    @staticmethod
    def create_pr():
        a_coeff = 0.4572
        b_coeff = 0.0778
        alpha_coeff = [0.37464, 1.54226, 0.26992]
        eps = 1 - (2 ** 0.5)
        sigma = 1 + (2 ** 0.5)
        omega = 0.07779
        return EoS(a_coeff, b_coeff, alpha_coeff, eps, omega, sigma)

    @staticmethod
    def create_srk():
        a_coeff = 0.42748
        b_coeff = 0.08664
        alpha_coeff = [0.48, 1.574, 0.176]
        eps = 0
        omega = 0.08664
        sigma = 1
        return EoS(a_coeff, b_coeff, alpha_coeff, eps, omega, sigma)

    def calc_z(self, fluid):
        # this method returns a list(usually contains 3 values)
        pass

    @staticmethod
    def calc_beta(b, P, T):
        return b * P / (EoS.R * T)

    @staticmethod
    def calc_q(a, b, T):
        return a / (b * EoS.R * T)

    def calc_z_liquid(self, q, beta, b):
        old_z = b
        z_calculator = lambda z: beta + (z + self.__eps * beta) * (z + self.__sigma * beta) * (1 + beta - z) / (
                q * beta)
        new_z = z_calculator(old_z)
        accuracy = 10 ** -4
        while abs(new_z - old_z) > accuracy:
            old_z = new_z
            new_z = z_calculator(old_z)
        return new_z

    def calc_z_gas(self, q, beta):
        old_z = 1
        z_calculator = lambda z: 1 + beta - q * beta * (
                (z - beta) / ((z + self.__eps * beta) * (z + self.__sigma * beta)))
        new_z = z_calculator(old_z)
        accuracy = 10 ** -7
        while abs(new_z - old_z) > accuracy:
            old_z = new_z
            new_z = z_calculator(old_z)
        return new_z

    def calc_Gr(self, z, T, P, a, b):
        ro = P / (z * EoS.R * T)
        q = EoS.calc_q(a, b, T)
        term1 = math.log(1 - ro * b)
        term2 = EoS.R * T * (z - 1 - term1) * z
        term3 = 1 / (self.eps - self.eps)
        term4 = q * term3 * math.log((1 + self.eps * ro * b) / (1 + self.eps * ro * b))
        Gr = term2 - term4
        return Gr

    @property
    def a_coeff(self):
        return self.__a_coeff

    @a_coeff.setter
    def a_coeff(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def b_coeff(self):
        return self.__b_coeff

    @b_coeff.setter
    def b_coeff(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def alpha_coeffs(self):
        return self.__alpha_coeffs

    @alpha_coeffs.setter
    def alpha_coeffs(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def eps(self):
        return self.__eps

    @eps.setter
    def eps(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def omega(self):
        return self.__omega

    @omega.setter
    def omega(self, value):
        raise Exception("you are not allowed to change this property")

    @property
    def sigma(self):
        return self.__sigma

    @sigma.setter
    def sigma(self, sigma):
        raise Exception("you are not allowed to change this property")

    def a_calculator(self, component):
        return self.a_coeff * (EoS.R ** 2) * (component.Tc ** 2) / component.Pc

    def b_calculator(self, component):
        return self.b_coeff * EoS.R * component.Tc / component.P4

    def k_calculator(self, component):
        a = self.alpha_coeffs[0]
        b = self.alpha_coeffs[1]
        c = self.alpha_coeffs[2]
        return a + b * component.omega - c * (component.omega ** 2)

    # now we need to calc alpha for each component
    # we need temperature but temp is belonged to fluid and here we don't access Fluid
    #
