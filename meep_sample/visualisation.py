import numpy as np
import matplotlib.pyplot as plt
import glob
from os import system


def electric_field(name_simulation):
    def load_npz(name):
        return np.load('meep_sample/out/' + name_simulation + '/' + name + '.npz', mmap_mode='r', allow_pickle=True)

    eps = load_npz('eps')
    ex = load_npz('ex')
    ey = load_npz('ey')
    ez = load_npz('ez')

    def eps_save(comp, axes):
        plt.figure(0)
        plt.matshow(comp.transpose(), interpolation='spline36', cmap='binary')
        plt.savefig('meep_sample/out/' + name_simulation + '/eps_img/eps_' + axes)
        plt.close()
        return print('save: eps_' + axes)

    def save_figure(comp, comp_name, eps_axes):
        for time in range(np.size(comp, 0)):
            plt.figure(0)
            plt.matshow(eps_axes.transpose(), interpolation='spline36', cmap='binary', fignum=0)
            plt.matshow(comp[time][0:][0:].transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9, fignum=0)
            plt.savefig('meep_sample/out/' + name_simulation + '/' + comp_name + '_img/' + comp_name + '_' + str(time))
            plt.close()
        return print('save: ' + comp_name)

    def img_to_gif(name):
        gif_name = name
        file_list = glob.glob('meep_sample/out/' + name + '_img/' + '*.png')
        list.sort(file_list, key=lambda x: int(
            x.split('_')[1].split('.png')[0]))

        with open('image_list.txt', 'w') as file:
            for item in file_list:
                file.write("%s\n" % item)

        system('convert @image_list.txt {}.gif'.format(gif_name))

    eps_save(eps['eps_xy'], 'xy')
    eps_save(eps['eps_xz'], 'xz')
    eps_save(eps['eps_yz'], 'yz')
    save_figure(ex['ex'], 'ex', eps['eps_xy'])
    save_figure(ey['ey'], 'ey', eps['eps_xy'])
    save_figure(ez['ez'], 'ez', eps['eps_xy'])
    img_to_gif('ex')
    return print('-done-')
