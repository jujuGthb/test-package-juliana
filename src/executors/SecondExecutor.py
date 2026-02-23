"""
Filter Processor (Blur or Sharpen)
"""

import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayScaleFlipHorizontal.src.utils.response import build_response_second
from components.GrayScaleFlipHorizontal.src.models.PackageModel import PackageModel


class SecondExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.mode = self.request.get_param("filter")
        self.image1 = self.request.get_param("inputImage")  
        self.image2 = self.request.get_param("inputImage2") 

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def blur(self, img, kernel):
        size = int(kernel.replace("x", ""))
        return cv2.blur(img, (size, size))

    def sharpen(self, img, strength):
        kernel = np.array([
            [0, -1, 0],
            [-1, 5 + strength, -1],
            [0, -1, 0]
        ])
        return cv2.filter2D(img, -1, kernel)



    def run(self):
    
        img1 = Image.get_frame(img=self.image1, redis_db=self.redis_db)
        
        
        if self.image2:
            img2 = Image.get_frame(img=self.image2, redis_db=self.redis_db)
        else:
            img2 = img1 

       
        if self.mode:
            option_name = self.mode.get("name")
            params = self.mode.get("value", {})

            if option_name == "Blur":
                kernel = params.get("kernel", {}).get("value", "3x3")
               
                
                print(f"[SecondExecutor] Blur kernel={kernel}")
                
                
                img1.value = self.blur(img1.value, kernel)
                img2.value = self.blur(img2.value, kernel)

            elif option_name == "Sharpen":
                strength = params.get("strength", {}).get("value", 1.0)
                
                print(f"[SecondExecutor] Sharpen strength={strength}")
                
                img1.value = self.sharpen(img1.value, strength)
                img2.value = self.sharpen(img2.value, strength)

      
        self.outputImage1 = Image.set_frame(img=img1, package_uID=f"{self.uID}_out1", redis_db=self.redis_db)
        
   
        self.outputImage2 = Image.set_frame(img=img2, package_uID=f"{self.uID}_out2", redis_db=self.redis_db)

        
        packageModel = build_response_second(context=self)
        return packageModel

    if "__main__" == __name__:
        Executor(sys.argv[1]).run()
