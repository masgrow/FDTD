from meep import Sphere, Source, GaussianSource, Ez, Vector3


def nanoparticle(radius, material):
    return [Sphere(radius, material=material)]


def source(wavelength, width, remote):
    return Source(GaussianSource(frequency=1 / wavelength, width=width), Ez, center=Vector3(remote, 0, 0))


def cell(radius, pml):

    def sxyz(radius, pml):
        return 2*(radius+0.5*radius+pml)

    return Vector3(sxyz(radius, pml), sxyz(radius, pml), sxyz(radius, pml))
