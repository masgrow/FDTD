import argparse
import custom_materials

parser = argparse.ArgumentParser('FDTD calculations for some nanoparticles')
parser.add_argument('--u', metavar='unit', type=float, default=0.1,
                    help='Unit of length a (default: 0.1 um), use unit length in um')
parser.add_argument('--res', metavar='resolution', type=int, default=50,
                    help='Resolution pixel/a (default: 500 pixel/um)')
parser.add_argument('--rad', metavar='radius', type=float, default=0.5,
                    help='Radius nanoparticle a*rad (default: 0.05 um')
parser.add_argument('--wl', metavar='wavelength', type=float, default=5,
                    help='Source wavelength wl/a (default: 0.5 um)')
parser.add_argument('--wid', metavar='width', type=float, default=0.5,
                    help='The width omega used in the Gaussian')
parser.add_argument('--mod', metavar='mode', type=str, default='sim',
                    help='Harminv (harm) or start simulation (sim) (default: sim)')
parser.add_argument('--mat', metavar='material', choices=custom_materials.material_lib_name(),
                    help='material nanoparticle (default: custom_ag)')
args = parser.parse_args()
