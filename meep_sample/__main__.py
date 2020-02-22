import initial_values as iv
import custom_materials as cm
import harm
from os import makedirs, path

arg = iv.init_values(cm.material_lib())


def out_path(name):
    out = 'out/' + name
    return out


def directory():
    if not path.exists(out_path(arg.n)):
        makedirs(out_path(arg.n), mode=0o777, exist_ok=False)


if arg.mod == 'harm':
    def modes_write(tup):
        f = open(out_path(arg.n + '/modes'), 'a')
        f.write('\n\n----start----')
        f.write('\n\n Parameters::  radius: ' + str(arg.rad))
        f.write('   material: ' + str(arg.mat))
        f.write('   wavelength: ' + str(arg.wl))
        f.write('   width: ' + str(arg.wid))
        f.write('   resolution: ' + str(arg.res))
        f.write('   time: ' + str(arg.t))
        f.write('\n\n Format::  frequency, imag. freq., Q, |amp|, amplitude, error')
        f.write('\n\n---Ex---\n\n' + str(tup[0]))
        f.write('\n\n---Ey---\n\n' + str(tup[1]))
        f.write('\n\n---Ez---\n\n' + str(tup[2]))
        f.write('\n\n---end---')
        f.close()


    directory()
    mod = harm.harm_run(arg.res, arg.rad, arg.pml, cm.material_lib_dict(arg.mat), arg.wl, arg.wid, arg.rem, arg.t)
    modes_write(mod)

elif arg.mod == 'sim':

    directory()
