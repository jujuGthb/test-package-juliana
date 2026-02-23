from sdks.novavision.src.helper.package import PackageHelper
from components.GrayScaleFlipHorizontal.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    FirstExecutor,
    FirstExecutorResponse,
    FirstExecutorOutputs,
    OutputImage,
    SecondExecutor,
    SecondExecutorResponse,
    SecondExecutorOutputs,
    OutputImage1,
    OutputImage2
)


def build_response_first(context):

    outputImage = OutputImage(value=context.image)

    firstOutputs = FirstExecutorOutputs(outputImage=outputImage)

    firstResponse = FirstExecutorResponse(outputs=firstOutputs)

    firstExecutor = FirstExecutor(value=firstResponse)

    executor = ConfigExecutor(value=firstExecutor)

    packageConfigs = PackageConfigs(executor=executor)

    package = PackageHelper(packageModel=PackageModel,packageConfigs=packageConfigs)

    packageModel = package.build_model(context)

    return packageModel


def build_response_second(context):

    outputImage1 = OutputImage1(value=context.outputImage1)
    outputImage2 = OutputImage2(value=context.outputImage2)

    secondOutputs = SecondExecutorOutputs(outputImage1=outputImage1,outputImage2=outputImage2)

    secondResponse = SecondExecutorResponse(outputs=secondOutputs)

    secondExecutor = SecondExecutor(value=secondResponse)

    executor = ConfigExecutor(value=secondExecutor)

    packageConfigs = PackageConfigs(executor=executor)

    package = PackageHelper(packageModel=PackageModel,packageConfigs=packageConfigs)

    packageModel = package.build_model(context)

    return packageModel
