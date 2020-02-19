from meep import Sphere, Source, GaussianSource, Ez, Vector3, Simulation, PML, Harminv, after_sources, Dielectric

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


def init(sim, radius, pml):
    sim.init_sim()
    return sim.get_array(component=Dielectric, center=Vector3(x=0, y=0),
                         size=Vector3(sxyz(radius, pml),
                                      sxyz(radius, pml)))
