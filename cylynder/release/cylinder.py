from meep import Vector3, Cylinder, inf, LorentzianSusceptibility, Medium, Volume, Source, GaussianSource, Ex, \
    Simulation, PML, FluxRegion, get_flux_freqs, get_fluxes, at_every, stop_when_fields_decayed, Animate2D, \
    in_volume, Mirror, X, DrudeSusceptibility, FreqRange
import argparse
import matplotlib.pyplot as plt
import numpy as np
from os import path, makedirs


def material(material_name):
    def meep_sio2():
        SiO2_range = FreqRange(min=um_scale / 1.77, max=um_scale / 0.25)

        SiO2_frq1 = 1 / (0.103320160833333 * um_scale)
        SiO2_gam1 = 1 / (12.3984193000000 * um_scale)
        SiO2_sig1 = 1.12

        SiO2_susc = [LorentzianSusceptibility(frequency=SiO2_frq1, gamma=SiO2_gam1, sigma=SiO2_sig1)]

        SiO2 = Medium(epsilon=1.0, E_susceptibilities=SiO2_susc, valid_freq_range=SiO2_range)
        return SiO2

    def vac():
        return Medium(epsilon=1)

    def custom_ag():
        ag_sus = [LorentzianSusceptibility(frequency=1e-20, gamma=0.0038715, sigma=4.4625e+39),
                  LorentzianSusceptibility(frequency=0.065815, gamma=0.31343, sigma=7.9247),
                  LorentzianSusceptibility(frequency=0.36142, gamma=0.036456, sigma=0.50133),
                  LorentzianSusceptibility(frequency=0.66017, gamma=0.0052426, sigma=0.013329),
                  LorentzianSusceptibility(frequency=0.73259, gamma=0.07388, sigma=0.82655),
                  LorentzianSusceptibility(frequency=1.6365, gamma=0.19511, sigma=1.1133)]
        return Medium(epsilon=1.0001, E_susceptibilities=ag_sus)

    def meep_ag():
        Ag_plasma_frq = 9.01 * eV_um_scale
        Ag_f0 = 0.845
        Ag_frq0 = 1e-10
        Ag_gam0 = 0.048 * eV_um_scale
        Ag_sig0 = Ag_f0 * Ag_plasma_frq ** 2 / Ag_frq0 ** 2
        Ag_f1 = 0.065
        Ag_frq1 = 0.816 * eV_um_scale  # 1.519 um
        Ag_gam1 = 3.886 * eV_um_scale
        Ag_sig1 = Ag_f1 * Ag_plasma_frq ** 2 / Ag_frq1 ** 2
        Ag_f2 = 0.124
        Ag_frq2 = 4.481 * eV_um_scale  # 0.273 um
        Ag_gam2 = 0.452 * eV_um_scale
        Ag_sig2 = Ag_f2 * Ag_plasma_frq ** 2 / Ag_frq2 ** 2
        Ag_f3 = 0.011
        Ag_frq3 = 8.185 * eV_um_scale  # 0.152 um
        Ag_gam3 = 0.065 * eV_um_scale
        Ag_sig3 = Ag_f3 * Ag_plasma_frq ** 2 / Ag_frq3 ** 2
        Ag_f4 = 0.840
        Ag_frq4 = 9.083 * eV_um_scale  # 0.137 um
        Ag_gam4 = 0.916 * eV_um_scale
        Ag_sig4 = Ag_f4 * Ag_plasma_frq ** 2 / Ag_frq4 ** 2
        Ag_f5 = 5.646
        Ag_frq5 = 20.29 * eV_um_scale  # 0.061 um
        Ag_gam5 = 2.419 * eV_um_scale
        Ag_sig5 = Ag_f5 * Ag_plasma_frq ** 2 / Ag_frq5 ** 2

        Ag_susc = [DrudeSusceptibility(frequency=Ag_frq0, gamma=Ag_gam0, sigma=Ag_sig0),
                   LorentzianSusceptibility(frequency=Ag_frq1, gamma=Ag_gam1, sigma=Ag_sig1),
                   LorentzianSusceptibility(frequency=Ag_frq2, gamma=Ag_gam2, sigma=Ag_sig2),
                   LorentzianSusceptibility(frequency=Ag_frq3, gamma=Ag_gam3, sigma=Ag_sig3),
                   LorentzianSusceptibility(frequency=Ag_frq4, gamma=Ag_gam4, sigma=Ag_sig4),
                   LorentzianSusceptibility(frequency=Ag_frq5, gamma=Ag_gam5, sigma=Ag_sig5)]

        Ag = Medium(epsilon=1.0, E_susceptibilities=Ag_susc, valid_freq_range=metal_range)
        return Ag

    def meep_au():
        metal_range = FreqRange(min=um_scale / 6.1992, max=um_scale / .24797)
        Au_plasma_frq = 9.03 * eV_um_scale
        Au_f0 = 0.760
        Au_frq0 = 1e-10
        Au_gam0 = 0.053 * eV_um_scale
        Au_sig0 = Au_f0 * Au_plasma_frq ** 2 / Au_frq0 ** 2
        Au_f1 = 0.024
        Au_frq1 = 0.415 * eV_um_scale  # 2.988 um
        Au_gam1 = 0.241 * eV_um_scale
        Au_sig1 = Au_f1 * Au_plasma_frq ** 2 / Au_frq1 ** 2
        Au_f2 = 0.010
        Au_frq2 = 0.830 * eV_um_scale  # 1.494 um
        Au_gam2 = 0.345 * eV_um_scale
        Au_sig2 = Au_f2 * Au_plasma_frq ** 2 / Au_frq2 ** 2
        Au_f3 = 0.071
        Au_frq3 = 2.969 * eV_um_scale  # 0.418 um
        Au_gam3 = 0.870 * eV_um_scale
        Au_sig3 = Au_f3 * Au_plasma_frq ** 2 / Au_frq3 ** 2
        Au_f4 = 0.601
        Au_frq4 = 4.304 * eV_um_scale  # 0.288 um
        Au_gam4 = 2.494 * eV_um_scale
        Au_sig4 = Au_f4 * Au_plasma_frq ** 2 / Au_frq4 ** 2
        Au_f5 = 4.384
        Au_frq5 = 13.32 * eV_um_scale  # 0.093 um
        Au_gam5 = 2.214 * eV_um_scale
        Au_sig5 = Au_f5 * Au_plasma_frq ** 2 / Au_frq5 ** 2

        Au_susc = [DrudeSusceptibility(frequency=Au_frq0, gamma=Au_gam0, sigma=Au_sig0),
                   LorentzianSusceptibility(frequency=Au_frq1, gamma=Au_gam1, sigma=Au_sig1),
                   LorentzianSusceptibility(frequency=Au_frq2, gamma=Au_gam2, sigma=Au_sig2),
                   LorentzianSusceptibility(frequency=Au_frq3, gamma=Au_gam3, sigma=Au_sig3),
                   LorentzianSusceptibility(frequency=Au_frq4, gamma=Au_gam4, sigma=Au_sig4),
                   LorentzianSusceptibility(frequency=Au_frq5, gamma=Au_gam5, sigma=Au_sig5)]

        Au = Medium(epsilon=1.0, E_susceptibilities=Au_susc, valid_freq_range=metal_range)
        return Au

    def meep_pt():
        Pt_plasma_frq = 9.59 * eV_um_scale
        Pt_f0 = 0.333
        Pt_frq0 = 1e-10
        Pt_gam0 = 0.080 * eV_um_scale
        Pt_sig0 = Pt_f0 * Pt_plasma_frq ** 2 / Pt_frq0 ** 2
        Pt_f1 = 0.191
        Pt_frq1 = 0.780 * eV_um_scale  # 1.590 um
        Pt_gam1 = 0.517 * eV_um_scale
        Pt_sig1 = Pt_f1 * Pt_plasma_frq ** 2 / Pt_frq1 ** 2
        Pt_f2 = 0.659
        Pt_frq2 = 1.314 * eV_um_scale  # 0.944 um
        Pt_gam2 = 1.838 * eV_um_scale
        Pt_sig2 = Pt_f2 * Pt_plasma_frq ** 2 / Pt_frq2 ** 2
        Pt_f3 = 0.547
        Pt_frq3 = 3.141 * eV_um_scale  # 0.395 um
        Pt_gam3 = 3.668 * eV_um_scale
        Pt_sig3 = Pt_f3 * Pt_plasma_frq ** 2 / Pt_frq3 ** 2
        Pt_f4 = 3.576
        Pt_frq4 = 9.249 * eV_um_scale  # 0.134 um
        Pt_gam4 = 8.517 * eV_um_scale
        Pt_sig4 = Pt_f4 * Pt_plasma_frq ** 2 / Pt_frq4 ** 2

        Pt_susc = [DrudeSusceptibility(frequency=Pt_frq0, gamma=Pt_gam0, sigma=Pt_sig0),
                   LorentzianSusceptibility(frequency=Pt_frq1, gamma=Pt_gam1, sigma=Pt_sig1),
                   LorentzianSusceptibility(frequency=Pt_frq2, gamma=Pt_gam2, sigma=Pt_sig2),
                   LorentzianSusceptibility(frequency=Pt_frq3, gamma=Pt_gam3, sigma=Pt_sig3),
                   LorentzianSusceptibility(frequency=Pt_frq4, gamma=Pt_gam4, sigma=Pt_sig4)]

        Pt = Medium(epsilon=1.0, E_susceptibilities=Pt_susc, valid_freq_range=metal_range)
        return Pt

    def meep_pd():
        Pd_plasma_frq = 9.72 * eV_um_scale
        Pd_f0 = 0.330
        Pd_frq0 = 1e-10
        Pd_gam0 = 0.008 * eV_um_scale
        Pd_sig0 = Pd_f0 * Pd_plasma_frq ** 2 / Pd_frq0 ** 2
        Pd_f1 = 0.649
        Pd_frq1 = 0.336 * eV_um_scale  # 3.690 um
        Pd_gam1 = 2.950 * eV_um_scale
        Pd_sig1 = Pd_f1 * Pd_plasma_frq ** 2 / Pd_frq1 ** 2
        Pd_f2 = 0.121
        Pd_frq2 = 0.501 * eV_um_scale  # 2.475 um
        Pd_gam2 = 0.555 * eV_um_scale
        Pd_sig2 = Pd_f2 * Pd_plasma_frq ** 2 / Pd_frq2 ** 2
        Pd_f3 = 0.638
        Pd_frq3 = 1.659 * eV_um_scale  # 0.747 um
        Pd_gam3 = 4.621 * eV_um_scale
        Pd_sig3 = Pd_f3 * Pd_plasma_frq ** 2 / Pd_frq3 ** 2
        Pd_f4 = 0.453
        Pd_frq4 = 5.715 * eV_um_scale  # 0.217 um
        Pd_gam4 = 3.236 * eV_um_scale
        Pd_sig4 = Pd_f4 * Pd_plasma_frq ** 2 / Pd_frq4 ** 2

        Pd_susc = [DrudeSusceptibility(frequency=Pd_frq0, gamma=Pd_gam0, sigma=Pd_sig0),
                   LorentzianSusceptibility(frequency=Pd_frq1, gamma=Pd_gam1, sigma=Pd_sig1),
                   LorentzianSusceptibility(frequency=Pd_frq2, gamma=Pd_gam2, sigma=Pd_sig2),
                   LorentzianSusceptibility(frequency=Pd_frq3, gamma=Pd_gam3, sigma=Pd_sig3),
                   LorentzianSusceptibility(frequency=Pd_frq4, gamma=Pd_gam4, sigma=Pd_sig4)]

        Pd = Medium(epsilon=1.0, E_susceptibilities=Pd_susc, valid_freq_range=metal_range)
        return Pd

    um_scale = 0.1
    eV_um_scale = um_scale / 1.23984193
    metal_range = FreqRange(min=um_scale / 12.398, max=um_scale / .24797)

    material_dict = {'custom_ag': custom_ag(),
                     'meep_ag': meep_ag(),
                     'meep_au': meep_au(),
                     'meep_pt': meep_pt(),
                     'meep_pd': meep_pd(),
                     'vac': vac(),
                     'meep_sio2': meep_sio2()}
    return material_dict[material_name]


