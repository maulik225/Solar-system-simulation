from re import A
from turtle import distance
import pygame
import math

pygame.init()

width ,height = 800, 650
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System")

FONT = pygame.font.SysFont("comicsans", 16)

class Planet: 
    AU = 149.6e6 * 1000 # 149.6 million km
    G = 6.67428e-11 # Gravitational Constant
    SCALE = 200/AU # 1 AU = 100 Pixels
    TIMESTEP = 3600 * 24 # 1 Day = 24 Hours = 3600 Seconds
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit =[]
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self,Win):
        x = self.x * self.SCALE + width/2
        y = self.y * self.SCALE + height/2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + width/2
                y = y * self.SCALE + height/2
                updated_points.append((x,y))
            
            pygame.draw.lines(Win, self.color, False, updated_points, 2)
            
        pygame.draw.circle(Win, self.color, (x,y), self.radius)        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)} KM", 1, (255,255,255))
            Win.blit(distance_text, (x, y))
        
    def attraction(self,other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if other.sun:
            self.distance_to_sun = distance 
        force = self.G * self.mass * other.mass / (distance**2) 
        theta = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y

    def update_position(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx ,fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x,self.y))

def main():
    run = True 
    clock = pygame.time.Clock() # to keep track of time
    
    sun = Planet(0,0,30, (255,255,0), 1.98892 * 10**30) # Sun
    sun.sun = True
    
    earth = Planet(-1*Planet.AU, 0, 16, (0,0,255), 5.9742 * 10**24) # Earth
    earth.y_vel = 29.783 * 1000 # 29.783 km/s
    
    mars = Planet(-1.524*Planet.AU, 0, 12, (255,0,0), 6.39 * 10**23) # Mars
    mars.y_vel = 24.077 * 1000 # 24.077 km/s
    
    mercury = Planet(0.387*Planet.AU, 0, 8, (80,78,100), 3.3011 * 10**23) # Mercury
    mercury.y_vel = -47.362 * 1000 # 47.362 km/s
    
    venus = Planet(0.723*Planet.AU, 0, 14, (255,255,255), 4.8685 * 10**24) # Venus
    venus.y_vel = -35.02 * 1000 # 35.02 km/s
    
    
    planets = [sun,earth,mars,mercury,venus]
    while run: # main game loop
        clock.tick(60) # 60 frames per second
        WIN.fill((0,0,0)) # fill the screen with black
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update() # update the screen
            
    pygame.quit()
    
main()
