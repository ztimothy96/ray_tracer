import math
import vec3

class HitRecord():
    def __init__(self):
        self.t = None # float: the time the ray hits
        self.p = None # vec3: the point that the ray hits
        self.normal = None # vec3: the normal vector to the hitpoint
        self.material = None

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
        return vec3.add(self.origin, vec3.scale(self.direction, t))


class Sphere():
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min, t_max):
        record = HitRecord()
        oc = vec3.subtract(ray.origin, self.center)
        a = vec3.squared_length(ray.direction)
        b = vec3.dot(oc, ray.direction)
        c = vec3.squared_length(oc) - self.radius**2
        discriminant = b**2 - a*c
        if discriminant > 0:
            t = (-b-math.sqrt(discriminant))/a
            if (t < t_max and t > t_min):
                record.t = t
                record.p = ray.point_at_time(t)
                record.normal = vec3.normalize(
                    vec3.subtract(record.p, self.center))
                record.material = self.material
                return record
        return None


# looks fine
class HitableList():
    def __init__(self, hitables):
        self.hitables = hitables

    def hit(self, ray, t_min, t_max):
        closest_record = HitRecord()
        hit_anything = False
        closest = t_max
        for i in range(len(self.hitables)):
            record = self.hitables[i].hit(ray, t_min, closest)
            if record:
                hit_anything = True
                closest = record.t
                closest_record = record
        return closest_record if hit_anything else None


class Camera():
    '''
    vec3 origin: camera position
    vec3 lookat: the lookat point
    vec3 up: the up vector specifying camera orientation
    float fov: degrees between top and bottom rays
    float aspect: ratio of width to height
    '''
    
    def __init__(self, origin, lookat, up, fov, aspect):
        theta = fov*math.pi/180
        half_height = math.tan(theta/2)
        half_width = aspect * half_height
        self.origin = origin
        w = vec3.normalize(vec3.subtract(origin, lookat))
        u = vec3.normalize(vec3.cross(up, w))
        v = vec3.cross(w, u)
        self.horizontal = vec3.scale(u, 2*half_width)
        self.vertical = vec3.scale(v, 2*half_height)
        center = vec3.subtract(origin, w)
        shift = vec3.scale(vec3.add(self.horizontal, self.vertical), 0.5)
        self.llc = vec3.subtract(center, shift)

    '''
    float u, v: parametric coordinates for the point the ray points to
    '''
    def get_ray(self, u, v):
        up = vec3.scale(self.vertical, v)
        right = vec3.scale(self.horizontal, u)
        direction = vec3.subtract(self.llc, self.origin)
        direction = vec3.add(direction, up)
        direction = vec3.add(direction, right)
        return Ray(self.origin, direction)