def parser():
    material_names = ['custom_ag', 'meep_ag', 'meep_au', 'meep_pt', 'meep_pd', 'vac', 'meep_sio2']
    parse = argparse.ArgumentParser('cylynder')
    parse.add_argument('-res', metavar='resolution', type=int, default=25,
                       help='Specifies the computational grid resolution in pixels per distance unit default: 25px/0.1um')
    parse.add_argument('-rad1', metavar='radius', type=float, default=0.25,
                       help='The radius of the larger cylinder. default: 0.25 (25nm)')
    parse.add_argument('-rad2', metavar='tuberad', type=float, default=0.0,
                       help='Smaller cylinder radius. default: 0.0')
    parse.add_argument('-mat1', metavar='material1', type=str, default='custom_ag',
                       choices=material_names,
                       help=':Large cylinder material. default: custom_ag')
    parse.add_argument('-mat2', metavar='material2', type=str, default='custom_ag',
                       choices=material_names,
                       help='Smaller cylinder material. default: custom_ag')
    parse.add_argument('-fcen', metavar='freqency', type=float, default=0.3,
                       help=' The center frequency f. default: 0.3 (meep unit)')
    parse.add_argument('-df', metavar='fwidth', type=float, default=0.3,
                       help='Synonym for width=1/x. The width w (omega) used in the Gaussian. default: 0.3')
    parse.add_argument('-dpml', metavar='dpml', type=float, default=1,
                       help='PML layer thickness. default: 1')
    parse.add_argument('-nfreq', metavar='nfreq', type=int, default=60,
                       help='')
    parse.add_argument('-name', metavar='outpath', type=str, default='rad_25_Ag_full',
                       help='Output folder name. default: rad_25_Ag_full')
    parse.add_argument('-cutoff', metavar='cutoff', type=float, default=5.0,
                       help='How many widths the current decays for before it is cut off and set to zero. default: 5.0')
    parse.add_argument('-decay', metavar='decay', type=float, default=1e-6,
                       help='see: https://meep.readthedocs.io/en/latest/Python_User_Interface/#run-functions (stop_when_fields_decayed). default: 1e-6')
    parse.add_argument('-rt', metavar='real_time', type=bool, default=True,
                       help='output ex during calculation. default: True')
    arg = vars(parse.parse_args())
    return arg


