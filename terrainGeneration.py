import pygame
import random
import noise

class Terrain:
	def __init__(self, width=500, height=500):
		self.windowWidth = width
		self.windowHeight = height
		self.terrain = []

	def generate_terrain(self, xoffset=0.0, yoffset=0.0):
		scale = 200
		octaves = 6
		persistence = 0.4
		lacunarity = 2.5
		terrain = []
		for i in range(self.windowWidth):
			row = []
			for j in range(self.windowHeight):
				row.append(noise.pnoise2((i + xoffset)/scale, (j + yoffset)/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity))
			terrain.append(row)
		self.terrain = terrain

	def show(self, screen):
		for i in range(self.windowWidth):
			for j in range(self.windowHeight):
				terrain_height = self.terrain[i][j]
				if(terrain_height < -0.25):
					screen.set_at((i, j), (15,94,156))
				elif(terrain_height < -0.05):
					screen.set_at((i, j), (28,163,236))
				elif(terrain_height < 0.05):
					screen.set_at((i, j), (234, 206, 106))
				elif(terrain_height > 0.3 and terrain_height < 0.45):
					screen.set_at((i, j), (85, 65, 36))
				elif(terrain_height > 0.45):
					screen.set_at((i, j), (255, 250, 250))
				else:
					screen.set_at((i, j), (126, 200, 80))

class Simulation:
	def __init__(self, height=500, width=500):
		self.windowHeight = height
		self.windowWidth = width

	def on_execute(self):
		pygame.init()
		screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		pygame.display.set_caption("Perlin Noise")

		terrain = Terrain(height=self.windowHeight, width=self.windowWidth)
		xoffset = 0.0
		yoffset = 0.0
		terrain.generate_terrain(xoffset=xoffset, yoffset=yoffset)

		running = True
		while running:
			screen.fill((255, 255, 255))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						yoffset -= 10
					if event.key == pygame.K_a:
						xoffset -= 10
					if event.key == pygame.K_s:
						yoffset += 10
					if event.key == pygame.K_d:
						xoffset += 10
					terrain.generate_terrain(xoffset=xoffset, yoffset=yoffset)

			terrain.show(screen)
			pygame.display.update()

if __name__ == '__main__':
	simulator = Simulation(height=500, width=500)
	simulator.on_execute()