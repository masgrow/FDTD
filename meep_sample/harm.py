from meep import Vector3, Sphere, Source, GaussianSource, Ez, Ey, Ex, Simulation, PML, after_sources, Harminv


def harm_run(resolution, radius, pml, material, fcen, df, remote, time):
    def s_xyz():
        return 2 * (radius + 0.5 * radius + pml)

    def cell():
        return Vector3(s_xyz(), s_xyz(), 0)

    def particle():
        return Sphere(radius, material=material)

    def source():
        return Source(GaussianSource(frequency=fcen, fwidth=df),
                      component=Ez,
                      center=Vector3(radius + remote, 0, 0))

    def sim():
        return Simulation(cell_size=cell(),
                          geometry=[particle()],
                          sources=[source()],
                          boundary_layers=[PML(pml)],
                          resolution=resolution)

    def mod(component):
        h = Harminv(c=component, pt=Vector3(radius + remote, 0, 0), fcen=fcen, df=df)
        sim().run(after_sources(h),
                  until_after_sources=time)
        return h.modes

    def out():
        #ex = mod(Ex)
        #ey = mod(Ey)
        ez = mod(Ez)
        tup = ez
        return tup

    return out()