def rad_units(radius):
    def unit(distance):
        return radius * distance

    return unit


def tube(rad1, rad2, mat1, mat2):
    return [Cylinder(radius=rad1, height=inf, material=material(mat1)),
            Cylinder(radius=rad2, height=inf, material=material(mat2))]


def cell(u, dpml):
    return Vector3(u(8) + 2 * dpml, u(8) + 2 * dpml)


def source(fcen, df, cutoff, u):
    return [Source(GaussianSource(frequency=fcen, width=df, cutoff=cutoff), Ex,
                   center=Vector3(0, u(4)), size=Vector3(u(8), 0))]


def simulation(cell_size, resolution, geom, dpml, sources):
    return Simulation(cell_size=cell_size,
                      resolution=resolution,
                      geometry=geom,
                      boundary_layers=[PML(dpml)],
                      sources=sources,
                      output_single_precision=True,
                      eps_averaging=False,
                      force_complex_fields=False,
                      Courant=0.25,
                      symmetries=[Mirror(direction=X, phase=-1)])


def flux_add(fcen, df, nfreq, u):
    def flux(sim, x, y, sx, sy):
        return sim.add_flux(fcen, df, nfreq,
                            FluxRegion(center=Vector3(u(x), u(y)), size=Vector3(u(sx), u(sy))))

    return flux


