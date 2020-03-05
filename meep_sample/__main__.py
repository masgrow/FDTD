import initial_values as iv
import custom_materials as cm
import harm
import sim
import datetime
import visualisation
from os import makedirs, path

arg = iv.init_values(cm.material_lib())


def out_path(name):
    out = 'meep_sample/out/' + name
    return out


def directory(name):
    name_path = out_path(arg.n) + name
    if not path.exists(name_path):
        makedirs(name_path, mode=0o777, exist_ok=False)
    return name_path


if arg.out == 'harm':
    def modes_write(tup):
        f = open(out_path(arg.n + '/modes'), 'a')
        f.write('\n\n----start----')
        f.write('\n' + str(datetime.datetime.now()))
        f.write('\n Parameters::  radius: ' + str(arg.rad))
        f.write('   unit length: ' + str(arg.u))
        f.write('   material: ' + str(arg.mat))
        f.write('   fcen: ' + str(arg.fcen))
        f.write('   fwidth: ' + str(arg.df))
        f.write('   resolution: ' + str(arg.res))
        f.write('   time: ' + str(arg.t))
        f.write('\n Format::  frequency, imag. freq., Q, |amp|, amplitude, error')
        f.write('\n---Ex---\n' + str(tup).replace('Mode', '\nMode'))
        f.write('\n---Ey---\n' + str(tup).replace('Mode', '\nMode'))
        f.write('\n---Ez---\n' + str(tup).replace('Mode', '\nMode'))
        f.write('\n---end---')
        f.close()


    directory('/')
    mod = harm.harm_run(arg.res, arg.rad, arg.pml, cm.material_lib_dict(arg.mat, arg.u),
                        arg.fcen, arg.df, arg.rem, arg.t)
    modes_write(mod)

elif arg.out == 'sim' or arg.out == 'sim_res':
    directory('/eps_img')
    directory('/ex_img')
    directory('/ey_img')
    directory('/ez_img')
    path_e = directory('/')
    sim.sim_run(arg.res, arg.rad, arg.pml, cm.material_lib_dict(arg.mat, arg.u),
                arg.fcen, arg.df, arg.rem, arg.t, arg.dt, path_e, arg.out, arg.u)
else:
    visualisation.electric_field(arg.n, arg.out)
