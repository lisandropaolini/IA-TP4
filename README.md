# IA-TP4

# Detección de Formas con Transformada de Hough

Este proyecto contiene dos prototipos de Python que utilizan la Transformada de Hough para detectar formas geométricas (líneas y círculos) en una imagen de un bloque de motor.

## Archivos del Proyecto

1.  `tp4-2.py`: Implementa la detección de **líneas rectas**. Utiliza una implementación manual optimizada con NumPy y SciPy.
2.  `tp4-3.py`: Implementa la detección de **circunferencias**. Utiliza la función optimizada `cv2.HoughCircles` de OpenCV.
3.  `block_motor.jpg`: La imagen de entrada utilizada para ambos análisis.

## Requisitos

Para ejecutar los scripts, necesitas tener instaladas las siguientes librerías de Python:

-   `numpy`
-   `matplotlib`
-   `opencv-python`
-   `scipy`

Puedes instalarlas todas con el siguiente comando:
```bash
pip install numpy matplotlib opencv-python scipy
```

## Uso

1.  Asegúrate de que la imagen `block_motor.jpg` se encuentre en la misma carpeta que los scripts.
2.  Ejecuta cada script de forma independiente desde tu terminal para ver los resultados.

**Para detectar líneas:**
```bash
python tp4-2.py
```

**Para detectar círculos:**
```bash
python tp4-3.py
```

Cada script mostrará una ventana con los resultados visuales del análisis.

## Criterios de análisis

### Preprocesamiento y detección de bordes

El preprocesamiento reduce información que no es necesaria para buscar geometría y prepara la imagen para que los votos de Hough sean más consistentes:

- **Líneas (`tp4-2.py`)**: la imagen BGR se convierte a escala de grises y se aplica Canny con umbrales 50 y 150. Canny entrega un mapa binario de bordes; la implementación de Hough vota usando los píxeles no nulos de ese mapa. Por eso, para esta implementación sí es necesario detectar los bordes antes de llamar a `detect_and_find_peaks`.
- **Círculos (`tp4-3.py`)**: se convierte a escala de grises y se aplica un filtro de mediana de tamaño 5 para reducir ruido impulsivo conservando contornos. No se genera un mapa de bordes por separado: `cv2.HoughCircles` con `HOUGH_GRADIENT` usa internamente gradientes y Canny (controlado en parte por `param1`). Aplicar Canny y pasar ese resultado a `HoughCircles` no es el flujo esperado por esta función.

Conviene partir de una imagen enfocada, con iluminación relativamente uniforme y el motor ocupando una porción significativa del cuadro. Si hay fondo u otras piezas que producen detecciones, se puede recortar una región de interés antes del análisis. El suavizado adicional, la ecualización de contraste o un cambio en los umbrales pueden ayudar en imágenes difíciles, pero no son pasos obligatorios: deben evaluarse mirando el mapa de bordes y las detecciones, porque demasiado suavizado o umbrales inadecuados pueden borrar contornos útiles o introducir falsos positivos.

### Qué geometrías buscar en el motor

Para las **rectas**, son más informativos los bordes largos y aproximadamente rectos: caras del bloque, límites de tapas o bridas, juntas visibles, filas de pernos y aristas mecanizadas. Los segmentos cortos de textura, texto, sombras y detalles internos suelen ser menos útiles. La Transformada de Hough de este prototipo detecta rectas geométricas, no segmentos: una recta dibujada puede prolongarse más allá del borde real del componente.

Para las **circunferencias**, interesan contornos circulares visibles, por ejemplo orificios de fijación, puertos, alojamientos o extremos de ejes. Deben tener borde suficientemente continuo y un radio dentro del intervalo configurado (20–50 píxeles). Los círculos parcialmente ocultos, muy pequeños, muy grandes o vistos en perspectiva pueden no detectarse; una circunferencia vista oblicuamente suele proyectarse como una elipse. Las detecciones también pueden corresponder a elementos circulares del fondo, no necesariamente al motor.

Los parámetros actuales son valores iniciales para la imagen de ejemplo, no valores universales. En líneas, `threshold=100` establece el mínimo de votos y `min_distance=15` separa máximos cercanos en el acumulador. En círculos, `param2` influye en la sensibilidad, `minDist` limita la cercanía entre centros y `minRadius`/`maxRadius` restringen tamaños. Si faltan formas, se pueden relajar los umbrales o ampliar el rango de radios; si aparecen muchas detecciones falsas, se pueden endurecer y limitar el análisis a una región de interés.

### Cómo interpretar los resultados y la posición

En la vista de líneas, cada marca sobre el acumulador corresponde a un máximo local; el valor de voto indica cuántos píxeles de borde apoyan esa recta. Una detección fuerte y alineada con una arista real es más confiable que una línea aislada sobre textura. Los parámetros geométricos son `rho` (distancia perpendicular de la recta al origen de la imagen) y `theta` (ángulo de esa normal). El conteo mostrado es el número de máximos encontrados, por lo que puede incluir duplicados de una misma arista o líneas de objetos ajenos al motor.

En la vista de círculos, el centro rojo es `(x, y)` en píxeles y el contorno verde indica el radio `r`, también en píxeles. El origen `(0, 0)` está en la esquina superior izquierda; `x` crece hacia la derecha y `y` hacia abajo. Comparando centros y aristas con el centro y los límites del cuadro se puede describir la ubicación **relativa** del motor y reconocer su orientación en la imagen. Si se usan varios puntos o líneas, sus distancias y ángulos permiten caracterizar mejor esa disposición.

Estas salidas no determinan por sí solas la posición física 3D del motor ni una distancia real: la perspectiva, la escala y la orientación de la cámara afectan las coordenadas en píxeles. Para estimar medidas físicas o pose 3D hacen falta calibración de cámara y referencias de escala, y normalmente un modelo geométrico adicional. Por tanto, las detecciones de Hough son evidencia geométrica 2D útil para localizar y describir rasgos, no una estimación completa de pose.
