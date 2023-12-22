import cv2
import mediapipe as mp 
from pynput.mouse import Button, Controller
import pyautogui
import math

mouse = Controller()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5)

vid = cv2.VideoCapture(0)

width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

(screen_width,screen_height) = pyautogui.size()

tipIds = [4,8,12,16,20]

pinch = False

#função para contar os dedos abertos na mão >=)
def count_fingers(image,hand_landmarks,handNo = 0):
    global pinch
    if hand_landmarks:
        landmarks = hand_landmarks[handNo].landmark
    #obter os pontos de referência da primeira mão visível 
        fingers = []
        for lm_index in tipIds :
            fingerTipY = landmarks [lm_index].y
            fingerBottomY = landmarks [lm_index -2].y
            thumbTipX = landmarks [4].x
            thumbBottomX = landmarks [2].x
            if lm_index != 4: 
                if fingerTipY < fingerBottomY:
                    fingers.append(1)
                if fingerTipY > fingerBottomY:
                    fingers.append(0)
            else:
                if thumbTipX < thumbBottomX:
                    fingers.append(1)
                if thumbTipX > thumbBottomX:
                    fingers.append(0)


        #contanto o total de dedos abertos
        total_fingers = fingers.count(1)
        # text = f"Dedos: {total_fingers}"
        # cv2.putText(image, text, (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
   
        # PINÇA

        #Bruna
		# Desenhe uma LINHA entre a PONTA DO DEDO e a PONTA DO POLEGAR
        fingerTipX = int((landmarks[8].x) * width)
        fingerTipY = int((landmarks[8].y) * height)
        thumbTipX = int((landmarks[4].x) * width)
        thumbTipY = int((landmarks[4].y) * height)

        cv2.line(image, (fingerTipX, fingerTipY), (thumbTipX, thumbTipY), (255,255,255), 2)

		# Desenhe um CÍRCULO no CENTRO da LINHA entre a PONTA DO DEDO e a PONTA DO POLEGAR
        centerX = int((fingerTipX + thumbTipX)/2)
        centerY = int((fingerTipY + thumbTipY)/2)

        cv2.circle(image, (centerX, centerY), 2, (0,0,255), 2)
		
        #Roberta
		# Calcule a DISTÂNCIA entre a PONTA DO DEDO e a PONTA DO POLEGAR
		# D = v[(x2-x1)² + (y2-y1)²]
        distance = math.sqrt(((fingerTipX-thumbTipX)**2) + ((fingerTipY-thumbTipY)**2))
        #print(distance)
        
		# Defina a posição do mouse na tela em relação ao tamanho da janela de resultado
        relative_mouse_x = (centerX/width)*screen_width
        relative_mouse_y = (centerY/height)*screen_height
        mouse.position = (relative_mouse_x, relative_mouse_y)

        #Marcos
		# Verifique as condições de formação da PINÇA
        if distance > 40 :
            if pinch == True:
                pinch = False
                mouse.release(Button.left)
    
        if distance <= 40 :
            if pinch == False:
                pinch = True
                mouse.press(Button.left)
        print(pinch)

        
        


def drawHandLandmarks(image, hand_landmarks):
    if hand_landmarks:
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
    #desenhe as conexões entre os pontos de referência

while True:
    success, frame = vid.read()

    frame = cv2.flip(frame,1)

    #Detectando os pontos de referência das mãos
    results = hands.process(frame)

    #Obtendo a posição do ponto de referência 
    hand_landmarks = results.multi_hand_landmarks

    #desenhando os pontos nas mãos
    drawHandLandmarks(frame,hand_landmarks )
    
    #contando os dedos
    count_fingers(frame,hand_landmarks)

    cv2.imshow("Maos",frame)

    key = cv2.waitKey(1)

    # 27 tecla esc
    # 32 tecla espaço
    if key == 27:
        break

cv2.destroAllWindows()