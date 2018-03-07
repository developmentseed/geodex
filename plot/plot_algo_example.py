"""
plot_algo_example.py

@author: DevelopmentSeed

Create images that show gif of how algorithm works
"""
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d

# Once images are created, compile them into gif with imagemagick like:
# convert -delay 100 -loop 0 *.png depth_search.gif

def add_square_patch(patch_list, tile_index, ax_obj):
    """Helper to update patches on the list"""

    for remove_ind in range(tile_index[2], 3):
        existing_p = patch_list[remove_ind]
        if existing_p is not None:
            existing_p.remove()
            patch_list[remove_ind] = None

    size_map = {0: 4, 1: 2, 2: 1}
    z_map = {0: 4, 1: 2, 2: 0}
    size = size_map[tile_index[2]]

    p = Rectangle(tile_index[0:2], size, size, alpha=0.5)
    ax_obj.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=z_map[tile_index[2]], zdir='z')

    patch_list[tile_index[2]] = p


# All zoom 2 tiles tiling whole world
tiles = [[0, 0, 0],
         [2, 2, 1],
         [3, 3, 2],
         [3, 2, 2],
         [2, 3, 2],
         [2, 2, 2],
         [2, 0, 1],
         [3, 1, 2],
         [3, 0, 2],
         [2, 1, 2],
         [2, 0, 2],
         [0, 2, 1],
         [1, 3, 2],
         [1, 2, 2],
         [0, 3, 2],
         [0, 2, 2],
         [0, 0, 1],
         [1, 1, 2],
         [1, 0, 2],
         [0, 1, 2],
         [0, 0, 2]]

#######################################
# Setup figure
#######################################
plt.close('all')
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(15, 30)
plt.axis('off')
#ax.grid('off')

# load some test data for demonstration and plot a wireframe
X, Y = np.meshgrid([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])

Z1 = np.zeros_like(X)
Z2 = 2 * np.ones_like(X)
Z3 = 4 * np.ones_like(X)

ax.plot_wireframe(X, Y, Z1)
ax.plot_wireframe(X, Y, Z2, rstride=2, cstride=2)
ax.plot_wireframe(X, Y, Z3, rstride=4, cstride=4)

#######################################
# Add in patches
#######################################
patch_list = [None, None, None]
tiles_printed = 0
tiles_stored = 0
text_params = dict(transform=ax.transAxes, horizontalalignment='right',
                   fontsize=14)

ax.text2D(0.9, 0.68, 'Zoom 0', **text_params)
ax.text2D(0.9, 0.41, 'Zoom 1', **text_params)
ax.text2D(0.9, 0.14, 'Zoom 2', **text_params)

ts_text = ax.text2D(0.4, 0.075, 'Tiles in memory: {:2.0f}'.format(tiles_stored),
                    **text_params)
tp_text = ax.text2D(0.4, 0.025, 'Tiles returned: {:2.0f}'.format(tiles_printed),
                    **text_params)
fig.savefig('plot_out_00.png')

for ii, ind in zip(range(1, len(tiles) + 1), tiles):
    add_square_patch(patch_list, ind, ax)

    tiles_stored = len(patch_list) - patch_list.count(None)
    if tiles_stored == len(patch_list):
        tiles_printed += 1

    ts_text.remove()
    tp_text.remove()
    ts_text = ax.text2D(0.4, 0.075, 'Tiles in memory: {:2.0f}'.format(tiles_stored),
                        **text_params)
    tp_text = ax.text2D(0.4, 0.025, 'Tiles returned: {:2.0f}'.format(tiles_printed),
                        **text_params)

    fig.savefig('plot_out_{:02.0f}.png'.format(ii))
