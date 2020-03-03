from meep import Vector3, Sphere, Source, GaussianSource, Ez, Ey, Ex, Dielectric, Simulation, PML, at_every, \
    at_beginning, at_end
import numpy as np


def sim_run(resolution, radius, pml, material, fcen, df, remote, time, dt, path_e, out, u):
    def s_xyz():
        return 2 * (radius + 0.5 * radius + pml)

    def cell():
        return Vector3(s_xyz(), s_xyz(), s_xyz())

    def particle():
        return Sphere(radius, material=material)

    def source():
        return Source(GaussianSource(frequency=fcen, fwidth=df),
                      component=Ez,
                      center=Vector3(radius + remote, 0, 0))

    def sim():
        simulation = Simulation(cell_size=cell(),
                                geometry=[particle()],
                                sources=[source()],
                                boundary_layers=[PML(pml)],
                                resolution=resolution)
        return simulation

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

            xy()
            xz()
            yz()
            return print('---slice eps---')

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
            return print('slice E comp\n' + ' time: ' + str(sim.meep_time()))

        if out == 'out_eps':
            eps = list()
            init = sim().init_sim()
            slice_dielectric(init)
            np.savez(path_e + 'eps', eps_xy=eps[0], eps_xz=eps[1], eps_yz=eps[2])
            print('---eps saved---')

        elif out == 'sim':
            eps = list()
            ex_comp = list()
            ey_comp = list()
            ez_comp = list()

            sim().run(at_beginning(slice_dielectric, slice_xy),
                      at_every(dt, slice_xy),
                      until_after_sources=time)
            np.savez(path_e + 'eps', eps_xy=eps[0], eps_xz=eps[1], eps_yz=eps[2])
            np.savez(path_e + 'ex', ex=ex_comp)
            np.savez(path_e + 'ey', ey=ey_comp)
            np.savez(path_e + 'ez', ez=ez_comp)

            return print('---E saved---')
        elif out == 'sim_res':
            eps = list()
            ex_comp = list()
            ey_comp = list()
            ez_comp = list()

            sim().run(at_beginning(slice_dielectric, slice_xy),
                      at_every((u/fcen)/20, slice_xy),
                      until_after_sources=(u/fcen))
            np.savez(path_e + 'eps', eps_xy=eps[0], eps_xz=eps[1], eps_yz=eps[2])
            np.savez(path_e + 'ex', ex=ex_comp)
            np.savez(path_e + 'ey', ey=ey_comp)
            np.savez(path_e + 'ez', ez=ez_comp)

            return print('---E saved---')

    start()
