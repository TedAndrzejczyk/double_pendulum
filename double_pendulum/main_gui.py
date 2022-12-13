import tkinter as tk  # for GUI
from tkinter import ttk  # for GUI
from double_pendulum.physics import physics_calcs  # main module calls 'physics_calcs' function from 'physics' module

# create tkinter window
root = tk.Tk()  # create instance of tkinter frame
root.title("Double Pendulum Simulation")  # window title
root.geometry("680x410")  # width x height
root.resizable(False, False)  # fixed window size

# surface gravities in m/s^s
pluto = 0.6
moon = 1.6
mars = 3.7
mercury = 3.7
uranus = 8.9
venus = 8.9
earth = 9.8
saturn = 10.4
neptune = 11.2
kepler = 18.6  # Kepler 452b - most earth-like planet (1402 light years away)
jupiter = 25
sun = 274

# defaults parameters will always remain these
global defaults
defaults = [earth, 150, 150, 5, 5]


# create a slider and subtitle for parameter
def create_parameter(col, sub, lower, upper, parameter, num_type):
    base_row = 0
    subtitle = tk.Label(root, text=sub)  # subtitle
    subtitle.grid(row=base_row, column=col, sticky=tk.N, padx=(40, 0), pady=(5, 1))  # subtitle placement

    slider = tk.DoubleVar()  # slider creation
    if num_type == "float":
        slider_type = '%0.1f'  # increments of 0.1
    else:
        slider_type = '%d'  # increments of 1

    mainframe = ttk.Frame(root, padding="50 5 5 5")  # create slider frame: left, right, top, bottom
    mainframe.grid(row=base_row + 1, column=col)  # value placement

    ttk.Label(mainframe, textvariable=slider).grid(row=1, column=col)  # slider label
    slider_scale = ttk.Scale(mainframe, from_=lower, to_=upper, length=300, orient=tk.VERTICAL,
                             command=lambda s: slider.set(slider_type % float(s)))  # slider specs
    slider_scale.grid(row=base_row + 2, column=col)  # slider placement, label type

    slider.set(parameter)  # set slider value to default
    slider_scale.set(parameter)  # set slider to default value

    # plots each slider
    for child in mainframe.winfo_children():
        child.grid_configure(padx=20, pady=2)  # padding for each slider grid

    return slider  # return slider, use slider.get() to get the value later


# create labels (gravity)
def make_labels(name, value):
    size = 9  # Default font: Segoe UI, size 9
    name_label = tk.Label(root, text=name, font=("Arial", size))
    num_label = tk.Label(root, text=value, font=("Arial", size))

    return name_label, num_label


# label placements (gravity)
def grid_label(label, num_label, padx, pady):
    label.grid(row=1, column=0, sticky=tk.NW, padx=(padx, 0), pady=(pady, 0))  # pad left, right, up, down
    num_label.grid(row=1, column=0, sticky=tk.NW, padx=(105, 0), pady=(pady, 0))


# create a button with a command
def create_button(name, col, cmd):
    button = ttk.Button(root, text=name, width=15, command=cmd)  # create button
    button.grid(row=3, column=col, pady=10)  # button placement


# iterate through list of sliders and return each
def get_sliders(sliders):
    slider_values = []  # initial new sliders

    # add each slider value (using slider.get) to new_sliders list
    for slider in sliders:
        slider_values.append(slider.get())

    return slider_values


# main function, clear previous frame is True or False
def main(run, parameters):
    # creating parameter sliders
    # column, subtitle, lower, upper, default/parameter, num_type
    grav_slider = create_parameter(0, "Gravity (m/s^2)", moon, jupiter, parameters[0], "float")
    l1_slider = create_parameter(1, "Length 1 (cm)", 50, 200, parameters[1], "integer")
    l2_slider = create_parameter(2, "Length 2 (cm)", 50, 200, parameters[2], "integer")
    m1_slider = create_parameter(3, "Mass 1 (kg)", 1, 10, parameters[3], "integer")
    m2_slider = create_parameter(4, "Mass 2 (kg)", 1, 10, parameters[4], "integer")

    # list of all the sliders created (update if necessary)
    sliders = [grav_slider, l1_slider, l2_slider, m1_slider, m2_slider]

    # gravity text and number labels
    # text, num
    moon_label, moon_num_label = make_labels("The Moon", moon)
    mars_label, mars_num_label = make_labels("Mars", mars)
    earth_label, earth_num_label = make_labels("Earth", earth)
    neptune_label, neptune_num_label = make_labels("Neptune", neptune)
    kepler_label, kepler_num_label = make_labels("Kepler-452b", kepler)
    jupiter_label, jupiter_num_label = make_labels("Jupiter", jupiter)

    # gravity label placements
    # label, num_label, padx, pady
    grid_label(moon_label, moon_num_label, 15, 25)
    grid_label(mars_label, mars_num_label, 40, 51)
    grid_label(earth_label, earth_num_label, 40, 126)
    grid_label(neptune_label, neptune_num_label, 22, 143)
    grid_label(kepler_label, kepler_num_label, 3, 232)
    grid_label(jupiter_label, jupiter_num_label, 30, 312)

    # creating buttons
    # name, column, command
    create_button('Run', 2, lambda: main(True, get_sliders(sliders)))  # run button, collects and feeds values
    create_button('Undo', 3, lambda: main(False, parameters))  # resets values to last 'run' values
    create_button('Reset', 4, lambda: main(False, defaults))  # run main with original defaults
    # create_button('Quit', 4, lambda: root.quit())  # quits program

    # if main is called using 'run' button, use the 'physics' module w/ 'Run' parameters
    if run:
        physics_calcs(parameters)


main(False, defaults)  # run main module using defaults without returning parameter

root.mainloop()  # display window with everything
