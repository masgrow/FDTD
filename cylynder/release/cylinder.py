from meep import Vector3, Cylinder, inf, LorentzianSusceptibility, Medium, Volume, Source, GaussianSource, Ex, \
    Simulation, PML, FluxRegion, get_flux_freqs, get_fluxes, at_every, stop_when_fields_decayed, Animate2D, \
    in_volume, Mirror, X
import argparse
import matplotlib.pyplot as plt
import numpy as np
from os import path, mkdir


def material(material_name):
    def custom_ag():
        ag_sus = [LorentzianSusceptibility(frequency=1e-20, gamma=0.0038715, sigma=4.4625e+39),
                  LorentzianSusceptibility(frequency=0.065815, gamma=0.31343, sigma=7.9247),
                  LorentzianSusceptibility(frequency=0.36142, gamma=0.036456, sigma=0.50133),
                  LorentzianSusceptibility(frequency=0.66017, gamma=0.0052426, sigma=0.013329),
                  LorentzianSusceptibility(frequency=0.73259, gamma=0.07388, sigma=0.82655),
                  LorentzianSusceptibility(frequency=1.6365, gamma=0.19511, sigma=1.1133)]
        return Medium(epsilon=1.0001, E_susceptibilities=ag_sus)

    material_dict = {'custom_ag': custom_ag()}
    return material_dict[material_name]


def parser():
    parse = argparse.ArgumentParser('cylynder')
    parse.add_argument('-res', metavar='resolution', type=int, default=25,
                       help='')
    parse.add_argument('-rad1', metavar='radius', type=float, default=0.25,
                       help='')
    parse.add_argument('-rad2', metavar='tuberad', type=float, default=0.0,
                       help='')
    parse.add_argument('-mat1', metavar='material1', type=str, default='custom_ag',
                       choices=['custom_ag'],
                       help='')
    parse.add_argument('-mat2', metavar='material2', type=str, default='custom_ag',
                       choices=['custom_ag'],
                       help='')
    parse.add_argument('-fcen', metavar='freqency', type=float, default=0.3,
                       help='')
    parse.add_argument('-df', metavar='fwidth', type=float, default=0.3,
                       help='')
    parse.add_argument('-dpml', metavar='dpml', type=float, default=1,
                       help='')
    parse.add_argument('-nfreq', metavar='nfreq', type=int, default=60,
                       help='')
    parse.add_argument('-name', metavar='outpath', type=str, default='rad_25_Ag_full',
                       help='')
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


def source(fcen, df, u):
    return [Source(GaussianSource(frequency=fcen, width=df), Ex,
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


def sim_no_geom(cell_size, resolution, dpml, sources, fl, u, out_path):

    sim = simulation(cell_size, resolution, [], dpml, sources)

    top = fl(sim, 0, 2, 4, 0)
    bottom = fl(sim, 0, -2, 4, 0)
    left = fl(sim, -2, 0, 0, 4)
    right = fl(sim, 2, 0, 0, 4)
    incident = fl(sim, 0, -4, 4, 0)

    plot(sim, 'no_geom', out_path)

    sim.run(until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, u(-4)), 1e-6))

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


def sim_with_geom(cell_size, resolution, geom, dpml, sources, fl, u, out_path, fl_data=None, scat=True):

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

        sim.run(until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, u(-4)), 1e-6))

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

        sim.run(at_every(0.2, in_volume(Volume(size=Vector3(u(4), u(4)), center=Vector3(0, 0)), animate)),
                until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, u(-4)), 1e-6))

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
    src = source(param['fcen'], param['df'], unit)
    cz = cell(unit, param['dpml'])
    flux = flux_add(param['fcen'], param['df'], param['nfreq'], unit)
    out_path = path.join(path.abspath('.'), param['name'])

    if not path.exists(out_path):
        mkdir(out_path)

    no_geom_data = sim_no_geom(cz, param['res'], param['dpml'], src, flux, unit, out_path)

    wl = no_geom_data['wl']
    inc = no_geom_data['incident_pow']
    fl_date = no_geom_data['flux_data']

    scat_pow = sim_with_geom(cz, param['res'], geom, param['dpml'], src, flux, unit, out_path, fl_date)
    abs_pow = sim_with_geom(cz, param['res'], geom, param['dpml'], src, flux, unit, out_path, fl_date, False)

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
