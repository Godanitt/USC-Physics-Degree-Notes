import cv2
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model
from pathlib import Path
import re



# -------------------------------
# Función para segmentar una imagen
# -------------------------------
def segmentar_digitos(ruta_imagen):
    img = cv2.imread(str(ruta_imagen), cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"❌ Error: No se pudo cargar la imagen: {ruta_imagen}")
        return []

    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    limpio = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    procesado = cv2.bitwise_not(cv2.dilate(cv2.bitwise_not(limpio), kernel, iterations=1))
    contornos, _ = cv2.findContours(procesado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[0])
    digitos = []
    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        if h > 15 and w > 5:
            roi = procesado[y:y+h, x:x+w]
            digit = cv2.resize(roi, (28, 28)).astype("float32") / 255.0
            digitos.append(digit.reshape(28, 28, 1))
    return np.array(digitos)

# -------------------------------
# Cargar el CSV y construir la lista de rutas y etiquetas
# -------------------------------
df = pd.read_csv('Lecturas_geiger.csv')

datos = []
for _, fila in df.iterrows():
    if pd.isna(fila['Tiempo']) or pd.isna(fila['Valor']):
        print(f"⚠️ Fila incompleta o vacía. Tiempo={fila['Tiempo']}, Valor={fila['Valor']}")
        continue
    try:
        numero = str(int(float(fila['Tiempo'])))            # Eliminar decimales de 'Tiempo'
        valor_entero = int(float(fila['Valor']))            # Convertir a entero
        valor = str(valor_entero).ljust(4, '0')             # Rellenar con ceros a la derecha si hace falta
    except ValueError:
        print(f"⚠️ Error de conversión en fila: {fila}")
        continue

    ruta = f'Geiger/ocr_input_{numero}s.png'
    digitos = [int(d) for d in valor]
    datos.append((ruta, digitos))

# -------------------------------
# Guardar cada dígito en su carpeta correspondiente
# -------------------------------
output_dir = Path('Geiger/dataset/train')
output_dir.mkdir(parents=True, exist_ok=True)

for ruta, etiquetas in datos:
    digitos = segmentar_digitos(ruta)

    if len(digitos) != len(etiquetas):
        print(f"⚠️ Atención: En {ruta}, se detectaron {len(digitos)} dígitos pero hay {len(etiquetas)} etiquetas.")
        continue

    for i, (digit, label) in enumerate(zip(digitos, etiquetas)):
        clase_dir = output_dir / str(label)
        clase_dir.mkdir(parents=True, exist_ok=True)
        filename = clase_dir / f'{Path(ruta).stem}_d{i}_{np.random.randint(10000)}.png'
        cv2.imwrite(str(filename), digit)

    print(f"✅ {ruta} procesado y guardado.")
# -------------------------------
# 1. Cargar el dataset desde las carpetas
# -------------------------------
batch_size = 32
img_size = (28, 28)

train_ds = tf.keras.utils.image_dataset_from_directory(
    "Geiger/dataset/train",
    labels="inferred",
    label_mode="int",
    image_size=img_size,
    color_mode="grayscale",
    shuffle=True,
    seed=123,
    batch_size=batch_size
)

# Normalizar imágenes: escala de 0-255 a 0-1
normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))

# -------------------------------
# 2. Definir el modelo CNN
# -------------------------------
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')  # 10 clases (0 a 9)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# -------------------------------
# 3. Entrenar el modelo
# -------------------------------
model.fit(train_ds, epochs=10)

# -------------------------------
# 4. Guardar el modelo entrenado
# -------------------------------
model.save("modelo_digitos.keras")
print("✅ Modelo guardado como modelo_digitos.keras")# Diviendo ejecución en bloques de 1000 ficheros, que se cuelga con facilidad

# -------------------------------
# Cargar el modelo entrenado
# -------------------------------
modelo = load_model("modelo_digitos.keras")

# -------------------------------
# Función para segmentar los dígitos
# -------------------------------
def segmentar_digitos(ruta_imagen):
    img = cv2.imread(str(ruta_imagen), cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    limpio = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    procesado = cv2.bitwise_not(cv2.dilate(cv2.bitwise_not(limpio), kernel, iterations=1))
    contornos, _ = cv2.findContours(procesado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[0])
    digitos = []
    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        if h > 15 and w > 5:
            roi = procesado[y:y+h, x:x+w]
            digit = cv2.resize(roi, (28, 28)).astype("float32") / 255.0
            digitos.append(digit.reshape(28, 28, 1))
    return np.array(digitos)

# -------------------------------
# Procesar archivos en bloques
# -------------------------------
carpeta = Path("Geiger")
archivos = list(carpeta.glob("ocr_input_*s.png"))
total_archivos = len(archivos)
bloque_tamano = 1000

bloques = [archivos[i:i+bloque_tamano] for i in range(0, total_archivos, bloque_tamano)]

df_final = pd.DataFrame()

for idx, bloque in enumerate(bloques, start=1):
    print(f"\n🧩 Procesando bloque {idx}/{len(bloques)} con {len(bloque)} archivos...")
    resultados = []

    for i, imagen_path in enumerate(bloque, start=1):
        print(f"  [{i}/{len(bloque)}] {imagen_path.name}")

        match = re.search(r"ocr_input_(\d+)s\.png", imagen_path.name)
        if not match:
            continue
        tiempo = int(match.group(1))

        digitos_segmentados = segmentar_digitos(imagen_path)
        if len(digitos_segmentados) < 4:
            print(f"⚠️ Solo se detectaron {len(digitos_segmentados)} dígitos en {imagen_path.name}")
            continue

        predicciones = modelo.predict(digitos_segmentados, verbose=0)
        valores = [str(np.argmax(p)) for p in predicciones]
        valor_final = "".join(valores)

        resultados.append({
            "Tiempo": tiempo,
            "Valor": int(valor_final),
            "Archivo": imagen_path.name
        })

    df_bloque = pd.DataFrame(resultados)
    df_final = pd.concat([df_final, df_bloque], ignore_index=True)

print("\n✅ Todos los bloques procesados.")
print(df_final.head())

# Guardar resultado completo
df_final.to_csv("Resultados_geiger_completo.csv", index=False)
print("📁 Archivo guardado: Resultados_geiger_completo.csv")