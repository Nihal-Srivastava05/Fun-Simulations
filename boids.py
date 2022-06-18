import pygame
import random
import math

def dist(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def add_vectors(v1, v2):
	return [v1[0] + v2[0], v1[1] + v2[1]]

def sub_vectors(v1, v2):
	return [v1[0] - v2[0], v1[1] - v2[1]]

def mult_scalar(v, s):
	return [v[0] * s, v[1] * s]

def limit_vector(vector, limit):
	mag = math.sqrt(vector[0]**2 + vector[1]**2)
	if(mag > limit):
		return [vector[0]*limit/mag, vector[1]*limit/mag]	
	else:
		return vector

def set_magnitude(vector, magnitude):
	mag = math.sqrt(vector[0]**2 + vector[1]**2)
	if(mag):
		return [vector[0] * magnitude / mag, vector[1] * magnitude / mag]
	else:
		return vector

class Boid:
	def __init__(self, width=500, height=500):
		self.windowWidth = width
		self.windowHeight = height
		self.position = [random.randint(0, width-1), random.randint(0, height-1)]
		self.velocity = random.sample(range(-10, 10), 2)
		self.acceleration = [0, 0]
		self.maxForce = 0.2
		self.maxSpeed = 2

	def edges(self):
		if(self.position[0] > self.windowWidth):
			self.position[0] = 0
		elif(self.position[0] < 0):
			self.position[0] = self.windowWidth

		if(self.position[1] > self.windowHeight):
			self.position[1] = 0
		elif(self.position[1] < 0):
			self.position[1] = self.windowHeight

	def align(self, boids):
		perceptionRadius = 100
		total = 0
		steering = [0, 0]
		for other in boids:
			d = dist(self.position[0], self.position[1], other.position[0], other.position[1])
			if(other != self and d < perceptionRadius):
				steering = add_vectors(steering, other.velocity)
				total += 1
		if(total > 0):
			steering[0] = steering[0]/total
			steering[1] = steering[1]/total
			steering = set_magnitude(steering, self.maxSpeed) 
			steering = sub_vectors(steering, self.velocity)
			steering = limit_vector(steering, self.maxForce)

		return steering

	def cohesion(self, boids):
		perceptionRadius = 100
		total = 0
		steering = [0, 0]
		for other in boids:
			d = dist(self.position[0], self.position[1], other.position[0], other.position[1])
			if(other != self and d < perceptionRadius):
				steering = add_vectors(steering, other.position)
				total += 1
		if(total > 0):
			steering[0] = steering[0]/total
			steering[1] = steering[1]/total
			steering = sub_vectors(steering, self.position)
			steering = set_magnitude(steering, self.maxSpeed)
			steering = sub_vectors(steering, self.velocity)
			steering = limit_vector(steering, self.maxForce)

		return steering

	def separation(self, boids):
		perceptionRadius = 100
		total = 0
		steering = [0, 0]
		for other in boids:
			d = dist(self.position[0], self.position[1], other.position[0], other.position[1])
			if(other != self and d < perceptionRadius):
				diff = sub_vectors(self.position, other.position)
				diff[0] = diff[0] / d**2
				diff[1] = diff[1] / d**2
				steering = add_vectors(steering, diff)
				total += 1

		if(total > 0):
			steering[0] = steering[0]/total
			steering[1] = steering[1]/total
			steering = set_magnitude(steering, self.maxSpeed)
			steering = sub_vectors(steering, self.velocity)
			steering = limit_vector(steering, self.maxForce)

		return steering

	def flock(self, boids, separationRatio, cohesionRatio, alignmentRatio):
		alignment = self.align(boids)
		cohesion = self.cohesion(boids)
		separation = self.separation(boids)

		separation = mult_scalar(separation, separationRatio)
		cohesion = mult_scalar(cohesion, cohesionRatio)
		alignment = mult_scalar(alignment, alignmentRatio)

		self.acceleration = add_vectors(self.acceleration, separation)
		self.acceleration = add_vectors(self.acceleration, alignment)
		self.acceleration = add_vectors(self.acceleration, cohesion)

	def update(self):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]

		self.velocity[0] += self.acceleration[0]
		self.velocity[1] += self.acceleration[1]

		self.velocity = limit_vector(self.velocity, self.maxSpeed)
		self.acceleration = [0, 0]

	def show(self, screen):
		pygame.draw.circle(screen, (0, 0, 0), self.position, 10, 0)

