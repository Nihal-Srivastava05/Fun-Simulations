import pygame
import random
from Assets.Button import Button, TextButton

def partition(L, p, q):
	L[p], L[q] = L[q], L[p]
	pivot = q
	i = p - 1
	for j in range(p, q+1):
		if(L[j] < L[pivot]):
			i += 1
			L[i], L[j] = L[j], L[i]

	L[i+1], L[q] = L[q], L[i+1]

	return i+1

def merge(A, p, m, r):
	n1 = m - p + 1
	n2 = r - m
	L = [0]*n1
	R = [0]*n2
	for i in range(n1):
		L[i] = A[p+i]

	for j in range(n2):
		R[j] = A[m + 1 + j]

	i = 0
	j = 0
	k = p
	while(i < n1 and j < n2):
		if(L[i] <= R[j]):
			A[k] = L[i]
			i += 1
		else:
			A[k] = R[j]
			j += 1
		k += 1

	while(i < n1):
		A[k] = L[i]
		i += 1
		k += 1
	while(j < n2):
		A[k] = R[j]
		j += 1
		k += 1

def getNextGap(gap):
    gap = (gap * 10)//13
    if gap < 1:
        return 1
    return gap

class Visulization():

	def __init__(self, limit=100, waitTime=100):
		self.limit = limit
		self.iteration_num = 0
		L = list(range(0, limit))
		random.shuffle(L)
		self.L = L
		self.waitTime = waitTime

	def bubbleSort(self, display):
		for i in range(len(self.L)):
			for j in range(len(self.L)-1-i):
				if self.L[j] > self.L[j+1]:
					self.L[j], self.L[j+1] = self.L[j+1], self.L[j]
			res = self.draw_grid(display)

		res = self.draw_grid(display)
		if(not res):
			return False

	def selectionSort(self, display):
		for i in range(len(self.L) - 1):
			imin = i
			for j in range(i + 1, len(self.L)):
				if(self.L[j] < self.L[imin]):
					imin = j
			if(imin != i):
				self.L[i], self.L[imin] = self.L[imin], self.L[i]
			res = self.draw_grid(display)

		res = self.draw_grid(display)
		if(not res):
			return False

	def insertionSort(self, display):
		for i in range(len(self.L)):
			currentNum = self.L[i]
			j = i
			while(self.L[j-1] > currentNum and j>0):
				self.L[j] = self.L[j-1]
				j -= 1
			self.L[j] = currentNum
			res = self.draw_grid(display)
		
		res = self.draw_grid(display)
		if(not res):
			return False

	def quickSort(self, display, p, q):
		if(p<q):
			r = partition(self.L, p, q);
			res = self.draw_grid(display)
			self.quickSort(display, p, r-1)
			res = self.draw_grid(display)
			self.quickSort(display, r+1, q)
		res = self.draw_grid(display)
		if(not res):
			return False

	def mergeSort(self, display, l, r):
		if(r > l):
			m = (l + r) // 2
			res = self.draw_grid(display)
			self.mergeSort(display, l, m)
			res = self.draw_grid(display)
			self.mergeSort(display, m+1, r)
			merge(self.L, l, m, r)
		res = self.draw_grid(display)
		if(not res):
			return False

	def combSort(self, display):
		n = len(self.L)
		gap = n
		swapped = True

		while gap !=1 or swapped == 1:
			gap = getNextGap(gap)
			swapped = False
			for i in range(0, n-gap):
				if self.L[i] > self.L[i + gap]:
					self.L[i], self.L[i + gap] = self.L[i + gap], self.L[i]
					swapped = True
			res = self.draw_grid(display)

		res = self.draw_grid(display)
		if(not res):
			return False

	def shellSort(self, display):
		n = len(self.L)
		gap=n//2  
		while gap>0:
			j=gap
			while j < n:
				i=j-gap
				while i >= 0:
					if self.L[i+gap]>self.L[i]:
						break
					else:
						self.L[i+gap],self.L[i]=self.L[i],self.L[i+gap]
					i=i-gap 
				j+=1
			
			res = self.draw_grid(display)
			gap=gap//2

		res = self.draw_grid(display)
		if(not res):
			return False

	def draw_grid(self, display):
		display.fill((255, 255, 255))
		for i in range(self.limit):
			pygame.draw.rect(display, (0, 0, 0), (i*5, 0, 5, self.L[i]*5))
		pygame.display.update()
		pygame.time.wait(self.waitTime)
		if(self.L == list(range(0, self.limit))):
			return False

		return True


