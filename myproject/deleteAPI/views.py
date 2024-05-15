import io

import cv2
from django.core.signals import request_finished
from django.db import transaction
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .mask import process_image
from .models import ProcessedImage
from .serializers import ProcessedImageSerializer
import requests
from PIL import Image
from .restore_background import remove_text


class ProcessImageView(APIView):
    # @transaction.atomic
    def post(self, request, format=None):
        serializer = ProcessedImageSerializer(data=request.data)
        if serializer.is_valid():
            # Save the incoming image
            processed_image = serializer.save()

            processed_image.save()

            # Create the mask
            mask_np_array = process_image(processed_image.image.path)
            mask_pil_image = Image.fromarray(mask_np_array)

            mask_bytes_io = io.BytesIO()
            mask_pil_image.save(mask_bytes_io, format='JPEG')
            mask_bytes_io.seek(0)

            # Assign the in-memory mask bytes to the mask field
            processed_image.mask.save('mask.jpg', mask_bytes_io)

            processed_image.save()

            # Send the image and mask to another application
            # files = {'image_file': (processed_image.image.name, open(processed_image.image.path, 'rb'), 'image/jpeg'),
            #          'Mask_file': (processed_image.mask.name, open(processed_image.image.path, 'rb'), 'image/jpeg')}
            # response = requests.post('https://hama-api/inpaint', files=files)

            # Assuming the other application returns the processed image
            # Save the processed image received from the other application
            # if response.status_code == 200:
            #     processed_image.processed_image = response.content
            #     processed_image.save()
            # else:
            #     processed_image.delete()
            #     return Response("Failed to process image", status=response.status_code)

            processed_np = remove_text(processed_image.image.path, processed_image.mask.path)
            processed_image_rgb = cv2.cvtColor(processed_np, cv2.COLOR_BGR2RGB)
            processed_pil_image = Image.fromarray(processed_image_rgb)

            processed_io = io.BytesIO()
            processed_pil_image.save(processed_io, format='JPEG')
            processed_io.seek(0)

            # Assign the in-memory mask bytes to the mask field
            processed_image.processed_image.save('processed_image.jpg', processed_io)

            # Создаем объект MultiPartParser и используем его для создания ответа
            # parser = MultiPartParser()
            # content, content_type = parser.parse({'file': processed_image.processed_image})
            processed_image_data = processed_image.processed_image.read()

            response = HttpResponse(processed_image_data, content_type='image/jpeg')

            mask_bytes_io.close()
            processed_io.close()
            mask_pil_image.close()
            processed_pil_image.close()

            # processed_image.delete()
            # transaction.on_commit(lambda: self.delete_processed_image())

            if processed_image.image:
                processed_image.image.delete()
            if processed_image.mask:
                processed_image.mask.delete()
            if processed_image.processed_image:
                processed_image.processed_image.delete()

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @transaction.on_commit
#     @staticmethod
#     def delete_processed_image(sender, instance, **kwargs):
#         if instance.processed_image:
#             instance.processed_image.delete()
#
#
# post_delete.connect(ProcessImageView.delete_processed_image, sender=ProcessedImage)
