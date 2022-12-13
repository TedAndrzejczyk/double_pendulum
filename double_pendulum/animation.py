from double_pendulum.graph import graphing  # animation calls graphing module to do energy graphs

import matplotlib.pyplot as plt  # for plots
from matplotlib import animation  # for animation
import numpy as np  # for a range of values
import time  # to take time elapsed


# makes an animation based off of these parameters
def animating(x1, y1, x2, y2, K, U):
    """Sets up figure and animates 2 subplots based on physics calculations

    Args: x1 (float): x1 coordinate of pendulum
          y1 (float): y1 coordinate of pendulum
          x2 (float): x2 coordinate of pendulum
          y2 (float): y2 coordinate of pendulum
          K (list): Kinetic Energy (J)
          U (list: Potential Energy (J)

    Output: Figure with an animated double pendulum simulation subplot and energy graph subplot
    """

    # plot figure, make subplots
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    fig.set_size_inches(12, 6, forward=True)

    # initialize empty x and y lists
    x_graph = []
    y1_graph = []
    y2_graph = []

    # function to set up updating plot
    def animate(i, K, U, loop_time, start_time):
        """Sets pendulum simulation and calls graphing module

        Args: i (int): iteration
              K (list): Kinetic Energy (J)
              U (list): Potential Energy (J)
              loop_time (int): loop time (ms)
              start_time (float): start time to find elapsed time later
        """

        # get rid of axes on ax1
        ax1.clear()
        ax1.axis('off')

        # compute ln1
        ln1, = ax1.plot([], [], 'bo-', lw=3, markersize=8)

        # set static bounds
        ax1.set_ylim(-4, 4)
        ax1.set_xlim(-4, 4)

        # animate ln1
        ln1.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

        # refer to graphing module for 2nd subplot
        graphing(i, loop_time, start_time, x_graph, y1_graph, y2_graph, ax2, K, U)

        # Disclaimer
        fig.suptitle("*Please Close this Window Before Running a New Simulation*", fontsize='small');

    # time at before animation begins
    start_time = time.time()
    loop_time = 4  # ms

    # animation, plays for about 70 seconds
    ani = animation.FuncAnimation(fig, animate, fargs=(K, U, loop_time, start_time), frames=1000, interval=loop_time)

    # show plots, ensure all fig windows displayed and return immediately
    plt.show(block=False)

    fig_num = 1  # default fig_num is 1

    # if plot #2 exists, close plot #1, plot #2 is now default
    if plt.fignum_exists(2):
        plt.close(1)
        fig_num = 2

    # if user manually closed plot, then also close the plot computationally
    for i in np.arange(120):
        plt.pause(0.5)  # pause 0.5 seconds before checking again

        # if plot doesn't exist (user closed it), close it computationally as well
        if not plt.fignum_exists(fig_num):
            plt.close(fig_num)
