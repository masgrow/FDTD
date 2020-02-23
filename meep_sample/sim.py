from meep import Vector3, Sphere, Source, GaussianSource, Ez, Ey, Ex, Dielectric, Simulation, PML, at_every, \
    at_beginning
import numpy as np


def sim_run(resolution, radius, pml, material, wavelength, width, remote, time, dt, path_e):
    def s_xyz():
        return 2 * (radius + 0.5 * radius + pml)

    def cell():
        return Vector3(s_xyz(), s_xyz(), s_xyz())

    def particle():
        return Sphere(radius, material=material)

    def source():
        return Source(GaussianSource(frequency=1 / wavelength, width=width),
                      component=Ez,
                      center=Vector3(radius + remote, 0, 0))

    def sim():
        return Simulation(cell_size=cell(),
                          geometry=[particle()],
                          sources=[source()],
                          boundary_layers=[PML(pml)],
                          resolution=resolution)

    def start():
        def slice_dielectric(sim):
            def xy():
                return eps.append(sim.get_array(component=Dielectric,
                                                size=Vector3(s_xyz(), s_xyz(), 0),
                                                center=Vector3(0, 0, 0)))

            def xz():
                return eps.append(sim.get_array(component=Dielectric,
                                                size=Vector3(s_xyz(), 0, s_xyz()),
                                                center=Vector3(0, 0, 0)))

            def yz():
                return eps.append(sim.get_array(component=Dielectric,
                                                size=Vector3(0, s_xyz(), s_xyz()),
                                                center=Vector3(0, 0, 0)))

        def slice_xy(sim):
            def array_ex():
                return ex_comp.append(sim.get_array(component=Ex,
                                                    size=Vector3(s_xyz(), s_xyz(), 0),
                                                    center=Vector3(0, 0, 0)))

            def array_ey():
                return ey_comp.append(sim.get_array(component=Ey,
                                                    size=Vector3(s_xyz(), s_xyz(), 0),
                                                    center=Vector3(0, 0, 0)))

            def array_ez():
                return ez_comp.append(sim.get_array(component=Ez,
                                                    size=Vector3(s_xyz(), s_xyz(), 0),
                                                    center=Vector3(0, 0, 0)))

            array_ex()
            array_ey()
            array_ez()
            return sim.print_times()

        eps = list()
        ex_comp = list()
        ey_comp = list()
        ez_comp = list()

        sim().run(at_beginning(slice_dielectric, slice_xy),
                  at_every(dt, slice_xy),
                  until_after_sources=time)
        np.savez(path_e + 'eps', eps)
        np.savez(path_e + 'ex', ex_comp)
        np.savez(path_e + 'ey', ey_comp)
        np.savez(path_e + 'ez', ez_comp)

    start()
