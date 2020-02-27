import numpy as np
import copy
from differential import Difference
from abc import ABCMeta, abstractmethod, abstractproperty


class Detector(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        self.__param = {
            "param name": {
                "Value": 0.0,
                "Unit": None
            }
        }
        pass

    @property
    def param(self) -> dict:
        return copy.copy(self.__param)

    @param.setter
    def param(self, parameter: dict):
        self.__param = parameter
        pass

    @abstractmethod
    def detect(self) -> list:
        return []


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from decoder import S1TDecoder
    from differential import Difference

    data = S1TDecoder(r"/Users/nobunobu/Downloads/GenC_ReAx_67.5mm_PV/Vibration resistance_No.01_1-27.S1T")
    print(data.name)
    diff = Difference(data.x(), data.y())
    diff_cent = diff.central_differential(0.05)
    diff_forw = diff.forward_differential(0.05)
    diff2 = Difference(diff_cent[0], diff_cent[1])
    diff2_cent = diff2.central_differential(0.05)
    plt.plot(data.x(), data.y())
    plt.plot(diff_cent[0], diff_cent[1])
    # plt.plot(diff_forw[0], diff_forw[1])
    plt.plot(diff2_cent[0], diff2_cent[1]/10)

    # array = np.arange(0, 2*np.pi, 0.001)
    # sin_wave = np.sin(array)
    # test = Difference(array, sin_wave)
    # result_cent = test.central_differential(0.01)
    # result_forward = test.forward_differential(0.01)
    # plt.plot(array, sin_wave)
    # plt.plot(result_cent[0], result_cent[1])
    # plt.plot(result_forward[0], result_forward[1])
    plt.show()
