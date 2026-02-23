from pydantic import validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Outputs, Configs, Response, Request, Output, Input, Config
)

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"


    class Config:
        title = "Image"

class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[Image, List[Image]]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Secondary Image"

class FirstExecutorInputs(Inputs):
    inputImage: InputImage

class SecondExecutorInputs(Inputs):
    inputImage: InputImage
    inputImage2: InputImage2

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Transformed Image"

class OutputImage1(Output):
    name: Literal["outputImage1"] = "outputImage1"
    value: Union[Image, List[Image]]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Filtered Image"

class OutputImage2(Output):
    name: Literal["outputImage2"] = "outputImage2"
    value: Union[Image, List[Image]]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Intermediate Output"

class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage

class SecondExecutorOutputs(Outputs):
    outputImage1: OutputImage1
    outputImage2: OutputImage2

class RotateAngle(Config):
    name: Literal["angle"] = "angle"
    value: Literal[0, 90, 180, 270] = 90
    type: Literal["number"] = "number"
    field: Literal["selectBox"] = "selectBox"

    class Config:
        title = "Rotation Angle"

class KeepSize(Config):
    name: Literal["keepSize"] = "keepSize"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"


    class Config:
        title = "Keep Original Size"

class RotateConfigs(Configs):
    angle: RotateAngle
    keepSize: KeepSize


class RotateOption(Config):
    name: Literal["Rotate"] = "Rotate"
    value: RotateConfigs
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Rotate Image"
        json_schema_extra = {"target": "value"}



class ResizeScale(Config):
    name: Literal["scale"] = "scale"
    value: float = 1.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Scale Factor"

class ResizeInterpolation(Config):
    name: Literal["method"] = "method"
    value: Literal["nearest", "linear", "cubic"] = "linear"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"

    class Config:
        title = "Interpolation Method"

class ResizeConfigs(Configs):
    scale: ResizeScale
    method: ResizeInterpolation

class ResizeOption(Config):
    name: Literal["Resize"] = "Resize"
    value: ResizeConfigs
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Resize Image"
        json_schema_extra = {"target": "value"}

class TransformOperation(Config):
    name: Literal["Transform"] = "Transform"
    value: Union[RotateOption, ResizeOption]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Transformation Type"
        json_schema_extra = {"target": "value"}

class BlurKernel(Config):
    name: Literal["kernel"] = "kernel"
    value: Literal["3x3", "5x5", "7x7"] = "3x3"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"

    class Config:
        title = "Kernel Size"

class BlurNormalize(Config):
    name: Literal["normalize"] = "normalize"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Normalize Result"

class BlurOption(Config):
    name: Literal["Blur"] = "Blur"
    value: Union[BlurKernel, BlurNormalize]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blur Filter"
        json_schema_extra = {"target": "value"}

class SharpenStrength(Config):
    name: Literal["strength"] = "strength"
    value: float = 1.0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Sharpen Strength"

class SharpenClamp(Config):
    name: Literal["clamp"] = "clamp"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Clamp Pixel Values"

class SharpenOption(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Union[SharpenStrength, SharpenClamp]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Sharpen Filter"
        json_schema_extra = {"target": "value"}

class FilterOperation(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[BlurOption, SharpenOption]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Filter Type"
        json_schema_extra = {"target": "value"}

class FirstExecutorConfigs(Configs):
    transform: TransformOperation

class SecondExecutorConfigs(Configs):
    filter: FilterOperation

class FirstExecutorRequest(Request):
    inputs: FirstExecutorInputs
    configs: FirstExecutorConfigs

    class Config:
        json_schema_extra = {"target": "configs"}

class FirstExecutorResponse(Response):
    outputs: FirstExecutorOutputs

class SecondExecutorRequest(Request):
    inputs: SecondExecutorInputs
    configs: SecondExecutorConfigs

    class Config:
        json_schema_extra = {"target": "configs"}

class SecondExecutorResponse(Response):
    outputs: SecondExecutorOutputs

class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: Union[FirstExecutorRequest, FirstExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "FirstExecutor"
        json_schema_extra = {"target": {"value": 0}}

class SecondExecutor(Config):
    name: Literal["SecondExecutor"] = "SecondExecutor"
    value: Union[SecondExecutorRequest, SecondExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "SecondExecutor"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor, SecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    name: Literal["ImageTransformFilter"] = "ImageTransformFilter"
    configs: PackageConfigs
    type: Literal["component"] = "component"
