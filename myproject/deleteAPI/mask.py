import cv2
import numpy as np
import pytesseract
from PIL import Image


def process_image(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Находим координаты прямоугольников, содержащих текст
    boxes = pytesseract.image_to_boxes(image)

    mask = np.zeros_like(image)

    # Рисуем прямоугольники на изображении, увеличивая их размер на пару пикселей
    for b in boxes.splitlines():
        b = b.split()
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        # Увеличиваем размеры прямоугольника на пару пикселей
        x -= 2
        y -= 2
        w += 4
        h += 4
        cv2.rectangle(mask, (x, mask.shape[0] - y), (w, mask.shape[0] - h), (255, 255, 255), -1)

    return mask
