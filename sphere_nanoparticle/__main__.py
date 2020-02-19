import initial_values as iv
import custom_materials as cm
import sim


def arg():
    return iv.init_values(cm.material_lib())


sim.create(arg().res, arg().rad, cm.material_lib_dict(arg().mat), arg().wl, arg().wid, arg().rem, arg().pml)

