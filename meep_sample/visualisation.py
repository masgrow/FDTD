import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
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

    def save_comp_png(comp, comp_name, eps_axes):
        for time in range(np.size(comp, 0)):
            plt.figure(0)
            plt.matshow(eps_axes.transpose(), interpolation='spline36', cmap='binary', fignum=0)
            plt.matshow(comp[time][0:][0:].transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9, fignum=0)
            plt.savefig('meep_sample/out/' + name_simulation + '/' + comp_name + '_img/' + comp_name + '_' + str(time))
            plt.close()
        return print('save: ' + comp_name)

    def save_comp__mp4(comp, comp_name, eps_axes):
        fig = plt.subplot()
        plt.imshow(eps_axes.transpose(), interpolation='spline36', cmap='binary')
        fig_list = []

        for time in range(np.size(comp, 0) - 1):
            plt.imshow(comp[time][0:][0:].transpose(),
                       interpolation='spline36', cmap='RdBu', alpha=0.9)

            anim = plt.gcf()
            fig_list.append(anim)

        anim_comp = animation.ArtistAnimation(fig=fig, artists=fig_list)
        plt.close()
        anim_comp.save('meep_sample/out/' + name_simulation + '/' + comp_name + '_' + str(np.size(comp, 0)) + '.mp4',
                       writer='ffmpeg', fps=5)





    # eps_save(eps['eps_xy'], 'xy')
    # eps_save(eps['eps_xz'], 'xz')
    # eps_save(eps['eps_yz'], 'yz')
    # save_comp_png(ex['ex'], 'ex', eps['eps_xy'])
    # save_comp_png(ey['ey'], 'ey', eps['eps_xy'])
    # save_comp_png(ez['ez'], 'ez', eps['eps_xy'])
    save_comp__mp4(ez['ez'], 'ez', eps['eps_xy'])
    return print('-done-')
