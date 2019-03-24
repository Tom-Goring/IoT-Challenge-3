from MicroBit.GUI import *


app = Challenge3()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, fargs=(x, y, z, t), interval=1)
app.mainloop()