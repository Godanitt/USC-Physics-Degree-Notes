import cv2
import pytesseract
import pandas as pd

VIDEO_PATH = "IMG_0589.MOV"

# ==== Configuración ====
INICIO_SEGUNDOS = 4*60+10
DURACION_SEGUNDOS = 1*3600+31*60+23
ROI = (840, 878, 1037, 1132)  # y1:y2, x1:x2 ajustado para el contador central
# ========================

cap = cv2.VideoCapture(VIDEO_PATH)


if not cap.isOpened():
    print("❌ No se pudo abrir el video.")
    exit()
    
fps = cap.get(cv2.CAP_PROP_FPS)
inicio_frame = int(INICIO_SEGUNDOS * fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, inicio_frame)
m=0.1
for i in range(0,int((DURACION_SEGUNDOS-INICIO_SEGUNDOS)//m),1):
    ret, frame = cap.read()
    if not ret:
        print(f"⚠️ No se pudo leer el frame en el segundo {INICIO_SEGUNDOS + i*m}")
        continue

    y1, y2, x1, x2 = ROI
    roi = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inverted, (7, 7), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.resize(thresh, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

    print(f"✅ Guardado frame en segundo {INICIO_SEGUNDOS + i}")
    cv2.imwrite(f"Geiger-2/ocr_input_{INICIO_SEGUNDOS + i}s.png", thresh)

    # Saltamos al siguiente segundo
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + fps*m - 1)
