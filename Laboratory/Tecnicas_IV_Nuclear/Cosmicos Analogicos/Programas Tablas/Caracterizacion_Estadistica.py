import cv2
import pytesseract
import pandas as pd
import os

# Parámetros configurables
VIDEO_PATH = 'Video.mp4'  # Cambia esto al nombre de tu video
FRAME_INTERVAL = 10       # Intervalo en segundos (puedes poner 1, 2, 5, 10, etc.)
OUTPUT_CSV = 'Lecturas.csv'

# Coordenadas aproximadas de las 3 pantallas (ajustar según tu video)
# Formato: (x, y, w, h)
DISPLAY_COORDS = {
    'izquierda': (140, 90, 90, 40),
    'centro':    (330, 90, 90, 40),
    'derecha':   (520, 90, 90, 40)
}

# Preprocesamiento de imagen para mejorar OCR
def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    return thresh

# OCR personalizado para números rojos sobre fondo negro
def extract_digits(image):
    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(image, config=config)
    return ''.join(filter(str.isdigit, text))

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * FRAME_INTERVAL)
    
    data = []
    frame_count = 0
    success, frame = cap.read()
    
    while success:
        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps

            readings = {'tiempo_s': round(timestamp, 2)}

            for name, (x, y, w, h) in DISPLAY_COORDS.items():
                roi = frame[y:y+h, x:x+w]
                roi_proc = preprocess(roi)
                valor = extract_digits(roi_proc)
                readings[name] = valor if valor else None

            data.append(readings)

        success, frame = cap.read()
        frame_count += 1

    cap.release()
    
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Datos guardados en {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

