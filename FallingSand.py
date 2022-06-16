import pygame
import random

def pixelToIndex(pos):
    return [pos[0]//10, pos[1]//10]

class Container:
    def __init__(self, dimensions):
        self.n = dimensions[0] // 10
        self.m = dimensions[1] // 10
        self.grid = []
        for i in range(self.m):
            row = []
            for j in range(self.n):
                row.append(0)
            self.grid.append(row)
    
    def get_limit(self):
        return (self.n, self.m)
    
    def get_index(self, pos):
        return [pos[0]//10, pos[1]//10]

    def get_cell_status(self, pos):
        return self.grid[pos[0]//10][pos[1]//10]
    
    def update_grid(self, sand_pos, value):
        self.grid[sand_pos[0]][sand_pos[1]] = value
    
    def draw_grid(self, display):
        for i in range(self.n):
            for j in range(self.m):
                if(self.grid[i][j] == 1):
                    pygame.draw.rect(display, (255, 220, 39), (i*10, j*10, 10, 10))
                if(self.grid[i][j] == 2):
                    pygame.draw.rect(display, (0, 0, 0), (i*10, j*10, 10, 10))
                if(self.grid[i][j] == 3):
                    pygame.draw.rect(display, (36, 232, 255), (i*10, j*10, 10, 10))
                if(self.grid[i][j] == 4):
                    pygame.draw.rect(display, (190, 190, 190), (i*10, j*10, 10, 10))
        pygame.time.wait(100)

class Sand_Collection:
    particles = []
    def add_particles(self, index, container):
        self.particles.append(index)
        container.update_grid(index, 1)

    def redraw_particle(self, container, water_container):
        max_limit = container.get_limit()
        for particle in self.particles:
            if(particle[0]+1 > max_limit[0]-1 or particle[1]+1 > max_limit[1]-1 or particle[0]-1 < 0 or particle[1]-1 < 0):
                continue
            else:
                container.update_grid(particle, 0)
                if(container.grid[particle[0]][particle[1]+1] == 0):
                    particle[1] += 1
                elif(container.grid[particle[0]][particle[1]+1] == 3):
                    water_container.update_particle_pos([particle[0],particle[1]+1], [particle[0],particle[1]])
                    particle[1] += 1
                else:
                    if((container.grid[particle[0] - 1][particle[1] + 1] == 0) and (container.grid[particle[0] + 1][particle[1] + 1])):
                        particle[1] += 1
                        particle[0] = random.choice([particle[0]+1, particle[0]-1])
                    elif(container.grid[particle[0] - 1][particle[1] + 1] == 0):
                        particle[1] += 1
                        particle[0] -= 1
                    elif(container.grid[particle[0] + 1][particle[1] + 1] == 0):
                        particle[0] += 1
                        particle[1] += 1
                container.update_grid(particle, 1)

class Stone_Collection:
    particles = []
    def add_particles(self, index, container):
        self.particles.append(index)
        container.update_grid(index, 2)

class Water_Collection:
    particles = []
    def add_particles(self, index, container):
        self.particles.append(index)
        container.update_grid(index, 3)

    def update_particle_pos(self, old_pos, new_pos):
        index_old_particle = self.particles.index(old_pos)
        self.particles[index_old_particle] = new_pos

    def redraw_particle(self, container):
        max_limit = container.get_limit()
        for particle in self.particles:
            if(particle[0]+1 > max_limit[0]-1 or particle[1]+1 > max_limit[1]-1 or particle[0]-1 < 0 or particle[1]-1 < 0):
                continue
            else:
                container.update_grid(particle, 0)
                if(container.grid[particle[0]][particle[1]+1] == 0):
                    particle[1] += 1
                else:
                    if((container.grid[particle[0] - 1][particle[1] + 1] == 0) and (container.grid[particle[0] + 1][particle[1] + 1])):
                        particle[1] += 1
                        particle[0] = random.choice([particle[0]+1, particle[0]-1])
                    elif(container.grid[particle[0] - 1][particle[1] + 1] == 0):
                        particle[1] += 1
                        particle[0] -= 1
                    elif(container.grid[particle[0] + 1][particle[1] + 1] == 0):
                        particle[0] += 1
                        particle[1] += 1
                    else:
                        if((container.grid[particle[0] + 1][particle[1]] == 0) and (container.grid[particle[0] - 1][particle[1]] == 0)):
                            index1 = 1
                            while( (particle[0]+index1 < max_limit[0]-1) and (container.grid[particle[0]+index1][particle[1]+1] != 0) ):
                                index1 += 1

                            index2 = 1
                            while( (particle[0]-index2 > 0) and (container.grid[particle[0]-index2][particle[1]+1] != 0)):
                                index2 += 1
                            if(index1 < abs(index2)):
                                particle[0] += 1
                            else:
                                particle[0] -= 1
                        elif(container.grid[particle[0] + 1][particle[1]] == 0):
                                particle[0] += 1
                        elif(container.grid[particle[0] - 1][particle[1]] == 0):
                                particle[0] -= 1
                container.update_grid(particle, 3)

class Smoke_Collection:
    particles = []
    def add_particles(self, index, container):
        self.particles.append(index)
        container.update_grid(index, 4)
    
    def redraw_particle(self, container, water_container):
        max_limit = container.get_limit()
        for particle in self.particles:
            if(particle[0]+1 > max_limit[0]-1 or particle[1]+1 > max_limit[1]-1 or particle[0]-1 < 0 or particle[1]-1 < 0):
                continue
            else:
                container.update_grid(particle, 0)
                if(container.grid[particle[0]][particle[1]-1] == 0):
                    particle[1] -= 1
                elif(container.grid[particle[0]][particle[1]-1] == 3):
                    water_container.update_particle_pos([particle[0],particle[1]-1], [particle[0],particle[1]])
                    particle[1] -= 1
                else:
                    if((container.grid[particle[0] - 1][particle[1] - 1] == 0) and (container.grid[particle[0] + 1][particle[1] - 1])):
                        particle[1] -= 1
                        particle[0] = random.choice([particle[0]+1, particle[0]-1])
                    elif(container.grid[particle[0] - 1][particle[1] - 1] == 0):
                        particle[1] -= 1
                        particle[0] -= 1
                    elif(container.grid[particle[0] + 1][particle[1] - 1] == 0):
                        particle[0] += 1
                        particle[1] -= 1
                    else:
                        if((container.grid[particle[0] + 1][particle[1]] == 0) and (container.grid[particle[0] - 1][particle[1]] == 0)):
                            index1 = 1
                            while( (particle[0]+index1 < max_limit[0]-1) and (container.grid[particle[0]+index1][particle[1]-1] != 0) ):
                                index1 += 1
                            index2 = 1
                            while( (particle[0]-index2 > 0) and (container.grid[particle[0]-index2][particle[1]-1] != 0)):
                                index2 += 1
                            if(index1 < index2):
                                particle[0] += 1
                            else:
                                particle[0] -= 1
                        elif(container.grid[particle[0] + 1][particle[1]] == 0):
                                particle[0] += 1
                        elif(container.grid[particle[0] - 1][particle[1]] == 0):
                                particle[0] -= 1
                container.update_grid(particle, 4)

class Simulate_Cellular_Automaton:
    def __init__(self, height=500, width=500):
        self.windowHeight = height
        self.windowWidth = width
        self.material_type = 1
    
    def on_execute(self):
        pygame.init()
        screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption("Falling Sand - Cellular Automata")
        container = Container((self.windowWidth, self.windowHeight))
        sand_collection = Sand_Collection()
        stone_collection = Stone_Collection()
        water_collection = Water_Collection()
        smoke_collection = Smoke_Collection()
        running = True
        while running:
            screen.fill((255, 255, 255)) #rbg value
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.material_type = 1
                    if event.key == pygame.K_b:
                        self.material_type = 2
                    if event.key == pygame.K_w:
                        self.material_type = 3
                    if event.key == pygame.K_g:
                        self.material_type = 4

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    index = pixelToIndex(pos)
                    if(self.material_type == 1):
                        sand_collection.add_particles(index, container)
                    if(self.material_type == 2):
                        stone_collection.add_particles(index, container)
                    if(self.material_type == 3):
                        water_collection.add_particles(index, container)
                    if(self.material_type == 4):
                        smoke_collection.add_particles(index, container)
            
            water_collection.redraw_particle(container)
            sand_collection.redraw_particle(container, water_collection)
            smoke_collection.redraw_particle(container, water_collection)
            container.draw_grid(screen)
            pygame.display.update()

if __name__ == '__main__':
    simulator = Simulate_Cellular_Automaton()
    simulator.on_execute()