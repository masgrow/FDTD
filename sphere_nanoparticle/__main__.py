import initial_values as iv
import custom_materials as cm
import sim
import datetime


def modes_output(modes, material):
    f = open('sphere_nanoparticle/output/' + arg().n + '_' + str(datetime.date) + 'modes', 'a')

    def list_to_str(modes):
        f.write('Date:   ' + datetime.datetime.now().__str__())
        f.write('   Material:   ' + material)
        f.write('   wavelength:  ' + arg().wl.__str__())
        f.write(' width:   ' + arg().wid.__str__())
        f.write('\n' + modes.__str__() + '\n ')
        f.close()

    return list_to_str(modes)


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
