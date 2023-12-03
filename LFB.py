import cv2
import numpy as np
import requests
import time


ip = "192.168.100.37"
camera_url = f"http://{ip}:4747/video"
cap = cv2.VideoCapture(camera_url)

max_tentativas_re = 5  # Ajuste conforme necessário
tentativas_restantes = max_tentativas_re
pause = False
modo_manual = False

while True:
    if not pause:
        ret, frame = cap.read()
        low_b = np.uint8([5, 5, 5])
        high_b = np.uint8([0, 0, 0])
        mask = cv2.inRange(frame, high_b, low_b)
        contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

        if not modo_manual:
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)

                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    print("CX: " + str(cx) + "  CY: " + str(cy))

                    if cx >= 450:
                        print("VIRA ESQUERDA")
                        tentativas_restantes = max_tentativas_re
                        # requests.get(f'http://{ip}/on?m=3')
                    elif 290 <= cx < 450:
                        print("VAI RETO!")
                        tentativas_restantes = max_tentativas_re
                        # requests.get(f'http://{ip}/on?m=1')
                    elif cx < 290:
                        print("VIRA DIREITA")
                        tentativas_restantes = max_tentativas_re
                        # requests.get(f'http://{ip}/on?m=4')

                    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
            else:
                print("PERDI A LINHA!")
                if tentativas_restantes > 0:
                    print(f"Tentativas restantes: {tentativas_restantes}")
                    # requests.get(f'http://{ip}/on?m=2')
                    tentativas_restantes -= 1
                else:
                    print("Número máximo de tentativas alcançado. Parando.")
                    # requests.get(f'http://{ip}/on?m=0')

            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
            cv2.imshow("Mask", mask)
            cv2.imshow("Frame", frame)
        else:  # Modo manual
            key = cv2.waitKey(1) & 0xff
            if key == ord('w'):
                print("MOVIMENTO PARA FRENTE")
                # requests.get(f'http://{ip}/on?m=1')
            elif key == ord('a'):
                print("VIRA PARA A ESQUERDA")
                # requests.get(f'http://{ip}/on?m=4')
            elif key == ord('s'):
                print("MOVIMENTO PARA TRÁS")
                # requests.get(f'http://{ip}/on?m=2')
            elif key == ord('d'):
                print("VIRA PARA A DIREITA")
                # requests.get(f'http://{ip}/on?m=3')

    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):   # 1 is the time in ms
        # requests.get(f'http://{ip}/on?m=0')
        break
    elif key == ord('p'):
        # requests.get(f'http://{ip}/on?m=0') 
        pause = not pause
        print(f"O código está {'pausado' if pause else 'retomado'}.")
    elif key == ord('m'):
        modo_manual = not modo_manual
        print(f"Modo Manual está {'ativado' if modo_manual else 'desativado'}.")

cap.release()
cv2.destroyAllWindows()