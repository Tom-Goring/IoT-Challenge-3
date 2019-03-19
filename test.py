import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from bluezero import microbit


ubit = microbit.Microbit(adapter_addr='B0:35:9F:CF:A7:CD',
                         device_addr='EC:34:F9:62:A7:09',
                         accelerometer_service=True,
                         button_service=True,
                         led_service=True,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=True)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = []
y = []
z = []
t = []

ubit.connect()


def animate(i, x, y, z, t):
    _x, _y, _z = ubit.accelerometer
    x.append(_x)
    y.append(_y)
    z.append(_z)
    t.append(dt.datetime.now())

    x = x[-20:]
    y = y[-20:]
    z = z[-20:]
    t = t[-20:]

    ax.clear()
    ax.plot(t, x)
    ax.plot(t, y)
    ax.plot(t, z)

    #ax.set_xlim(2.1)

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('MicroBit Accelerometer Readings')
    plt.ylabel('Acceleration (g)')


ani = animation.FuncAnimation(fig, animate, fargs=(x, y, z, t), interval=10)
plt.show()

