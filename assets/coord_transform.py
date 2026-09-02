from scipy.spatial.transform import RigidTransform as Tf
from scipy.spatial.transform import Rotation as R
import numpy as np

import matplotlib.pyplot as plt
colors = ("#FF6666", "#005533", "#1199EE")  # Colorblind-safe RGB

def plot_transformed_axes(ax, tf, name=None, scale=1):
    r = tf.rotation
    t = tf.translation
    loc = np.array([t, t])
    for i, (axis, c) in enumerate(zip((ax.xaxis, ax.yaxis, ax.zaxis),
                                      colors)):
        axlabel = axis.axis_name
        axis.set_label_text(axlabel)
        axis.label.set_color(c)
        axis.line.set_color(c)
        axis.set_tick_params(colors=c)
        line = np.zeros((2, 3))
        line[1, i] = scale
        line_rot = r.apply(line)
        line_plot = line_rot + loc
        ax.plot(line_plot[:, 0], line_plot[:, 1], line_plot[:, 2], c)
        text_loc = line[1]*1.2
        text_loc_rot = r.apply(text_loc)
        text_plot = text_loc_rot + t
        ax.text(*text_plot, axlabel.upper(), color=c,
                va="center", ha="center")
    ax.text(*tf.translation, name, color="k", va="center", ha="center",
            bbox={"fc": "w", "alpha": 0.8, "boxstyle": "circle"})


def get_transform_a_b(p1_cam):
        # define base coordinate system (in robot base)
        tf_base = Tf.identity()

        # rotation from base to cam
        rot_x = R.from_matrix([[1, 0, 0],[0, -1, 0],[0, 0, -1]])
        rot_y = R.from_matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
        rot_z = R.from_matrix([[0, -1, 0],[1, 0, 0],[0, 0, 1]])

        r_base_cam = rot_x * rot_y * rot_z
        #print(r_base_cam)

        # translation from base to cam 
        #t_base_cam = np.array([180,-40,480])    # Robot 01
        #t_base_cam = np.array([190,10,480])     # Robot 02
        t_base_cam = np.array([190,0,480])    # Robot 03

        # get full transformation
        tf_base_cam = Tf.from_components(t_base_cam, r_base_cam)

        # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        # plot_transformed_axes(ax, tf_base, name="tfA")     # A plotted in A
        # plot_transformed_axes(ax, tf_base_cam, name="tfAB")  # B plotted in A
        # ax.set_title("A, B frames with respect to A")
        # ax.set_aspect("equal")
        # ax.figure.set_size_inches(6, 5)
        # plt.show()

        tf_cam_base = tf_base_cam.inv()

        #p1_cam = np.array([-56, 14, 420])

        p1_base = tf_base_cam.apply(p1_cam)

        #print(p1_cam)
        #print(p1_base)

        return p1_base


""" 
# define base coordinate system (in robot base)
tf_base = Tf.identity()

# rotation from base to cam
rot_x = R.from_matrix([[1, 0, 0],[0, -1, 0],[0, 0, -1]])
rot_y = R.from_matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
rot_z = R.from_matrix([[0, -1, 0],[1, 0, 0],[0, 0, 1]])

r_base_cam = rot_x * rot_y * rot_z
#print(r_base_cam)

# translation from base to cam 
t_base_cam = np.array([300,70,420])

# get full transformation
tf_base_cam = Tf.from_components(t_base_cam, r_base_cam)

#print(tf_base_cam)

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# plot_transformed_axes(ax, tf_base, name="tfA")     # A plotted in A
# plot_transformed_axes(ax, tf_base_cam, name="tfAB")  # B plotted in A
# ax.set_title("A, B frames with respect to A")
# ax.set_aspect("equal")
# ax.figure.set_size_inches(6, 5)
# plt.show()

#tf_base_cam = get_transform_a_b()

tf_cam_base = tf_base_cam.inv()

p1_cam = np.array([-56, 14, 420])

p1_base = tf_base_cam.apply(p1_cam)

#print(p1_cam)
#print(p1_base) """