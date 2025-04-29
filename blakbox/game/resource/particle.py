from blakbox.globs import os, pg, math, random
from blakbox.atom import Atom

# ------------------------------------------------------------ #
class ParticleSystem:
    def __init__(self):
        self.spawners = []      # A list of spawners, each with its own configuration
        self.particles = []     # Raw particle data: [x, y, dx, dy, lifetime, max_lifetime, size, color]
        
    def set_spawner(
            self,
            rate: int, speed: int, lifetime: int, pos: list[float], 
            color:list[int]=[255, 255, 255], drange: list[float]=[10, -10], srange: list[int]=[2,8]
        ) -> None:
        spawner = [rate, speed, lifetime, pos, color, drange, srange]
        self.spawners.append(spawner)
        return len(self.spawners) - 1
    
    def mod_spawner(
            self, pspawn: int,
            rate: int=None, speed: int=None, lifetime: int=None, pos: list[float]=None,
            color:list[int]=None, drange: list[float]=None, srange: list[int]=None
        ) -> None:
        if pspawn < 0 or pspawn >= len(self.spawners): return
        self.spawners[pspawn][0] = rate if rate else self.spawners[pspawn][0]
        self.spawners[pspawn][1] = speed if speed else self.spawners[pspawn][1]
        self.spawners[pspawn][2] = lifetime if lifetime else self.spawners[pspawn][2]
        self.spawners[pspawn][3] = pos if pos else self.spawners[pspawn][3]
        self.spawners[pspawn][4] = color if color else self.spawners[pspawn][4]
        self.spawners[pspawn][5] = drange if drange else self.spawners[pspawn][5]
        self.spawners[pspawn][6] = srange if srange else self.spawners[pspawn][6]

    def spawn(self):
        for r, s, l, p, c, dr, sr in self.spawners:
            for _ in range(r):
                x, y = p
                lifetime = random.uniform(1 * 0.4, l)
                speed = random.uniform(s//4, s)
                direction = random.uniform(dr[0], dr[1])
                dx = speed * math.cos(direction)
                dy = speed * math.sin(direction)
                size = random.uniform(sr[0], sr[1])
                self.particles.append([x, y, dx, dy, lifetime, size, c])

    def update(self, dt):
        to_remove = []
        for i, particle in enumerate(self.particles):
            x, y, dx, dy, lifetime, size, color = particle
            if lifetime <= 0: continue
            
            x += dx * dt
            y += dy * dt
            dy += 9.8 * dt

            lifetime -= dt
            if lifetime <= 0:
                to_remove.append(i)
            else:
                self.particles[i] = [x, y, dx, dy, lifetime, size, color]
        self.particles = [p for i, p in enumerate(self.particles) if i not in to_remove]

    def render(self, render_func: callable):
        if not callable(render_func):
            return
        for particle in self.particles:
            x, y, _, _, lifetime, size, color = particle
            render_func(x, y, lifetime, size, color)
# ------------------------------------------------------------ #
