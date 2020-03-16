from meep import Vector3, Cylinder, inf, LorentzianSusceptibility, Medium, Volume, Source, GaussianSource, Ex, \
    Simulation, PML, FluxRegion, get_flux_freqs, get_fluxes, Dielectric, at_beginning, at_every
import argparse
import matplotlib.pyplot as plt
import numpy as np


def material(material_name):
    def custom_ag():
        ag_sus = [LorentzianSusceptibility(frequency=1e-20, gamma=0.0038715, sigma=4.4625e+39),
                  LorentzianSusceptibility(frequency=0.065815, gamma=0.31343, sigma=7.9247),
                  LorentzianSusceptibility(frequency=0.36142, gamma=0.036456, sigma=0.50133),
                  LorentzianSusceptibility(frequency=0.66017, gamma=0.0052426, sigma=0.013329),
                  LorentzianSusceptibility(frequency=0.73259, gamma=0.07388, sigma=0.82655),
                  LorentzianSusceptibility(frequency=1.6365, gamma=0.19511, sigma=1.1133)]
        return Medium(epsilon=1, E_susceptibilities=ag_sus)

    material_dict = {'custom_ag': custom_ag()}
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
                    rigth=FluxRegion(center=Vector3(sx(2), 0), size=Vector3(0, sx(4))))

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
                      sources=source(**kwargs))


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
                rigth=sim.add_flux(kwargs['fcen'],
                                   kwargs['df'],
                                   kwargs['nfreq'],
                                   geometry(**kwargs)['flux']['rigth']))


def flux_data(sim, flux_obj):
    return dict(top=sim.get_flux_data(flux_obj['top']),
                bottom=sim.get_flux_data(flux_obj['bottom']),
                left=sim.get_flux_data(flux_obj['left']),
                rigth=sim.get_flux_data(flux_obj['rigth']))


def flux_minus(sim, box_geom, box_no_geom):
    sim.load_minus_flux_data(box_geom['top'], box_no_geom['top'])
    sim.load_minus_flux_data(box_geom['bottom'], box_no_geom['bottom'])
    sim.load_minus_flux_data(box_geom['left'], box_no_geom['left'])
    sim.load_minus_flux_data(box_geom['rigth'], box_no_geom['rigth'])


def flux_get(fl):
    return dict(top=get_fluxes(fl['top']),
                bottom=get_fluxes(fl['bottom']),
                left=get_fluxes(fl['left']),
                rigth=get_fluxes(fl['rigth']))


def flux_out():
    def slice_xy(sim):
        def array_ex():
            return ex_comp.append(sim.get_array(component=Ex,
                                                size=geometry(**arg)['slice'],
                                                center=Vector3(0, 0)))

        array_ex()

    def slice_dielectric(sim):
        def xy():
            return eps.append(sim.get_array(component=Dielectric,
                                            size=geometry(**arg)['slice'],
                                            center=Vector3(0, 0)))

        xy()
        return print('---slice eps---')

    sim_no_geom = sim(**app_dict(arg, ['geom'], [False]))
    flux_no_geom = flux(sim_no_geom, **arg)
    sim_no_geom.run(until_after_sources=10)

    freq = get_flux_freqs(flux_no_geom['top'])
    box_xy_data = flux_data(sim_no_geom, flux_no_geom)
    incident = np.array(get_fluxes(flux_no_geom['top']))

    sim_no_geom.reset_meep()

    incident_pow = np.divide(incident, arg['rad'] * 4)

    sim_with_geom = sim(**(app_dict(arg, ['geom'], [True])))
    flux_with_geom = flux(sim_with_geom, **arg)

    flux_minus(sim_with_geom, flux_with_geom, box_xy_data)

    sim_with_geom.run(until_after_sources=0.25)

    box_xy_flux = flux_get(flux_with_geom)

    scat_pow = np.absolute((np.array(box_xy_flux['top']) - np.array(box_xy_flux['bottom']) +
                            np.array(box_xy_flux['left']) - np.array(box_xy_flux['rigth'])))

    sim_with_geom.reset_meep()

    eps = []
    ex_comp = []

    sim_with_geom = sim(**(app_dict(arg, ['geom'], [True])))
    flux_with_geom = flux(sim_with_geom, **arg)

    sim_with_geom.run(at_beginning(slice_dielectric, slice_xy),
                      at_every(0.4, slice_xy),
                      until_after_sources=0.25)

    abs_flux = flux_get(flux_with_geom)
    abs_pow = np.array(abs_flux['top']) - np.array(abs_flux['bottom']) + \
              np.array(abs_flux['left']) - np.array(abs_flux['rigth'])

    wave_length = np.power(freq * 100, -1, dtype=np.float)

    print(incident)
    print(incident_pow)

    return dict(scat=scat_pow, abs=abs_pow, wl=wave_length, incident=incident_pow)


def app_dict(sdict, key, value):
    for n in range(len(key)):
        sdict.update({key[n]: value[n]})
    return sdict


def parser():
    parse = argparse.ArgumentParser('cylynder')
    parse.add_argument('-res', metavar='resolution', type=int, default=50,
                       help='')
    parse.add_argument('-rad', metavar='radius', type=float, default=0.25,
                       help='')
    parse.add_argument('-mat', metavar='material', type=str, default='custom_ag',
                       choices=['custom_ag'],
                       help='')
    parse.add_argument('-fcen', metavar='freqency', type=float, default=0.175,
                       help='')
    parse.add_argument('-df', metavar='fwidth', type=float, default=0.15,
                       help='')
    parse.add_argument('-dpml', metavar='dpml', type=float, default=1,
                       help='')
    parse.add_argument('-nfreq', metavar='nfreq', type=int, default=100,
                       help='')
    return parse.parse_args()


arg = vars(parser())

out = flux_out()

scat_cross = np.divide(out['scat'], out['incident'])
abs_cross = np.divide(out['abs'], out['incident'])

wl = out['wl']

plt.figure()
plt.plot(wl.transpose, scat_cross, 'bo-', label='scattering')
plt.plot(wl.transpose, abs_cross, 'ro-', label='absorption')
plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="...")
plt.show()
