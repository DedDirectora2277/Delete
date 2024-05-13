import cv2
import numpy as np


def remove_text(image_path, mask_path):
    # Загрузка изображения и маски
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, 0)  # Загружаем как одноканальное изображение

    # Применяем инвертированную маску к изображению
    #inverted_mask = cv2.bitwise_not(mask)
    result = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    return result
