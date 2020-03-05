import argparse


def init_values(material_lib):
    parser = argparse.ArgumentParser('FDTD calculations for some nanoparticles')
    parser.add_argument('--u', metavar='unit', type=float, default=0.01,
                        help='Unit of length a (default: 0.1 um), use unit length in um '
                             '(for materials from meep library)')
    parser.add_argument('--res', metavar='resolution', type=int, default=50,
                        help='Resolution pixel/a (default: 500 pixel/um)')
    parser.add_argument('--rad', metavar='radius', type=float, default=1,
                        help='Radius nanoparticle a*rad (default:  20 nm')
    parser.add_argument('--fcen', metavar='frequency', type=float, default=0.1,
                        help='The center frequency f (c/distance or ω in units of 2πc/distance) (default: 0,256410256)')
    parser.add_argument('--df', metavar='fwidth', type=float, default=10,
                        help='fwidth: 1/width, the width omega used in the Gaussian (default: 0.1)')
    parser.add_argument('--rem', metavar='remote', type=float, default=0.01,
                        help='Remoteness of a source from a particle (default: 1 nm)')
    parser.add_argument('--out', metavar='output', type=str, choices=['sim', 'harm', 'out_eps', 'sim_res',
                                                                      'ez_xy_png', 'ey_xy_png', 'ex_xy_png', 'eps_png'],
                        default='sim',
                        help='Harminv (harm)'
                             'start simulation (sim) (default: sim)'
                             'Output Ez in xy plane (gif_ez_xy)')
    parser.add_argument('--mat', metavar='material', type=str, choices=material_lib, default='custom_ag',
                        help='material nanoparticle (default: custom_ag)')
    parser.add_argument('--pml', metavar='PML', type=float, default=0.1,
                        help='PML thickness (default: 10 nm')
    parser.add_argument('--t', metavar='time', type=float, default=10,
                        help='Simulation time (default: 50)')
    parser.add_argument('--n', metavar='name', type=str, default='nanoparticle',
                        help='Name for output data and folder (default: nanoparticle')
    parser.add_argument('--dt', metavar='dtime', type=float, default=1.0,
                        help='Time between component output E (default: 10.0')
    return parser.parse_args()
