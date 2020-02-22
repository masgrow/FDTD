from meep import Vector3, Sphere, Source, GaussianSource, Ez, Ey, Ex, Simulation, PML, at_every, at_beginning


def sim_run(resolution, radius, pml, material, wavelength, width, remote, time, dt):
    def s_x_y_z():
        return 2 * (radius + 0.5 * radius + pml)

    def cell():
        return Vector3(s_x_y_z(), s_x_y_z(), s_x_y_z())

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
        sim_full = sim()
        sim_full.run(until=50)(at_beginning(lambda: print(start())),
                               at_every(dt, lambda: print(sim_full.meep_time())),
                               until_after_sources=time)
