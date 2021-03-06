import tkinter as tk
import datetime as dt
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib
from tkinter import ttk, CENTER, SUNKEN, RAISED
from bluezero import microbit
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import threading
import time

from matplotlib import style
matplotlib.use("TkAgg")
style.use('ggplot')

ubit = microbit.Microbit(adapter_addr='B0:35:9F:CF:A7:CD',
                         device_addr='EC:34:F9:62:A7:09',
                         accelerometer_service=True,
                         button_service=True,
                         led_service=True,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=True)

ubit.connect()

buttonA_pressed, buttonB_pressed = False, False
x, y, z, t = [], [], [], []  # lists to hold accelerometer data
temp = None
update_screen_flag = True
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)

plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('Desktop BLE Client Accelerometer Readings')
plt.ylabel('Acceleration (g)')


def get_temperature_readings():
    global temp
    while True:
        temp = ubit.temperature
        time.sleep(5)

def update_button_states():
    global buttonA_pressed
    global buttonB_pressed
    while True:
        #print("Retrieving button data")
        buttonA_pressed = ubit.button_a
        buttonB_pressed = ubit.button_b
        # print(buttonA_pressed, buttonB_pressed)
        time.sleep(1)


def get_accelerometer_readings():
    while True:
        #print("Retrieving accel data")
        _x, _y, _z = ubit.accelerometer
        x.append(_x)
        y.append(_y)
        z.append(_z)
        t.append(dt.datetime.now())
        time.sleep(0.5)


threading.Thread(target=update_button_states).start()
threading.Thread(target=get_accelerometer_readings).start()  # we get the accel & temp readings in a thread due to it
threading.Thread(target=get_temperature_readings).start()    # being a large bottleneck in the speed of the program


def animate(i, x, y, z, t):
    x = x[-50:]
    y = y[-50:]
    z = z[-50:]
    t = t[-50:]

    a.clear()
    a.plot(t, x)
    a.plot(t, y)
    a.plot(t, z)


LARGE_FONT = ("Verdana", 12)


class Challenge3(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Desktop BLE Client Linux Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, AccelerometerPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="This is the start page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.canvas = tk.Canvas(self, width=400, height=175)

        self.buttonA = self.canvas.create_oval(20, 20, 120, 120,
                                     fill="red")
        self.buttonB = self.canvas.create_oval(275, 20, 375, 120,
                                     fill="red")
        self.canvas.pack(anchor=CENTER)

        threading.Thread(target=lambda: self.display_button_state()).start()

        button_grid = tk.Frame(self)
        grid = {}
        pixels = ubit.pixels
        for i in range(5):
            pixels[i] = "{0:5b}".format(pixels[i])
        for x in range(5):
            for y in range(5):
                btn = tk.Button(button_grid, command=lambda row=x, column=y: handle_pixel_grid(grid, row, column))
                btn.config(relief=RAISED)
                btn.grid(column=x, row=y)
                if pixels[y][x] == "1":
                    btn.configure(background="red")
                    btn.config(relief='sunken')
                grid[x, y] = btn

        threading.Thread(target=lambda: update_microbit_display(grid)).start()

        button_grid.pack()

        self.temperature = ttk.Label(self, text=ubit.temperature, font=LARGE_FONT)
        self.temperature.pack()

        threading.Thread(target=lambda: self.update_temp_reading()).start()

        button1 = ttk.Button(self, text="Graph Page",
                             command=lambda: controller.show_frame(AccelerometerPage))
        button1.pack()

        self.entry = tk.Entry(self, text="Message")
        self.entry.pack()

        button2 = ttk.Button(self, text="Send Message",
                             command=self.send_message)

        button2.pack()

    def send_message(self):
        update_screen_flag = False
        string = self.entry.get()
        ubit.text = string
        time.sleep(5)
        update_screen_flag = True

    def display_button_state(self):
        while True:
            if buttonA_pressed != 0:
                change_colour(canvas=self.canvas, object=self.buttonA, colour="green")
            else:
                change_colour(canvas=self.canvas, object=self.buttonA, colour="red")

            if buttonB_pressed != 0:
                change_colour(canvas=self.canvas, object=self.buttonB, colour="green")
            else:
                change_colour(canvas=self.canvas, object=self.buttonB, colour="red")
            time.sleep(1)

    def update_temp_reading(self):
        while True:
            string = str(temp) + " degrees C"
            self.temperature.configure(text=string)
            print(temp)
            time.sleep(1)


def change_colour(canvas=None, object=None, colour=None):
    canvas.itemconfig(object, fill=colour)


def handle_pixel_grid(grid, row, column):
    if grid[row, column].config('relief')[-1] == 'sunken':
        grid[row, column].config(relief=RAISED)
        grid[row, column].configure(background="#d9d9d9")
    else:
        grid[row, column].config(relief=SUNKEN)
        grid[row, column].configure(background="red")


def update_microbit_display(button_grid):
    while True:
        if update_screen_flag:
            pixel_grid = []
            #print("Retrieving pixel data")
            current_grid_on_mb = ubit.pixels
            for y in range(5):
                string = ""
                for x in range(5):
                    if button_grid[x, y].cget("background") == "red":
                        string += "1"
                    else:
                        string += "0"
                pixel_grid.append(string)

            for i in range(5):
                pixel_grid[i] = int(pixel_grid[i], 2)

            inter = set(pixel_grid).intersection(current_grid_on_mb)
            if len(inter) is not 0:
                #print("Sending pixel data")
                ubit.pixels = pixel_grid
        time.sleep(1)


class AccelerometerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Desktop BLE Client Accelerometer Readings", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
