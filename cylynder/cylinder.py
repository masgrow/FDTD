from meep import Vector3, Cylinder, inf, LorentzianSusceptibility, Medium, Volume, Source, GaussianSource, Ex, \
    Simulation, PML, FluxRegion, get_flux_freqs, get_fluxes, at_every, stop_when_fields_decayed, Animate2D, \
    in_volume, Mirror, X
from meep.materials import Si
import argparse
import matplotlib.pyplot as plt
import numpy as np
from os import path


def material(material_name):
    def custom_ag():
        ag_sus = [LorentzianSusceptibility(frequency=1e-20, gamma=0.0038715, sigma=4.4625e+39),
                  LorentzianSusceptibility(frequency=0.065815, gamma=0.31343, sigma=7.9247),
                  LorentzianSusceptibility(frequency=0.36142, gamma=0.036456, sigma=0.50133),
                  LorentzianSusceptibility(frequency=0.66017, gamma=0.0052426, sigma=0.013329),
                  LorentzianSusceptibility(frequency=0.73259, gamma=0.07388, sigma=0.82655),
                  LorentzianSusceptibility(frequency=1.6365, gamma=0.19511, sigma=1.1133)]
        return Medium(epsilon=1.0001, E_susceptibilities=ag_sus)

    material_dict = {'custom_ag': custom_ag(), 'meep': Si}
    return material_dict[material_name]


def geometry(**kwargs):
    def sx(leng):
        return leng * kwargs['rad']

    def cell():
        return Vector3(sx(8) + 2 * kwargs['dpml'],
                       sx(8) + 2 * kwargs['dpml'])

    def cylinder():
        if kwargs['geom']:
            return [Cylinder(radius=kwargs['rad'], height=inf,
                             center=Vector3(0, 0),
                             material=Si),
                    Cylinder(radius=kwargs['rad2'], height=inf,
                             center=Vector3(0, 0),
                             material=material(kwargs['mat']))]
        elif not kwargs['geom']:
            return []

    def source_volume():
        return Volume(center=(Vector3(0, sx(4))),
                      size=Vector3(sx(8), 0))

    def flux_reg():
        return dict(top=FluxRegion(center=Vector3(0, sx(2)), size=Vector3(sx(4), 0)),
                    bottom=FluxRegion(center=Vector3(0, sx(-2)), size=Vector3(sx(4), 0)),
                    left=FluxRegion(center=Vector3(sx(-2), 0), size=Vector3(0, sx(4))),
                    right=FluxRegion(center=Vector3(sx(2), 0), size=Vector3(0, sx(4))))

    def surf_slice():
        return Vector3(sx(8), sx(8))

    return dict(cell=cell(), cylinder=cylinder(), source=source_volume(), flux=flux_reg(), slice=surf_slice())


def source(**kwargs):
    return [Source(GaussianSource(frequency=kwargs['fcen'],
                                  fwidth=kwargs['df'],
                                  is_integrated=True),
                   component=Ex,
                   center=geometry(**kwargs)['source'].center,
                   size=geometry(**kwargs)['source'].size)]


def sim(**kwargs):
    return Simulation(cell_size=geometry(**kwargs)['cell'],
                      resolution=(kwargs['res']),
                      geometry=geometry(**kwargs)['cylinder'],
                      boundary_layers=[PML(kwargs['dpml'])],
                      sources=source(**kwargs),
                      output_single_precision=True,
                      eps_averaging=False,
                      force_complex_fields=False,
                      Courant=0.25,
                      symmetries=[Mirror(direction=X, phase=-1)])


def flux(sim, **kwargs):
    return dict(top=sim.add_flux(kwargs['fcen'],
                                 kwargs['df'],
                                 kwargs['nfreq'],
                                 geometry(**kwargs)['flux']['top']),
                bottom=sim.add_flux(kwargs['fcen'],
                                    kwargs['df'],
                                    kwargs['nfreq'],
                                    geometry(**kwargs)['flux']['bottom']),
                left=sim.add_flux(kwargs['fcen'],
                                  kwargs['df'],
                                  kwargs['nfreq'],
                                  geometry(**kwargs)['flux']['left']),
                right=sim.add_flux(kwargs['fcen'],
                                   kwargs['df'],
                                   kwargs['nfreq'],
                                   geometry(**kwargs)['flux']['right']))


def flux_data(sim, flux_obj):
    return dict(top=sim.get_flux_data(flux_obj['top']),
                bottom=sim.get_flux_data(flux_obj['bottom']),
                left=sim.get_flux_data(flux_obj['left']),
                right=sim.get_flux_data(flux_obj['right']))


def flux_get(fl):
    return dict(top=get_fluxes(fl['top']),
                bottom=get_fluxes(fl['bottom']),
                left=get_fluxes(fl['left']),
                right=get_fluxes(fl['right']))


