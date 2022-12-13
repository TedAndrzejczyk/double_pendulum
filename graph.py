import matplotlib.pyplot as plt  # for plots
from matplotlib.ticker import MaxNLocator  # forces x-axis ticks to be integers if possible
import time  # to take time elapsed


# uses these parameters to set up an energy graph on the right subplot
def graphing(i, loop_time, start_time, x_graph, y1_graph, y2_graph, ax2, K, U):
    # calculate time elapsed from iteration and loop time (s)
    scaling_factor = 60.799 * loop_time ** (-0.951)  # found using power trend line from excel data
    corrected_loop_sec = (loop_time / 1000) * scaling_factor  # corrected loop time in seconds

    # time elapsed since beginning of animation
    end_time = time.time()
    elapsed_time = end_time - start_time

    # append the time to the x list, append the energy value to the y list
    x_graph.append(elapsed_time)  # x = time
    y1_graph.append(K[i])  # y = energy values
    y2_graph.append(U[i])

    ax2.clear()  # clear plot every iteration so no overlap

    # only plot the last approx 5 seconds (or whatever number is divisor of loop_sec)
    time_shown = round(5 / corrected_loop_sec)  # sec/(sec/iteration) = iterations
    ax2.plot(x_graph[-time_shown:], y1_graph[-time_shown:])
    ax2.plot(x_graph[-time_shown:], y2_graph[-time_shown:])

    # forces x-axis ticks to be integers if possible
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

    # plot labels
    plt.legend(['Kinetic Energy', 'Potential Energy'], loc='upper center')
    ax2.set_xlabel('Time Elapsed (s)')
    ax2.set_ylabel('Energy Value [J]')
    ax2.set_title('Double Pendulum Energy')
