import pygame
import math
import random

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

class Particle:
	def __init__(self, width, height, scale=10, initial_pos=(0, 0), initial_vel=(0, 0)):
		self.width = width
		self.height = height
		self.scale = scale
		self.rows = int(math.floor(self.width / self.scale))
		self.cols = int(math.floor(self.height / self.scale))

		self.pos = pygame.math.Vector2(initial_pos[0], initial_pos[1])
		self.vel = pygame.math.Vector2(initial_vel[0], initial_vel[1])
		self.acc = pygame.math.Vector2(0, 0)

		self.maxSpeed = 1

	def update(self):
		self.vel += self.acc
		self.vel.scale_to_length(self.maxSpeed)
		self.pos += self.vel
		self.acc *= 0

	def follow(self, vectors):
		x = int(math.floor(self.pos.x / self.scale))
		y = int(math.floor(self.pos.y / self.scale))
		index = x + y * self.cols
		force = vectors[index]
		self.applyForce(force)

	def applyForce(self, force):
		self.acc += force

	def show(self, screen):
		# screen.set_at((int(self.pos.x), int(self.pos.y)), (255, 0, 0))
		# pygame.draw.circle(screen, (0, 0, 0), (int(self.pos.x), int(self.pos.y)), 1)
		draw_circle_alpha(screen, (0, 0, 0, 5), (int(self.pos.x), int(self.pos.y)), 1)

	def edges(self):
		if(self.pos.x > self.width):
			self.pos.x = 0
		elif(self.pos.x < 0):
			self.pos.x = self.width - 1
		
		if(self.pos.y > self.height):
			self.pos.y = 0
		elif(self.pos.y < 0):
			self.pos.y = self.height - 1