def plot(sim, name, out_path):
    plt.figure()
    sim.plot2D(boundary_parameters={'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y',
                                    'edgecolor': 'b', 'alpha': 0.3},
               eps_parameters={'cmap': 'gray'})
    plt.savefig(path.join(out_path, name + '.png'))
    plt.close()


def sim_no_geom(cell_size, resolution, dpml, sources, fl, u, decay, out_path):
    sim = simulation(cell_size, resolution, [], dpml, sources)

    top = fl(sim, 0, 2, 4, 0)
    bottom = fl(sim, 0, -2, 4, 0)
    left = fl(sim, -2, 0, 0, 4)
    right = fl(sim, 2, 0, 0, 4)
    incident = fl(sim, 0, -4, 4, 0)

    plot(sim, 'no_geom', out_path)

    sim.run(until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, u(-4)), decay))

    flux_data = dict(top=sim.get_flux_data(top),
                     bottom=sim.get_flux_data(bottom),
                     left=sim.get_flux_data(left),
                     right=sim.get_flux_data(right))

    freq = np.asarray(get_flux_freqs(top))

    inc = np.absolute(np.asarray(get_fluxes(incident)))
    incident_pow = inc / u(4)
    wave_length = np.divide(100, freq, dtype=np.float)

    sim.reset_meep()

    return dict(flux_data=flux_data, incident_pow=incident_pow, wl=wave_length)


