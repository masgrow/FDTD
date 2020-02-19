import initial_values as iv
import custom_materials as cm
import sim
import datetime


def modes_output(modes, material):
    def list_to_str(modes):
        return '\nDate:   ' + datetime.datetime.now().__str__() + '   Material:   ' \
               + material + '\n' + modes.__str__()

    def op():
        return open('sphere_nanoparticle/output/modes', 'a')

    return op().write(list_to_str(modes))


def arg():
    return iv.init_values(cm.material_lib())


if arg().mod == 'harm':
    modes_output(sim.mod(
        sim.create(arg().res, arg().rad, cm.material_lib_dict(arg().mat), arg().wl, arg().wid, arg().rem, arg().pml),
        arg().rem,
        arg().rad,
        arg().wl,
        arg().wid,
        arg().t),
        arg().mat)
