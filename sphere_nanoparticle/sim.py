from meep import Sphere, Source, GaussianSource, Ez, Ex, Ey, Vector3, Simulation, PML, Harminv, after_sources, \
    Dielectric, at_every
import numpy as np

sxyz = lambda radius, pml: 2 * (radius + 0.5 * radius + pml)


def create(res, radius, material, wavelength, width, remote, pml):
    def cell(radius, pml):
        return Vector3(sxyz(radius, pml), sxyz(radius, pml), sxyz(radius, pml))

    def nanoparticle(radius, material):
        return [Sphere(radius, material=material)]

    def source(wavelength, width, remote):
        return [
            Source(GaussianSource(frequency=1 / wavelength, width=width), Ez, center=Vector3(remote + radius, 0, 0))]

    return Simulation(cell_size=cell(radius, pml),
                      resolution=res,
                      boundary_layers=[PML(pml)],
                      geometry=nanoparticle(radius, material),
                      sources=source(wavelength, width, remote))


def mod(sim, remote, radius, wavelength, width, time):
    h = Harminv(Ez, Vector3(remote + radius, 0, 0), fcen=1 / wavelength, df=width)
    sim.run(after_sources(h),
            until_after_sources=time)
    return h.modes


def output_dielectric(sim, radius, pml, path):
    sim.init_sim()
    eps = sim.get_array(component=Dielectric, center=Vector3(x=0, y=0),
                        size=Vector3(sxyz(radius, pml), sxyz(radius, pml)))
    return np.save(path, eps)


def output_ez(sim, radius, pml, path_z):
    ez = sim.get_array(component=Ez, center=Vector3(x=0, y=0),
                       size=Vector3(sxyz(radius, pml), sxyz(radius, pml)))
    return np.save(path_z, ez)


def output_ey(sim, radius, pml, path_y):
    ey = sim.get_array(component=Ey, center=Vector3(x=0, y=0),
                       size=Vector3(sxyz(radius, pml), sxyz(radius, pml)))
    return np.save(path_y, ey)


def output_ex(sim, radius, pml, path_x):
    ex = sim.get_array(component=Ex, center=Vector3(x=0, y=0),
                       size=Vector3(sxyz(radius, pml), sxyz(radius, pml)))
    return np.save(path_x, ex)


def start(sim, time, dt, path_x, path_y, path_z, radius, pml):
    sim.run(at_every(dt, output_ez(sim, radius=radius, pml=pml, path_z=path_z),
                     output_ey(sim, radius=radius, pml=pml, path_y=path_y),
                     output_ex(sim, radius=radius, pml=pml, path_x=path_x)),
            until_after_sources=time)
