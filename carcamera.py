import pygame
import cv2
import numpy as np

from utils import scale_image
from car import Car  # Certifique-se de ter a classe Car definida em seu arquivo car.py

TRACK = scale_image(pygame.image.load('assets/forest-track.png'), 0.75)
WHITE_CAR = scale_image(pygame.image.load('assets/white-car.png'), 0.8)
ip = "192.168.100.37"
camera_url = f"http://{ip}:4747/video"
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Simulador de Carro')

FPS = 120

class CameraControlledCar:
    def __init__(self, x, y, image, start_position):
        self.car = Car(x, y, image, start_position)
        self.cap = cv2.VideoCapture(camera_url)

    def process_camera_input(self):
        ret, frame = self.cap.read()

        if not ret or frame is None:
            print("Erro ao capturar o frame da câmera.")
            return

        low_b = np.uint8([5, 5, 5])
        high_b = np.uint8([0, 0, 0])
        mask = cv2.inRange(frame, high_b, low_b)
        contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            if M["m00"] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                print("CX: " + str(cx) + "  CY: " + str(cy))

                if cx >= 450:
                    print("VIRA ESQUERDA")
                    self.car.rotate(left=True)
                elif 290 <= cx < 450:
                    print("VAI RETO!")
                    self.car.move_forward()
                elif cx < 290:
                    print("VIRA DIREITA")
                    self.car.rotate(right=True)
            else:
                print("PERDI A LINHA!")
        else:
            print("NENHUM CONTORNO ENCONTRADO")

        cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
        cv2.imshow("Frame", frame)


    def draw(self, win, images):
        for img, pos in images:
            win.blit(img, pos)
        self.car.draw(win)
        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        images = [(TRACK, (0, 0))]

        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.process_camera_input()
            self.draw(WIN, images)

        self.cap.release()
        pygame.quit()

# Inicie a instância da classe CameraControlledCar com os parâmetros apropriados
car_with_camera = CameraControlledCar(3, 3, WHITE_CAR, (423, 800))
car_with_camera.run()
