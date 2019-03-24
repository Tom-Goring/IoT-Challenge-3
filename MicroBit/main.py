from MicroBit.GUI import *


app = Challenge3()
ani = animation.FuncAnimation(f, animate, fargs=(x, y, z, t), interval=5)
app.mainloop()
