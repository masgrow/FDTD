import initial_values as iv
import custom_materials as cm
import sim
import datetime
from os import makedirs


def output_path(name):
    path = 'sphere_nanoparticle/output/' + arg().n + name
    return path


def create_output_path(path):
    makedirs(path, mode=0o777, exist_ok=True)


def modes_output(modes, material):
    path = output_path('/modes')
    f = open(path, 'a')

    def list_to_str(modes):
        f.write('Date:   ' + datetime.datetime.now().__str__())
        f.write('   material:   ' + material)
        f.write('   wavelength:  ' + arg().wl.__str__())
        f.write('   width:   ' + arg().wid.__str__())
        f.write('   resolution:    ' + arg().res.__str__())
        f.write('   time:   ' + arg().t.__str__())
        f.write('\n' + modes.__str__() + '\n\n')
        f.close()

    return list_to_str(modes)


def arg():
    return iv.init_values(cm.material_lib())


create_output_path(output_path(''))

if arg().mod == 'harm':
    modes_output(sim.mod(
        sim.create(arg().res, arg().rad, cm.material_lib_dict(arg().mat), arg().wl, arg().wid, arg().rem,
                   arg().pml),
        arg().rem, arg().rad, arg().wl, arg().wid, arg().t),
        arg().mat)

elif arg().mod == 'sim':
    simulation = sim.create(arg().res, arg().rad, cm.material_lib_dict(arg().mat), arg().wl, arg().wid, arg().rem,
                            arg().pml)
    sim.output_dielectric(simulation, arg().rad, arg().pml, output_path('/eps'))
    create_output_path(output_path('/ez'))
    create_output_path(output_path('/ey'))
    create_output_path(output_path('/ex'))
    sim.start(simulation, arg().t, arg().dt, output_path('/ez/ez_'),
              arg().rad, arg().pml)
