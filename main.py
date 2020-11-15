import random
import math
from tkinter import Tk, Canvas, PhotoImage, mainloop
import vec3
from ray import Ray

width = 400
height = 200
window = Tk()
canvas = Canvas(window, width=width, height=height)
canvas.pack()
img = PhotoImage(width=width, height=height)
canvas.create_image((width//2, height//2), image=img, state="normal")

def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

def color(ray):
    if ray.hit_sphere((0, 0, -1), 0.5):
        return (1, 0, 0)
    unit = vec3.normalize(ray.direction)
    t = 0.5 * (unit[1] + 1.0)
    c1 = vec3.scale((1.0, 1.0, 1.0), 1.0 - t)
    c2 = vec3.scale((0.5, 0.7, 1.0), t)
    return vec3.add(c1, c2)

# note that height is reversed from C++
def draw():
    llc = (-2.0, -1.0, -1.0)
    horizontal = (4.0, 0.0, 0.0)
    vertical = (0.0, 2.0, 0.0)
    origin = (0.0, 0.0, 0.0)
    for j in range(height):
        for i in range(width):
            u, v = float(i) / float(width), float(j) / float(height)
            direction = vec3.scale(vertical, v)
            direction = vec3.add(direction, vec3.scale(horizontal, u))
            direction = vec3.add(direction, llc)
            ray = Ray(origin, direction)
            r, g, b = color(ray)
            ir = int(255.99 * r)
            ig = int(255.99 * g)
            ib = int(255.99 * b)
            img.put(from_rgb((ir, ig, ib)), (i, height-j-1))
draw()
mainloop()
