import numpy as np
from differential import Difference
from detector import Detector
from peak_detector import PeakDetector


class ChangePointDetector(Detector):
    def __init__(self, x: np.ndarray, y: np.ndarray):
        super(ChangePointDetector, self).__init__()
        self.x = x
        self.y = y
        self.__param = {
            "Threshold": {
                "Unit": None,
                "Value": 0.15
            },
            "Δx": {
                "Unit": "mm",
                "Value": 0.05
            },
            "Peak Sensitivity": {
                "Unit": None,
                "Value": 0.5
            }
        }
        self.diff2 = []

    def detect(self) -> list:
        dx = self.__param["Δx"]["Value"]
        peak_sens = self.__param["Peak Sensitivity"]["Value"]

        diff = Difference(self.x, self.y)
        diff_x, diff_y = diff.central_differential(dx)
        diff2 = Difference(diff_x, diff_y)
        diff2_x, diff2_y = diff2.central_differential(dx)
        self.diff2 = [diff2_x, diff2_y]

        peak_detector = PeakDetector(diff2_x, diff2_y*(-1.0))
        peak_detector.set_sensitivity(peak_sens)

        return peak_detector.detect()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from decoder import S1TDecoder
    from differential import Difference

    data = S1TDecoder(r"/Users/nobunobu/Downloads/GenC_ReAx_67.5mm_PV/Vibration resistance_No.03_3-31.S1T")
    print(data.name)
    # diff = Difference(data.x(), data.y())
    # diff_cent = diff.central_differential(0.05)
    # diff_forw = diff.forward_differential(0.05)
    # diff2 = Difference(diff_cent[0], diff_cent[1])
    # diff2_cent = diff2.central_differential(0.05)
    # plt.plot(data.x(), data.y())
    # plt.plot(diff_cent[0], diff_cent[1])
    # # plt.plot(diff_forw[0], diff_forw[1])
    # plt.plot(diff2_cent[0], diff2_cent[1]/10)

    detector = ChangePointDetector(data.x(), data.y())
    detect_point = detector.detect()

    fig, ax1 = plt.subplots()
    ax1.plot(data.x(), data.y())
    ax2 = ax1.twinx()
    ax2.plot(detector.diff2[0], detector.diff2[1], "y")
    ax2.plot(detector.diff2[0][detect_point], detector.diff2[1][detect_point], "ro")

    plt.show()