from utils import blit_rotate_center
import math

class Car:
  def __init__(self, max_vel, rotation_vel, img, start_pos):
    self.img = img

    self.max_vel = max_vel
    self.vel = 0

    self.rotation_vel = rotation_vel
    self.angle = 0

    self.start_pos = start_pos
    self.x, self.y = start_pos

    self.acceleration = 0.1
    
    self.last_moved_forward = True

  def rotate(self, left=False, right=False):
    if left:
      self.angle += self.rotation_vel
    elif right:
      self.angle -= self.rotation_vel

  def draw(self, win):
    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

  def move_forward(self):
    self.last_moved_forward = True
    self.vel = min(self.vel + self.acceleration, self.max_vel)
    self.move()

  def move(self, reverse=False):
    radians = math.radians(self.angle)
    vertical = math.cos(radians) * self.vel
    horizontal = math.sin(radians) * self.vel

    self.y += vertical if reverse else -vertical
    self.x += horizontal if reverse else -horizontal

  def move_backwards(self):
    self.last_moved_forward = False
    self.vel = min(self.vel + self.acceleration, self.max_vel)
    self.move(reverse=True)

  def reduce_speed(self):
    self.vel = max(self.vel - self.acceleration / 2, 0)
    self.move()

  def reduce_speed_back(self):
    self.vel = max(self.vel - self.acceleration / 2, 0)
    self.move(reverse=True)