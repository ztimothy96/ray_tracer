import vec3
from ray import *
import random

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

class Dielectric(Material):
    '''
    float ri: refraction index of the material
    '''
    def __init__(self, ri):
        super(Dielectric, self).__init__((1, 1, 1))
        self.ri = ri

    def schlick(self, cos, ri):
        r0 = ((1 - ri) / (1 + ri))**2
        return r0 + (1-r0) * (1-cos)**5
        
    def scatter(self, ray, record):
        reflected = vec3.reflect(vec3.normalize(ray.direction), record.normal)
        outward_normal = (0, 0, 0)
        idx_ratio = 0

        if vec3.dot(ray.direction, record.normal) > 0:
            outward_normal = vec3.scale(record.normal, -1)
            idx_ratio = self.ri
            cos = self.ri * vec3.dot(vec3.normalize(ray.direction), record.normal)
        else:
            outward_normal = record.normal
            idx_ratio = 1.0 / self.ri
            cos = -vec3.dot(vec3.normalize(ray.direction), record.normal)

        refracted = vec3.refract(ray.direction, outward_normal, idx_ratio)
        if refracted:
            reflect_prob = self.schlick(cos, self.ri)
            if random.random() < reflect_prob:
                return Ray(record.p, reflected)
            return Ray(record.p, refracted)
        else:
            return Ray(record.p, reflected)
