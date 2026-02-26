"""
Image Transformation: Rotate or Resize
"""


import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageTransformFilter.src.utils.response import build_response_first
from components.ImageTransformFilter.src.models.PackageModel import PackageModel


class FirstExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.mode = self.request.get_param("Transform")
        if self.mode == "Rotate":
            angle = self.request.get_param("angle")
        elif self.mode == "Resize":
            scale = self.request.get_param("scale")
            method = self.request.get_param("method")
            
        
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}


    def rotate(self, img, angle):
        h, w = img.shape[:2]
        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(img, matrix, (w, h))


    def resize(self, img, scale, method):
        interpolation_map = {
            "nearest": cv2.INTER_NEAREST,
            "linear": cv2.INTER_LINEAR,
            "cubic": cv2.INTER_CUBIC,
        }

        h, w = img.shape[:2]
        new_size = (int(w * scale), int(h * scale))

        return cv2.resize(img, new_size,
                        interpolation=interpolation_map[method])

    def run(self):
        img=Image.get_frame(img=self.image, redis_db=self.redis_db)

        
        
        
            
        if self.mode == "Rotate":
            angle = getattr(self, 'angle',90)
            img.value = self.rotate(img.value, angle)
        elif self.mode == "Resize":
            scale = getattr(self, 'scale',90)
            scale = getattr(self, 'scale',1.0)
            method = getattr(self, 'method',"linear")
                
            img.value = self.resize(img.value, scale, method)
                
        
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
       
        
        packageModel = build_response_first(context=self)    
        return packageModel
            


    if "__main__" == __name__:
        Executor(sys.argv[1]).run()
