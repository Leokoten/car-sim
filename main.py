import pygame
import time
from utils import scale_image
from car import Car

TRACK = scale_image(pygame.image.load('assets/forest-track.png'), 0.75)
WHITE_CAR = scale_image(pygame.image.load('assets/white-car.png'), 0.8)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Simulador de Carro')

FPS = 60

def draw(win, images):
  for img, pos in images:
    win.blit(img, pos)

  car.draw(win)
  pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(TRACK, (0, 0))]
car = Car(4, 4, WHITE_CAR, (423, 800))

while run:
  clock.tick(FPS)

  draw(WIN, images)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      break

  keys = pygame.key.get_pressed()
  moved = False

  if keys[pygame.K_a]:
    car.rotate(left=True)
  if keys[pygame.K_d]:
    car.rotate(right=True)
  if keys[pygame.K_w]:
    moved = True
    car.move_forward()
  if keys[pygame.K_s]:
    moved = True
    car.move_backwards()

  if not moved:
    if car.last_moved_forward:
      car.reduce_speed()
    else:
      car.reduce_speed_back()
    

pygame.quit()