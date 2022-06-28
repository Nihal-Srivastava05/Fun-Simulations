import pygame
import random
import noise
import math

from Assets.particle import Particle

PI = math.pi

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def convert_range(value):
	return (value + 1) / 2

def rotated_point(point, angle):
	x = point[0] + math.cos(math.radians(angle))
	y = point[1] + math.sin(math.radians(angle))

	return (x, y)

class Container:
	def __init__(self, width=200, height=200, scale=10, increment=0.1):
		self.windowWidth = width
		self.windowHeight = height
		self.scale = scale
		self.inc = increment
		self.rows = int(math.floor(self.windowWidth / self.scale))
		self.cols = int(math.floor(self.windowHeight / self.scale))
		self.zoff = 0
		self.particles = []
		self.flowfield = []

	def setup(self, screen):
		for i in range(1000):
			self.particles.append(Particle(width=self.windowWidth,
										   height=self.windowHeight,
										   scale=self.scale,
										   initial_pos=(random.random()*self.windowWidth,
										   				random.random()*self.windowHeight)))

		self.flowfield = [None] * (self.cols + self.rows * self.cols)
		screen.fill((255, 255, 255))

	def show(self, screen, show_direction=False, random_start=0):
		yoff = 0
		for y in range(self.rows):
			xoff = 0
			for x in range(self.cols):
				index = x + y * self.cols
				angle = convert_range(noise.pnoise3(xoff+random_start, yoff+random_start, self.zoff+random_start)) * 360
				v_start = pygame.math.Vector2(x*self.scale, y*self.scale)
				v_curr = pygame.math.Vector2(self.scale, 0).rotate(angle)
				v_end = v_start + v_curr

				xoff += self.inc

				v_curr.scale_to_length(1)
				self.flowfield[index] = v_curr

				if(show_direction):
					pygame.draw.line(screen, (0, 0, 0), v_start, v_end, 1)
			
			yoff += self.inc

		for i in range(len(self.particles)):
			self.particles[i].follow(self.flowfield)
			self.particles[i].update()
			self.particles[i].show(screen)
			self.particles[i].edges()

		self.zoff += 0.001

class Simulation:
	def __init__(self, height=200, width=200):
		self.windowHeight = height
		self.windowWidth = width

	def on_execute(self):
		pygame.init()
		screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		pygame.display.set_caption("Perlin Noise - Flow Field ")

		container = Container(width=self.windowWidth, height=self.windowHeight)
		container.setup(screen)

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			container.show(screen, random_start=101)
			pygame.display.update()

if __name__ == '__main__':
	simulator = Simulation(height=400, width=400)
	simulator.on_execute()