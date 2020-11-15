import math
import vec3

'''
params:
Vec3 origin
Vec3 direction
'''
class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    # t is a scalar parameter
    def point_at_time(self, t):
        return self.origin + Vec3.scale(direction, t)

    def hit_sphere(self, center, radius):
        oc = vec3.add(self.origin, vec3.scale(center, -1))
        a = vec3.length(self.direction)
        b = 2.0 * vec3.dot(oc, self.direction)
        c = vec3.length(oc) - radius**2
        discriminant = b**2 - 4*a*c
        return discriminant > 0
