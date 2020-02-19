import initial_values as iv
import custom_materials as cm
import sim


def mote_output(modes):
    return 0


def arg():
    return iv.init_values(cm.material_lib())


if arg().mod == 'harm':
    sim.mod(
        sim.create(arg().res, arg().rad, cm.material_lib_dict(arg().mat), arg().wl, arg().wid, arg().rem, arg().pml),
        arg().rem,
        arg().rad,
        arg().wl,
        arg().wid,
        arg().t)
