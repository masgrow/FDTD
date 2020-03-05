import numpy as np
import matplotlib.pyplot as plt


def electric_field(name_simulation, out):
    def load_npz(name):
        return np.load('meep_sample/out/' + name_simulation + '/' + name + '.npz', mmap_mode='r', allow_pickle=True)

    def eps_save(comp, axes):
        plt.figure(0)
        plt.matshow(comp.transpose(), interpolation='spline36', cmap='binary')
        plt.savefig('meep_sample/out/' + name_simulation + '/eps_img/eps_' + axes)
        plt.close()
        return print('save: eps_' + axes)

    def save_comp_png(comp, comp_name, eps_axes):
        for time in range(np.size(comp, 0)):
            plt.figure(0)
            plt.matshow(eps_axes.transpose(), interpolation='spline36', cmap='binary', fignum=0)
            plt.matshow(comp[time][0:][0:].transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9, fignum=0)
            plt.savefig('meep_sample/out/' + name_simulation + '/' + comp_name + '_img/' + comp_name + '_' + str(time))
            plt.close()
        return print('save: ' + comp_name)

    if out == 'eps_png':
        eps = load_npz('eps')
        eps_save(eps['eps_xy'], 'xy')
        eps_save(eps['eps_xz'], 'xz')
        eps_save(eps['eps_yz'], 'yz')

    elif out == 'ex_xy_png':
        eps = load_npz('eps')
        ex = load_npz('ex')
        save_comp_png(ex['ex'], 'ex', eps['eps_xy'])
        return print('-done-')

    elif out == 'ey_xy_png':
        eps = load_npz('eps')
        ey = load_npz('ey')
        save_comp_png(ey['ey'], 'ey', eps['eps_xy'])
        return print('-done-')

    elif out == 'ez_xy_png':
        eps = load_npz('eps')
        ez = load_npz('ez')
        save_comp_png(ez['ez'], 'ez', eps['eps_xy'])
        return print('-done-')