class SortingAlgoViz():

	def __init__(self, height=500, width=500):
		self.windowHeight = height
		self.windowWidth = width
		self.algo = 'bubbleSort'

	def on_execute(self):
		pygame.init()
		screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		pygame.display.set_caption("Sorting Algorithm Visulization")
		visu = Visulization()
		running = True
		while running:
			screen.fill((255, 255, 255))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			if self.algo == 'bubbleSort':
				end = visu.bubbleSort(screen)
			elif self.algo == 'selectionSort':
				end = visu.selectionSort(screen)
			elif self.algo == 'insertionSort':
				end = visu.insertionSort(screen)
			elif self.algo == 'quickSort':
				end = visu.quickSort(screen, 0, 99)
			elif self.algo == 'mergeSort':
				end = visu.mergeSort(screen, 0, 99)
			elif self.algo == 'combSort':
				end = visu.combSort(screen)
			elif self.algo == 'shellSort':
				end = visu.shellSort(screen)

			pygame.display.update()

			if(not end):
				running = False
				self.start_menu()

	def start_menu(self):
		pygame.init()
		screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		pygame.display.set_caption("Start Menu")

		start_img = pygame.image.load('Assets/start.png').convert_alpha()
		start_button = Button(150, 10, start_img, 0.4)

		bubbleSort_button = TextButton(100, 300, "Bubble Sort", bg_color=(230, 240, 10))
		selectionSort_button = TextButton(120, 350, "Selection Sort")
		insertionSort_button = TextButton(120, 400, "Insertion Sort")
		quickSort_button = TextButton(95, 450, "Quick Sort")
		
		mergeSort_button = TextButton(400, 300, "Merge Sort")
		combSort_button = TextButton(400, 350, "Comb Sort")
		shellSort_button = TextButton(400, 400, "Shell Sort")

		running = True
		while running:
			screen.fill((255, 255, 255))
			
			if start_button.draw(screen):
				running = False
				self.on_execute()

			if bubbleSort_button.draw(screen):
				self.algo = "bubbleSort"
				bubbleSort_button.change_bg_color((230, 240, 10))
				selectionSort_button.change_bg_color((235, 235, 235))
				insertionSort_button.change_bg_color((235, 235, 235))
				quickSort_button.change_bg_color((235, 235, 235))
				mergeSort_button.change_bg_color((235, 235, 235))
				combSort_button.change_bg_color((235, 235, 235))
				shellSort_button.change_bg_color((235, 235, 235))

			if selectionSort_button.draw(screen):
				self.algo = "selectionSort"
				bubbleSort_button.change_bg_color((235, 235, 235))
				selectionSort_button.change_bg_color((230, 240, 10))
				insertionSort_button.change_bg_color((235, 235, 235))
				quickSort_button.change_bg_color((235, 235, 235))
				mergeSort_button.change_bg_color((235, 235, 235))
				combSort_button.change_bg_color((235, 235, 235))
				shellSort_button.change_bg_color((235, 235, 235))

			if insertionSort_button.draw(screen):
				self.algo = "insertionSort"
				bubbleSort_button.change_bg_color((235, 235, 235))
				selectionSort_button.change_bg_color((235, 235, 235))
				insertionSort_button.change_bg_color((230, 240, 10))
				quickSort_button.change_bg_color((235, 235, 235))
				mergeSort_button.change_bg_color((235, 235, 235))
				combSort_button.change_bg_color((235, 235, 235))
				shellSort_button.change_bg_color((235, 235, 235))

			if quickSort_button.draw(screen):
				self.algo = "quickSort"
				bubbleSort_button.change_bg_color((235, 235, 235))
				selectionSort_button.change_bg_color((235, 235, 235))
				insertionSort_button.change_bg_color((235, 235, 235))
				quickSort_button.change_bg_color((230, 240, 10))
				mergeSort_button.change_bg_color((235, 235, 235))
				combSort_button.change_bg_color((235, 235, 235))
				shellSort_button.change_bg_color((235, 235, 235))

			if mergeSort_button.draw(screen):
				self.algo = "mergeSort"
				bubbleSort_button.change_bg_color((235, 235, 235))
				selectionSort_button.change_bg_color((235, 235, 235))
				insertionSort_button.change_bg_color((235, 235, 235))
				quickSort_button.change_bg_color((235, 235, 235))
				mergeSort_button.change_bg_color((230, 240, 10))
				combSort_button.change_bg_color((235, 235, 235))
				shellSort_button.change_bg_color((235, 235, 235))

			if combSort_button.draw(screen):
				self.algo = "combSort"
				bubbleSort_button.change_bg_color((235, 235, 235))
				selectionSort_button.change_bg_color((235, 235, 235))
				insertionSort_button.change_bg_color((235, 235, 235))
				quickSort_button.change_bg_color((235, 235, 235))
				mergeSort_button.change_bg_color((235, 235, 235))
				combSort_button.change_bg_color((230, 240, 10))
				shellSort_button.change_bg_color((235, 235, 235))

			if shellSort_button.draw(screen):
				self.algo = "shellSort"
				bubbleSort_button.change_bg_color((235, 235, 235))
				selectionSort_button.change_bg_color((235, 235, 235))
				insertionSort_button.change_bg_color((235, 235, 235))
				quickSort_button.change_bg_color((235, 235, 235))
				mergeSort_button.change_bg_color((235, 235, 235))
				combSort_button.change_bg_color((235, 235, 235))
				shellSort_button.change_bg_color((230, 240, 10))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			pygame.display.update()

if __name__ == '__main__':
	simulator = SortingAlgoViz()
	simulator.start_menu()
