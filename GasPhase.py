from math import log

from Phase import Phase


class GasPhase(Phase):
    def __init__(self, fluid, compositions):
        super().__init__(fluid)
        self.__compositions = compositions

    def calc_I(self, EoS, z, bm, fluid):
        P = fluid.P
        T = fluid.T
        z = fluid.calc_z_gas(self, )
        ro = P / (T * EoS.R * z)
        term1 = 1 / (EoS.omega - EoS.eps)
        term2 = (EoS.omega * bm * ro + 1) / (1 + EoS.eps * ro * bm)
        term3 = log(term2)
        return term1 * term3

    def calc_Dq_DT(self, am, bm, T, EoS, Dam_DT):
        term1 = Dam_DT / (bm * EoS.R * T)
        term2 = am / (bm * EoS.R * (T ** 2))
        return term1 - term2

    def calc_Dam_DT(self, fluid, compositions):
        T = fluid.T
        components = fluid.components
        sigmaj = 0
        sigmai = 0
        count = len(components)
        for j in range(count):
            for i in range(count):
                zi = compositions[i]
                zj = compositions[j]
                Ai = components[i].a
                Aj = components[j].a
                term1 = zi * zj * ((Ai * Aj) ** 0.5)
                alphaj = components[j].alpha
                alphai = components[i].alpha
                ki = components[i].k
                kj = components[j].k
                Tci = components[i].Tc
                Tcj = components[j].Tc
                term2 = (-ki / (2 * ((T * Tci) ** 0.5)))
                term3 = (-kj / (2 * ((T * Tcj) ** 0.5)))
                sigmai += term1 * (alphaj * term2 + alphai * term3)
            sigmaj += sigmai
        return sigmaj

    def calc_Hr(self, fluid, EoS, z):
        am = fluid.calc_am(EoS, self.compositions)
        bm = fluid.calc_bm(EoS, self.compositions)
        Dam_DT = self.calc_Dam_DT(fluid, self.compositions)
        Dq_DT = self.calc_Dq_DT(am, bm, fluid.T, EoS, Dam_DT)
        I = self.calc_I(EoS, z, bm, fluid)
        return EoS.R * fluid.T * (z - 1 + fluid.T * I * Dq_DT)

    def calc_H_ig(self, fluid):
        H_ig = 0
        component_count = len(fluid.components)
        for i in range(component_count):
            component = fluid.components[i]
            composition = self.compositions[i]
            H_ig_i = Phase.calc_H_ig_i(component.Cp_coeff, fluid.T, 298)
            H_ig += composition * H_ig_i
        return H_ig

    def calc_H(self, z):
        EoS = self.__EoS
        fluid = self.fluid
        am = fluid.calc_am(EoS, self.compositions)
        bm = fluid.calc_bm(EoS, self.compositions)
        z = fluid.calc_z_gas(self, EoS, am, bm, fluid.T, fluid.P)
        Hr = self.calc_Hr(fluid, EoS, z)
        H_ig = self.calc_H_ig(fluid)
        return H_ig + Hr

    def calc_entropy_residual(self, fluid, EoS, z):
        bm = fluid.calc_bm(EoS, self.compositions)
        am = fluid.calc_am(EoS, self.compositions)
        Dam_DT = self.calc_Dam_DT(fluid, self.compositions)
        S_R = log(z - EoS.calc_beta(bm, fluid.P, fluid.T)) + (
        (EoS.calc_q(am, bm, fluid.T) + fluid.T * (self.calc_Dq_DT(am, bm, fluid.T, EoS, Dam_DT)))) * self.calc_I(EoS, z,
                                                                                                                 bm,
                                                                                                                 fluid)
