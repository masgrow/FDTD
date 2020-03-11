from meep import Vector3, Cylinder, inf, LorentzianSusceptibility, Medium, Volume, Source, GaussianSource, Ex, \
    Simulation, PML
import argparse


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
    def sx_length(leng):
        return leng * kwargs['rad']

    def cell():
        return Vector3(sx_length(8) + 2 * kwargs['dpml'],
                       sx_length(8) + 2 * kwargs['dpml'])

    def cylinder():
        if kwargs['geom']:
            return Cylinder(radius=kwargs['rad'], height=inf,
                            center=Vector3(0, 0),
                            material=material(kwargs['mat']))
        else:
            return []

    def source_volume():
        return Volume(center=(Vector3(0, sx_length(4))),
                      size=Vector3(sx_length(8), 0))

    def flux_volume():
        return dict(top=Volume(center=Vector3(0, 2), size=Vector3(4, 0)),
                    bottom=Volume(center=Vector3(0, -2), size=Vector3(4, 0)),
                    left=Volume(center=Vector3(-2, 0), size=Vector3(0, 4)),
                    rigth=Volume(center=Vector3(2, 0), size=Vector3(0, 4)))

    return dict(cell=cell(), cylinder=cylinder(), source=source_volume(), monitor=flux_volume())


def source(**kwargs):
    return Source(GaussianSource(frequency=kwargs['fcen'],
                                 fwidth=kwargs['df']),
                  component=Ex,
                  center=geometry(**kwargs)['source'].center,
                  size=geometry(**kwargs)['source'].size)


def sim(**kwargs):
    return Simulation(cell_size=geometry(**kwargs)['cell'],
                      resolution=(kwargs['res']),
                      geometry=geometry(**kwargs)['cylinder'],
                      boundary_layers=[PML(kwargs['dpml'])],
                      sources=source(**kwargs))


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
    return parse.parse_args()


arg = parser()
sim(res=arg.res, rad=arg.rad, mat=arg.mat, fcen=arg.fcen, df=arg.df, dpml=arg.dpml, geom=False)
