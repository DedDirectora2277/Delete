import cv2
import numpy as np
import pytesseract


def process_image(image_path, output_path):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Находим координаты прямоугольников, содержащих текст
    boxes = pytesseract.image_to_boxes(image)

    mask = np.zeros_like(image)

    # Рисуем прямоугольники на изображении
    for b in boxes.splitlines():
        b = b.split()
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(mask, (x, mask.shape[0] - y), (w, mask.shape[0] - h), (255, 255, 255), -1)

    cv2.imwrite(output_path, mask)


def restore_background(image_path, mask_path, output_path):
    # Загрузка изображения и маски
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # Инвертирование маски
    mask_inv = cv2.bitwise_not(mask)

    # Применение инвертированной маски к изображению для восстановления фона
    background_restored_image = cv2.bitwise_and(image, image, mask=mask_inv)

    # Сохранение восстановленного изображения
    cv2.imwrite(output_path, background_restored_image)


# Пример использования
process_image('photoenglish.jpg', 'mask.png')
restore_background('photoenglish.jpg', 'mask.png', 'background_restored_image.jpg')
