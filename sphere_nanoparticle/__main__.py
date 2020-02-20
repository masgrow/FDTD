import initial_values as iv
import custom_materials as cm
import sim
import datetime


def modes_output(modes, material):
    def list_to_str(modes):
        return 'Date:   ' + datetime.datetime.now().__str__() + '   Material:   ' + material + '   wavelength:  ' \
               + arg().wl.__str__() + ' width:   ' + arg().wid.__str__() + '\n' + modes.__str__() + '\n '

    return open('sphere_nanoparticle/output/modes', 'a').write(list_to_str(modes))


def arg():
    return iv.init_values(cm.material_lib())


if arg().mod == 'harm':
    modes_output(sim.mod(
        sim.create(arg().res, arg().rad, cm.material_lib_dict(arg().mat), arg().wl, arg().wid, arg().rem,
                   arg().pml),
        arg().rem, arg().rad, arg().wl, arg().wid, arg().t),
        arg().mat)

elif arg().mod == 'sim':
    simulation = sim.create(arg().res, arg().rad, cm.material_lib_dict(arg().mat), arg().wl, arg().wid, arg().rem,
                            arg().pml)
    sim.output_dielectric(simulation,
                          arg().rad, arg().pml)
    simulation.run(sim.output_ez_step(simulation, arg().rad, arg().pml), until=10)
