from meep import LorentzianSusceptibility, Medium, DrudeSusceptibility, FreqRange


def material_lib():
    return tuple(['custom_ag', 'meep_ag'])


def material_lib_dict(material_name, um_scale):
    def meep_ag():
        metal_range = FreqRange(min=um_scale / 12.398, max=um_scale / .24797)

        ag_plasma_frq = 9.01 * um_scale / 1.23984193
        ag_f0 = 0.845
        ag_frq0 = 1e-10
        ag_gam0 = 0.048 * um_scale / 1.23984193
        ag_sig0 = ag_f0 * ag_plasma_frq ** 2 / ag_frq0 ** 2
        ag_f1 = 0.065
        ag_frq1 = 0.816 * um_scale / 1.23984193  # 1.519 um
        ag_gam1 = 3.886 * um_scale / 1.23984193
        ag_sig1 = ag_f1 * ag_plasma_frq ** 2 / ag_frq1 ** 2
        ag_f2 = 0.124
        ag_frq2 = 4.481 * um_scale / 1.23984193  # 0.273 um
        ag_gam2 = 0.452 * um_scale / 1.23984193
        ag_sig2 = ag_f2 * ag_plasma_frq ** 2 / ag_frq2 ** 2
        ag_f3 = 0.011
        ag_frq3 = 8.185 * um_scale / 1.23984193  # 0.152 um
        ag_gam3 = 0.065 * um_scale / 1.23984193
        ag_sig3 = ag_f3 * ag_plasma_frq ** 2 / ag_frq3 ** 2
        ag_f4 = 0.840
        ag_frq4 = 9.083 * um_scale / 1.23984193  # 0.137 um
        ag_gam4 = 0.916 * um_scale / 1.23984193
        ag_sig4 = ag_f4 * ag_plasma_frq ** 2 / ag_frq4 ** 2
        ag_f5 = 5.646
        ag_frq5 = 20.29 * um_scale / 1.23984193  # 0.061 um
        ag_gam5 = 2.419 * um_scale / 1.23984193
        ag_sig5 = ag_f5 * ag_plasma_frq ** 2 / ag_frq5 ** 2

        ag_susc = [DrudeSusceptibility(frequency=ag_frq0, gamma=ag_gam0, sigma=ag_sig0),
                   LorentzianSusceptibility(frequency=ag_frq1, gamma=ag_gam1, sigma=ag_sig1),
                   LorentzianSusceptibility(frequency=ag_frq2, gamma=ag_gam2, sigma=ag_sig2),
                   LorentzianSusceptibility(frequency=ag_frq3, gamma=ag_gam3, sigma=ag_sig3),
                   LorentzianSusceptibility(frequency=ag_frq4, gamma=ag_gam4, sigma=ag_sig4),
                   LorentzianSusceptibility(frequency=ag_frq5, gamma=ag_gam5, sigma=ag_sig5)]

        return Medium(epsilon=1.0, E_susceptibilities=ag_susc, valid_freq_range=metal_range)

    def custom_ag():
        ag_sus = [LorentzianSusceptibility(frequency=1e-20, gamma=0.0038715, sigma=4.4625e+39),
                  LorentzianSusceptibility(frequency=0.065815, gamma=0.31343, sigma=7.9247),
                  LorentzianSusceptibility(frequency=0.36142, gamma=0.036456, sigma=0.50133),
                  LorentzianSusceptibility(frequency=0.66017, gamma=0.0052426, sigma=0.013329),
                  LorentzianSusceptibility(frequency=0.73259, gamma=0.07388, sigma=0.82655),
                  LorentzianSusceptibility(frequency=1.6365, gamma=0.19511, sigma=1.1133)]
        return Medium(epsilon=1, E_susceptibilities=ag_sus)

    material_dict = dict(custom_ag=custom_ag(), meep_ag=meep_ag())
    return material_dict[material_name]
