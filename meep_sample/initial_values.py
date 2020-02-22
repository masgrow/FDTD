import argparse


def init_values(material_lib):
    parser = argparse.ArgumentParser('FDTD calculations for some nanoparticles')
    parser.add_argument('--u', metavar='unit', type=float, default=0.1,
                        help='Unit of length a (default: 0.1 um), use unit length in um')
    parser.add_argument('--res', metavar='resolution', type=int, default=50,
                        help='Resolution pixel/a (default: 500 pixel/um)')
    parser.add_argument('--rad', metavar='radius', type=float, default=0.3,
                        help='Radius nanoparticle a*rad (default: 0.03 um')
    parser.add_argument('--wl', metavar='wavelength', type=float, default=3.9,
                        help='Source wavelength wl/a (default: 0.39 um)')
    parser.add_argument('--wid', metavar='width', type=float, default=0.7,
                        help='The width omega used in the Gaussian (default: 0.7')
    parser.add_argument('--rem', metavar='remote', type=float, default=0.01,
                        help='Remoteness of a source from a particle (default: 0.001 um')
    parser.add_argument('--mod', metavar='mode', type=str, default='sim',
                        help='Harminv (harm) or start simulation (sim) (default: sim)')
    parser.add_argument('--mat', metavar='material', type=str, choices=material_lib, default='custom_ag',
                        help='material nanoparticle (default: custom_ag)')
    parser.add_argument('--pml', metavar='PML', type=float, default=0.5,
                        help='PML thickness (default: 0.05 um')
    parser.add_argument('--t', metavar='time', type=float, default=50,
                        help='Simulation time (default: 50)')
    parser.add_argument('--n', metavar='name', type=str, default='nanoparticle',
                        help='Name for output data and folder (default: nanoparticle')
    parser.add_argument('--dt', metavar='dtime', type=float, default=10.0,
                        help='Time between component output E (default: 10.0')
    return parser.parse_args()