def sim_with_geom(cell_size, resolution, geom, dpml, sources, fl, u, out_path, decay, rt, fl_data=None, scat=True):
    sim = simulation(cell_size, resolution, geom, dpml, sources)

    top = fl(sim, 0, 2, 4, 0)
    bottom = fl(sim, 0, -2, 4, 0)
    left = fl(sim, -2, 0, 0, 4)
    right = fl(sim, 2, 0, 0, 4)

    if scat:

        sim.load_minus_flux_data(top, fl_data['top'])
        sim.load_minus_flux_data(bottom, fl_data['bottom'])
        sim.load_minus_flux_data(left, fl_data['left'])
        sim.load_minus_flux_data(right, fl_data['right'])

        sim.run(until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, u(-4)), decay))

        scat_top = get_fluxes(top)
        scat_bottom = get_fluxes(bottom)
        scat_left = get_fluxes(left)
        scat_right = get_fluxes(right)

        scat_pow = np.absolute(-np.asarray(scat_top) + np.asarray(scat_bottom)
                               + np.asarray(scat_left) - np.asarray(scat_right))

        sim.reset_meep()

        return scat_pow

    else:

        plot(sim, 'geom', out_path)

        animate = Animate2D(sim,
                            fields=Ex,
                            realtime=True,
                            field_parameters={'alpha': 0.8, 'cmap': 'RdBu', 'interpolation': 'spline36'},
                            eps_parameters={'cmap': 'binary'})

        sim.run(at_every(0.1, in_volume(Volume(size=Vector3(u(4), u(4)), center=Vector3(0, 0)), animate)),
                until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, u(-4)), decay))

        animate.to_mp4(fps=12, filename=path.join(out_path, 'ex_anim.mp4'))

        abs_top = get_fluxes(top)
        abs_bottom = get_fluxes(bottom)
        abs_left = get_fluxes(left)
        abs_right = get_fluxes(right)

        abs_pow = -np.asarray(abs_top) + np.asarray(abs_bottom) + np.asarray(abs_left) - np.asarray(abs_right)

        return abs_pow


def initialize():
    param = parser()

    unit = rad_units(param['rad1'])
    geom = tube(param['rad1'], param['rad2'], param['mat1'], param['mat2'])
    src = source(param['fcen'], param['df'], param['cutoff'], unit)
    cz = cell(unit, param['dpml'])
    flux = flux_add(param['fcen'], param['df'], param['nfreq'], unit)
    out_path = path.join(path.abspath('.'), param['name'])

    makedirs(out_path, mode=0o777, exist_ok=True)

    no_geom_data = sim_no_geom(cz, param['res'], param['dpml'], src, flux, unit, param['decay'], out_path)

    wl = no_geom_data['wl']
    inc = no_geom_data['incident_pow']
    fl_date = no_geom_data['flux_data']

    scat_pow = sim_with_geom(cz, param['res'], geom, param['dpml'], src, flux, unit, out_path, param['decay'],
                             param['rt'], fl_date)
    abs_pow = sim_with_geom(cz, param['res'], geom, param['dpml'], src, flux, unit, out_path, param['decay'],
                            param['rt'], fl_date,
                            False)

    scat_cross = np.asarray(scat_pow / inc)
    abs_cross = np.asarray(abs_pow / inc)

    ext_cross = np.asarray(scat_cross + abs_cross)
    wl = np.asarray(wl)

    spectrum_date = np.array([wl, scat_cross, abs_cross, ext_cross]).transpose()

    np.savetxt(fname=path.join(out_path, 'spectrums.txt'),
               X=spectrum_date,
               header='unit length(um): 0.1     ' + 'rad: ' + str(param['rad1']) +
                      '\n\nwl   scattering    absorption    extintion\n\n',
               delimiter='    ',
               newline='\n')

    plt.figure()
    plt.plot(wl, 100 * scat_cross, 'bo-', label='scattering')
    plt.plot(wl, 100 * abs_cross, 'ro-', label='absorption')
    plt.plot(wl, 100 * ext_cross, 'go-', label='extinction')
    plt.xlabel("wavelength (μm)")
    plt.ylabel("cross-section (nm)")
    plt.legend(loc="upper right")
    plt.savefig(path.join(out_path, 'abs_scat_ext.png'))
    plt.close()


initialize()
