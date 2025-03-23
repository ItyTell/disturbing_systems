import threading
import time
import pygame
from math import sin, cos, pi 
from random import random

n = 5

class Philosopher(threading.Thread):
    running = True
    forks_semaphores = [threading.Semaphore(1) for _ in range(n)]
    mutex = threading.Semaphore(n-1)
    eating = [0] * n
    hunger_cooldown = 1 
    eating_time = 5
    
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.index = number
        self.left_fork = self.index
        self.right_fork = (self.index + 1) % n
    
    def run(self):
        while self.running:
            time.sleep(self.hunger_cooldown)
            print(f'Філософ {self.index} розмовляє')
            self.hunt()
    
    def hunt(self):
        while self.running:
            self.mutex.acquire()
            
            if self.forks_semaphores[self.left_fork].acquire(blocking=False):
                time.sleep(random() * 0.5)
                
                if self.forks_semaphores[self.right_fork].acquire(blocking=False):
                    self.mutex.release()
                    self.eat()
                    
                    self.forks_semaphores[self.right_fork].release()
                    self.forks_semaphores[self.left_fork].release()
                    return
                else:
                    self.forks_semaphores[self.left_fork].release()
            
            self.mutex.release()
            time.sleep(random() * 0.2)
    
    def eat(self):
        print(f'Філософ {self.index} почав їсти')
        self.eating[self.index] = 1
        time.sleep(self.eating_time)
        self.eating[self.index] = 0 
        print(f'Філософ {self.index} наївся')

def is_fork_available(fork_index):
    if Philosopher.forks_semaphores[fork_index].acquire(blocking=False):
        Philosopher.forks_semaphores[fork_index].release()
        return True
    return False

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Philosophers with Semaphores')
clock = pygame.time.Clock()
run = True
fps = 10

fork = pygame.image.load('pictures/fork.jpg')
fork = pygame.transform.scale(fork, (50, 50))
forks_g = []
forks_r = []

for i in range(n):
    fork1 = pygame.transform.rotate(fork, 180 + 360 * i / n)
    fork2 = pygame.transform.rotate(fork, 180 + 360 * i / n)
    fork_rect1 = fork1.get_rect(center=(300 - 100 * sin(2 * pi * i / n), 300 - 100 * cos(2 * pi * i / n)))
    green = (0, 255, 0)
    red = (255, 0, 0)
    fork1.fill(green, None, pygame.BLEND_RGB_MULT)
    fork2.fill(red, None, pygame.BLEND_RGB_MULT)
    forks_g.append((fork1, fork_rect1))
    forks_r.append((fork2, fork_rect1))

def update():
    screen.fill('white')
    pygame.draw.circle(surface=screen, color='brown', center=(300, 300), radius=150)
    
    for i in range(n):
        fork = forks_r[i][0]
        if is_fork_available(i):
            fork = forks_g[i][0]
        screen.blit(fork, forks_g[i][1])
    
    for i in range(n):
        color = 'blue'
        if Philosopher.eating[i]:
            color = 'red'
        pygame.draw.circle(surface=screen, color=color, 
                          center=(300 - 150 * sin(2 * pi * i / n + pi / n), 
                                 300 - 150 * cos(2 * pi * i / n + pi / n)), 
                          radius=20, width=0)
    
    pygame.display.update()

philosophers = [Philosopher(i) for i in range(n)]
Philosopher.running = True 
for philosopher in philosophers:
    philosopher.start()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            Philosopher.running = False
    
    update()
    clock.tick(fps)

for philosopher in philosophers:
    philosopher.join()

pygame.quit()