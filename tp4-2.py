import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter
from typing import Tuple, List
import cv2

class HoughLineDetector:

    def __init__(self, theta_res: float = 1.0, rho_res: float = 1.0):
        self.theta_res = theta_res
        self.rho_res = rho_res
        self.thetas = np.deg2rad(np.arange(-90.0, 90.0, self.theta_res))
        self.accumulator = np.array([])
        self.rhos = np.array([])
        self.peaks = []

    def detect_and_find_peaks(self, binary_img: np.ndarray, threshold: int, min_distance: int = 10) -> List[Tuple[float, float, int]]:
        height, width = binary_img.shape
        diag_len = int(np.ceil(np.sqrt(width**2 + height**2)))
        self.rhos = np.arange(-diag_len, diag_len + 1, self.rho_res)
        self.accumulator = np.zeros((len(self.rhos), len(self.thetas)), dtype=np.uint64)

        y_idxs, x_idxs = np.nonzero(binary_img)
        
        cos_thetas = np.cos(self.thetas)
        sin_thetas = np.sin(self.thetas)
        
        rhos_matrix = np.round(x_idxs[:, np.newaxis] * cos_thetas + y_idxs[:, np.newaxis] * sin_thetas).astype(int)
        rhos_matrix += diag_len
        
        for theta_idx in range(len(self.thetas)):
            np.add.at(self.accumulator[:, theta_idx], rhos_matrix[:, theta_idx], 1)

        footprint = np.ones((2 * min_distance + 1, 2 * min_distance + 1))
        local_maxima = maximum_filter(self.accumulator, footprint=footprint)
        
        is_peak = (self.accumulator == local_maxima) & (self.accumulator > threshold)
        rho_indices, theta_indices = np.nonzero(is_peak)
        
        votes = self.accumulator[rho_indices, theta_indices]
        self.peaks = sorted(zip(self.rhos[rho_indices], self.thetas[theta_indices], votes), key=lambda x: x[2], reverse=True)
        
        return self.peaks

    def plot_results(self, img: np.ndarray, edges: np.ndarray):
        fig, axes = plt.subplots(1, 3, figsize=(21, 7))
        ax_img, ax_edges, ax_acc = axes

        ax_img.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax_img.set_title(f"Resultado Final - {len(self.peaks)} líneas detectadas")
        ax_img.set_axis_off()

        for rho, theta, _ in self.peaks:
            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho
            x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * (a))
            x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * (a))
            ax_img.plot((x1, x2), (y1, y2), color='lime', linewidth=2)
        
        ax_edges.imshow(edges, cmap='gray')
        ax_edges.set_title("Bordes (Canny)")
        ax_edges.set_axis_off()

        extent = [np.rad2deg(self.thetas[0]), np.rad2deg(self.thetas[-1]), self.rhos[-1], self.rhos[0]]
        im = ax_acc.imshow(self.accumulator, cmap='hot', aspect='auto', extent=extent)
        ax_acc.set_title("Acumulador de Hough (Líneas)")
        ax_acc.set_xlabel("θ (grados)"), ax_acc.set_ylabel("ρ (píxeles)")
        fig.colorbar(im, ax=ax_acc)

        for rho, theta, _ in self.peaks:
            ax_acc.plot(np.rad2deg(theta), rho, 'cx', markersize=10, markeredgewidth=2)

        plt.tight_layout()
        plt.show()

def process_lines(image_path='block_motor.jpg'):
    try:
        original_img = cv2.imread(image_path)
        if original_img is None: raise FileNotFoundError
        
        gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        edges_img = cv2.Canny(gray_img, 50, 150)

        detector = HoughLineDetector(theta_res=1.0, rho_res=1.0)
        
        print("--- Detección de Líneas ---")
        print("Aplicando Transformada de Hough y buscando picos...")
        peaks = detector.detect_and_find_peaks(edges_img, threshold=100, min_distance=15)
        
        print(f"\nSe detectaron {len(peaks)} líneas.")
        detector.plot_results(original_img, edges_img)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{image_path}'.")

if __name__ == "__main__":
    IMAGE_FILE = 'block_motor.jpg'
    process_lines(IMAGE_FILE)