def out():
    sim_no_geom = sim(**app_dict(arg, ['geom'], [False]))
    flux_no_geom = flux(sim_no_geom, **arg)
    incident = sim_no_geom.add_flux(arg['fcen'], arg['df'], arg['nfreq'], FluxRegion(center=Vector3(0, -4 * arg['rad']),
                                                                                     size=Vector3(4 * arg['rad'], 0)))

    plt.figure()
    sim_no_geom.plot2D(boundary_parameters={'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y',
                                            'edgecolor': 'b', 'alpha': 0.3},
                       eps_parameters={'cmap': 'gray'})
    plt.savefig((path.join(path.abspath('.'), 'sim_no_geom.png')))
    plt.close()

    sim_no_geom.run(until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, -4 * arg['rad']), 1e-6))

    box_top = sim_no_geom.get_flux_data(flux_no_geom['top'])
    box_bottom = sim_no_geom.get_flux_data(flux_no_geom['bottom'])
    box_left = sim_no_geom.get_flux_data(flux_no_geom['left'])
    box_right = sim_no_geom.get_flux_data(flux_no_geom['right'])

    freq = np.asarray(get_flux_freqs(flux_no_geom['top']))

    inc = np.absolute(np.asarray(get_fluxes(incident)))
    incident_pow = inc / (4 * arg['rad'])

    sim_no_geom.reset_meep()

    sim_with_geom = sim(**(app_dict(arg, ['geom'], [True])))
    flux_with_geom = flux(sim_with_geom, **arg)

    sim_with_geom.load_minus_flux_data(flux_with_geom['top'], box_top)
    sim_with_geom.load_minus_flux_data(flux_with_geom['bottom'], box_bottom)
    sim_with_geom.load_minus_flux_data(flux_with_geom['left'], box_left)
    sim_with_geom.load_minus_flux_data(flux_with_geom['right'], box_right)

    sim_with_geom.run(until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, -4 * arg['rad']), 1e-6))

    box_xy_flux = flux_get(flux_with_geom)

    scat_pow = np.absolute(-np.asarray(box_xy_flux['top']) + np.asarray(box_xy_flux['bottom']) + \
                           np.asarray(box_xy_flux['left']) - np.asarray(box_xy_flux['right']))

    sim_with_geom.reset_meep()

    sim_with_geom = sim(**(app_dict(arg, ['geom'], [True])))
    flux_with_geom = flux(sim_with_geom, **arg)

    plt.figure()
    sim_with_geom.plot2D(boundary_parameters={'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y',
                                              'edgecolor': 'b', 'alpha': 0.3},
                         eps_parameters={'cmap': 'gray'})
    plt.savefig((path.join(path.abspath('.'), 'sim_with_geom.png')))
    plt.close()

    animate = Animate2D(sim_with_geom,
                        fields=Ex,
                        realtime=False,
                        field_parameters={'alpha': 0.8, 'cmap': 'RdBu', 'interpolation': 'spline36'},
                        eps_parameters={'cmap': 'binary'})

    sim_with_geom.run(at_every(0.2, in_volume(Volume(size=Vector3(4 * arg['rad'], 4 * arg['rad']),
                                                     center=Vector3(0, 0)),
                                              animate)),
                      until_after_sources=stop_when_fields_decayed(1, Ex, Vector3(0, -4 * arg['rad']), 1e-6))

    animate.to_mp4(fps=12, filename=path.join(path.abspath('.'), 'ex_anim.mp4'))

    abs_flux = flux_get(flux_with_geom)

    abs_pow = -np.asarray(abs_flux['top']) + np.asarray(abs_flux['bottom']) + \
              np.asarray(abs_flux['left']) - np.asarray(abs_flux['right'])

    wave_length = np.divide(100, freq, dtype=np.float)

    return dict(scat=scat_pow,
                abs=abs_pow,
                wl=wave_length,
                incident=incident_pow)


def app_dict(sdict, key, value):
    for n in range(len(key)):
        sdict.update({key[n]: value[n]})
    return sdict


def parser():
    parse = argparse.ArgumentParser('cylynder')
    parse.add_argument('-res', metavar='resolution', type=int, default=25,
                       help='')
    parse.add_argument('-rad', metavar='radius', type=float, default=0.25,
                       help='')
    parse.add_argument('-rad2', metavar='tuberad', type=float, default=0.05,
                       help='')
    parse.add_argument('-mat', metavar='material', type=str, default='custom_ag',
                       choices=['custom_ag', 'meep'],
                       help='')
    parse.add_argument('-fcen', metavar='freqency', type=float, default=0.3,
                       help='')
    parse.add_argument('-df', metavar='fwidth', type=float, default=0.3,
                       help='')
    parse.add_argument('-dpml', metavar='dpml', type=float, default=1,
                       help='')
    parse.add_argument('-nfreq', metavar='nfreq', type=int, default=60,
                       help='')
    return parse.parse_args()


arg = vars(parser())

donut = out()

scat_cross = np.asarray(donut['scat'] / donut['incident'])
abs_cross = np.asarray(donut['abs'] / donut['incident'])
ext_cross = np.asarray(scat_cross + abs_cross)
wl = np.asarray(donut['wl'])

spectrum_date = np.array([wl, scat_cross, abs_cross, ext_cross]).transpose()

np.savetxt(fname=path.join(path.abspath('.'), 'spectrums.txt'),
           X=spectrum_date,
           header='unit length(um): 0.1     ' + 'rad: ' + str(arg['rad']) + '\n\nwl   scattering    absorption    '
                                                                            'extintion\n\n',
           delimiter='    ',
           newline='\n')

plt.figure()
plt.plot(wl, 100 * scat_cross, 'bo-', label='scattering')
plt.plot(wl, 100 * abs_cross, 'ro-', label='absorption')
plt.plot(wl, 100 * ext_cross, 'go-', label='extinction')
plt.xlabel("wavelength (μm)")
plt.ylabel("cross-section (nm)")
plt.legend(loc="upper right")
plt.savefig(path.join(path.abspath('.'), 'abs_scat_ext.png'))
plt.close()
