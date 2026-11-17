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
