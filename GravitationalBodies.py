import pygame
import math
import random

G = 6.6743 * (10 ** (-3)) # (6.6743 ± 0.00015) × 10−11 m3 kg−1 s−2.

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

class Body:
	def __init__(self, width, height, mass, scale=10, initial_pos=(0, 0), initial_vel=(0, 0)):
		self.width = width
		self.height = height
		self.scale = scale
		self.rows = int(math.floor(self.width / self.scale))
		self.cols = int(math.floor(self.height / self.scale))
		self.mass = mass

		self.pos = pygame.math.Vector2(initial_pos[0], initial_pos[1])
		self.vel = pygame.math.Vector2(initial_vel[0], initial_vel[1])
		self.acc = pygame.math.Vector2(0, 0)

		self.maxSpeed = 1

	def update(self):
		self.vel += self.acc
		# self.vel.scale_to_length(self.maxSpeed)
		self.pos += self.vel
		self.acc *= 0

	def follow(self, vectors):
		x = int(math.floor(self.pos.x / self.scale))
		y = int(math.floor(self.pos.y / self.scale))
		index = x + y * self.cols
		force = vectors[index]
		self.applyForce(force)

	def applyForce(self, force):
		self.acc += (force / self.mass)

	def show(self, screen):
		# screen.set_at((int(self.pos.x), int(self.pos.y)), (255, 0, 0))
		# pygame.draw.circle(screen, (0, 0, 0), (int(self.pos.x), int(self.pos.y)), 1)
		
		draw_circle_alpha(screen, (0, 0, 0, self.mass*255/1000), (int(self.pos.x), int(self.pos.y)), 10)

	def edges(self):
		if(self.pos.x > self.width or self.pos.x < 0):
			self.vel.x *= -1
		if(self.pos.y > self.height or self.pos.y < 0):
			self.vel.y *= -1

		# if(self.pos.x > self.width):
		# 	self.pos.x = 0
		# elif(self.pos.x < 0):
		# 	self.pos.x = self.width - 1
		
		# if(self.pos.y > self.height):
		# 	self.pos.y = 0
		# elif(self.pos.y < 0):
		# 	self.pos.y = self.height - 1

def calculateNetForce(a, b):
	# fx = rGmM/r^3, r = (x^2 + y^2)^0.5, r = ax - bx (force on a by b)
	r = (b.pos[0] - a.pos[0], b.pos[1] - a.pos[1])
	magR = (r[0] ** 2 + r[1] ** 2) ** 0.5
	fx = r[0] * G * a.mass * b.mass / (magR ** 3)
	fy = r[1] * G * a.mass * b.mass / (magR ** 3)
	return pygame.math.Vector2(fx, fy)
	

class Container:
	def __init__(self, width=200, height=200, scale=10, increment=0.1):
		self.windowWidth = width
		self.windowHeight = height
		self.scale = scale
		self.inc = increment
		self.rows = int(math.floor(self.windowWidth / self.scale))
		self.cols = int(math.floor(self.windowHeight / self.scale))
		self.zoff = 0
		self.bodies = []

	def setup(self, screen):
		for i in range(1, 6):
			self.bodies.append(Body(width=self.windowWidth, height=self.windowHeight, mass=50 * i, scale=self.scale, initial_pos=(random.random()*self.windowWidth,random.random()*self.windowHeight)))

		self.bodies.append(Body(width=self.windowWidth, height=self.windowHeight, mass=1000, scale=self.scale, initial_pos=(random.random()*self.windowWidth,random.random()*self.windowHeight)))

		screen.fill((255, 255, 255))

	def show(self, screen, show_direction=False, random_start=0):
		screen.fill((255, 255, 255))
		for i in range(len(self.bodies)):
			totalForce = pygame.math.Vector2(0, 0)
			for j in range(len(self.bodies)):
				if i != j:
					force = calculateNetForce(self.bodies[i], self.bodies[j])
					totalForce += force
			self.bodies[i].applyForce(totalForce)
					
					
		# for y in range(self.rows):
		# 	xoff = 0
		# 	for x in range(self.cols):
		# 		index = x + y * self.cols
		# 		angle = convert_range(noise.pnoise3(xoff+random_start, yoff+random_start, self.zoff+random_start)) * 360
		# 		v_start = pygame.math.Vector2(x*self.scale, y*self.scale)
		# 		v_curr = pygame.math.Vector2(self.scale, 0).rotate(angle)
		# 		v_end = v_start + v_curr

		# 		xoff += self.inc

		# 		v_curr.scale_to_length(1)
		# 		self.flowfield[index] = v_curr

		# 		if(show_direction):
		# 			pygame.draw.line(screen, (0, 0, 0), v_start, v_end, 1)
			
		# 	yoff += self.inc
		

		for i in range(len(self.bodies)):
			# self.particles[i].follow(self.flowfield)
			self.bodies[i].update()
			self.bodies[i].show(screen)
			self.bodies[i].edges()

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
	simulator = Simulation(height=1000, width=1000)
	simulator.on_execute()