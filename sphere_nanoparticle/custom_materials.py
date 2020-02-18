from meep import LorentzianSusceptibility, Medium


def material_lib():
    lib = ['custom_ag']
    return lib


def material_lib_dict(material_name):
    def custom_ag():
        ag_sus = [LorentzianSusceptibility(frequency=1e-20, gamma=0.0038715, sigma=4.4625e+39),
                  LorentzianSusceptibility(frequency=0.065815, gamma=0.31343, sigma=7.9247),
                  LorentzianSusceptibility(frequency=0.36142, gamma=0.036456, sigma=0.50133),
                  LorentzianSusceptibility(frequency=0.66017, gamma=0.0052426, sigma=0.013329),
                  LorentzianSusceptibility(frequency=0.73259, gamma=0.07388, sigma=0.82655),
                  LorentzianSusceptibility(frequency=1.6365, gamma=0.19511, sigma=1.1133)]
        return Medium(epsilon=1, E_susceptibilities=ag_sus)

    material_dict = dict(custom_ag=custom_ag())
    return material_dict[material_name]
