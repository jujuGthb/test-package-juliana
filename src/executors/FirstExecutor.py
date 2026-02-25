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
from components.GrayScaleFlipHorizontal.src.utils.response import build_response_first
from components.GrayScaleFlipHorizontal.src.models.PackageModel import PackageModel


class FirstExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.mode = self.request.get_param("Transform")
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

        
        if self.mode:
            option_name = self.mode.get("name")
            values = self.mode.get("value", {})
            
            if option_name == "Rotate":
                angle = values.get("angle", {}).get("value", 90)
                img.value = self.rotate(img.value, angle)
            elif option_name == "Resize":
                scale = values.get("scale", {}).get("value", 1.0)
                method = values.get("method", {}).get("value", "linear")
                
                img.value = self.resize(img.value, scale, method)
                
        
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
       
        
        packageModel = build_response_first(context=self)    
        return packageModel
            


    if "__main__" == __name__:
        Executor(sys.argv[1]).run()
