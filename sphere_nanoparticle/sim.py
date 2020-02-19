from meep import Sphere, Source, GaussianSource, Ez, Vector3, Simulation, PML, Harminv


def create(res, radius, material, wavelength, width, remote, pml):
    def nanoparticle(radius, material):
        return [Sphere(radius, material=material)]

    def source(wavelength, width, remote):
        return [Source(GaussianSource(frequency=1 / wavelength, width=width), Ez, center=Vector3(remote, 0, 0))]

    def cell(radius, pml):
        def sxyz(radius, pml):
            return 2 * (radius + 0.5 * radius + pml)

        return Vector3(sxyz(radius, pml), sxyz(radius, pml), sxyz(radius, pml))

    def sim(res, radius, material, wavelength, width, remote, pml):
        return Simulation(cell_size=cell(radius, pml),
                          resolution=res,
                          boundary_layers=[PML(pml)],
                          geometry=nanoparticle(radius, material),
                          sources=source(wavelength, width, remote))

    return sim(res, radius, material, wavelength, width, remote, pml)


def harm(sim):
    return sim.run(until_after_sources=Harminv())