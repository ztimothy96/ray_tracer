import vec3
from ray import *

class Material():
    def __init__(self, a):
        self.attenuation = a #how much of each light ray the material reflects

    def scatter(ray, record):
        pass

class Lambertian(Material):
    def __init__(self, a):
        super(Lambertian, self).__init__(a)
        
    def scatter(self, ray, record):
        target = vec3.add(vec3.add(record.p, record.normal), vec3.rand_sphere())
        scattered = Ray(record.p, vec3.subtract(target, record.p))
        return scattered
    
class Metal(Material):
    def __init__(self, a):
        super(Metal, self).__init__(a)
        
    def scatter(self, ray, record):
        reflected = vec3.reflect(vec3.normalize(ray.direction), record.normal)
        scattered = Ray(record.p, reflected)
        return scattered if vec3.dot(scattered.direction, record.normal) > 0 else None