class Simulation:
	def __init__(self, height=500, width=500):
		self.windowHeight = height
		self.windowWidth = width
		self.attribute = 'separation'
		self.separationRatio = 0.5
		self.cohesionRatio = 0.5
		self.alignmentRatio = 0.5

	def on_execute(self):
		pygame.init()
		screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		pygame.display.set_caption("Boids - Flock Simulation")

		flock = []
		for i in range(50):
			b = Boid(width=self.windowWidth, height=self.windowHeight)
			flock.append(b)

		running = True
		font = pygame.font.Font('freesansbold.ttf', 32)
		separationText = font.render('Separation'+str(self.separationRatio), True, (0, 0, 0), (222, 222, 222))
		separationRect = separationText.get_rect()
		separationRect.center = (self.windowWidth - 150, self.windowHeight - 150)

		cohesionText = font.render('Cohesion '+str(self.cohesionRatio), True, (0, 0, 0), (222, 222, 222))
		cohesionRect = cohesionText.get_rect()
		cohesionRect.center = (self.windowWidth - 150, self.windowHeight - 100)

		alignmentText = font.render('Alignment  '+str(self.alignmentRatio), True, (0, 0, 0), (222, 222, 222))
		alignmentRect = alignmentText.get_rect()
		alignmentRect.center = (self.windowWidth - 150, self.windowHeight - 50)
		while running:
			screen.fill((255, 255, 255)) #rbg value
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_s:
						self.attribute = 'separation'
					if event.key == pygame.K_c:
						self.attribute = 'cohesion'
					if event.key == pygame.K_a:
						self.attribute = 'alignment'
					if event.key == pygame.K_UP:
						if self.attribute == 'separation':
							if(self.separationRatio <= 1):
								self.separationRatio += 0.1
								separationText = font.render('Separation '+str(self.separationRatio), True, (0, 0, 0), (222, 222, 222))
						elif self.attribute == 'cohesion':
							if(self.cohesionRatio <= 1):
								self.cohesionRatio += 0.1
								cohesionText = font.render('Cohesion '+str(self.cohesionRatio), True, (0, 0, 0), (222, 222, 222))
						elif self.attribute == 'alignment':
							if(self.alignmentRatio <= 1):
								self.alignmentRatio += 0.1
								alignmentText = font.render('Alignment  '+str(self.alignmentRatio), True, (0, 0, 0), (222, 222, 222))
					if event.key == pygame.K_DOWN:
						if self.attribute == 'separation':
							if(self.separationRatio >= 0):
								self.separationRatio -= 0.1
								separationText = font.render('Separation '+str(self.separationRatio), True, (0, 0, 0), (222, 222, 222))
						elif self.attribute == 'cohesion':
							if(self.cohesionRatio >= 0):
								self.cohesionRatio -= 0.1
								cohesionText = font.render('Cohesion '+str(self.cohesionRatio), True, (0, 0, 0), (222, 222, 222))
						elif self.attribute == 'alignment':
							if(self.alignmentRatio >= 0):
								self.alignmentRatio -= 0.1
								alignmentText = font.render('Alignment  '+str(self.alignmentRatio), True, (0, 0, 0), (222, 222, 222))

			for boid in flock:
				boid.edges()
				boid.flock(flock, self.separationRatio, self.cohesionRatio, self.alignmentRatio)
				boid.update()
				boid.show(screen)

			screen.blit(separationText, separationRect)
			screen.blit(cohesionText, cohesionRect)
			screen.blit(alignmentText, alignmentRect)

			pygame.display.update()

if __name__ == '__main__':
	simulator = Simulation(width=800, height=800)
	simulator.on_execute()