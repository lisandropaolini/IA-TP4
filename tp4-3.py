
import numpy as np
import matplotlib.pyplot as plt
import cv2

def process_circles(image_path='block_motor.jpg'):

    try:
        original_img = cv2.imread(image_path)
        if original_img is None: raise FileNotFoundError
        
        output_img = original_img.copy()
        gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        
        gray_img = cv2.medianBlur(gray_img, 5)

        print("\n--- Detección de Circunferencias ---")
        print("Aplicando Transformada de Hough para Círculos...")

        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40,
                                   param1=50, param2=30, minRadius=20, maxRadius=50)

        num_circles = 0
        if circles is not None:
            circles = np.uint16(np.around(circles))
            num_circles = len(circles[0, :])
            for i in circles[0, :]:
                # Dibujar la circunferencia exterior en verde
                cv2.circle(output_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # Dibujar el centro del círculo en rojo
                cv2.circle(output_img, (i[0], i[1]), 2, (0, 0, 255), 3)
        
        print(f"\nSe detectaron {num_circles} circunferencias.")

        # Visualización de resultados
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
        plt.title(f'Resultado Final - {num_circles} círculos detectados')
        plt.axis('off')
        plt.show()

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{image_path}'.")


if __name__ == "__main__":
    IMAGE_FILE = 'block_motor.jpg'

    process_circles(IMAGE_FILE)