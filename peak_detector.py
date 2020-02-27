import numpy as np
from detector import Detector


class PeakDetector(Detector):
    def __init__(self, x: np.ndarray, y: np.ndarray):
        super(PeakDetector, self).__init__()
        self.__x = x
        self.__y = y
        self.__param = {
            "Sensitivity": {
                "Unit": None,
                "Value": 0.05,
            }
        }

    def set_sensitivity(self, v):
        self.__param["Sensitivity"]["Value"] = v

    def __search_index(self, data: np.ndarray, y):
        for i, d in enumerate(data):
            if d == y:
                return i
        return -1

    def detect(self):
        th = self.__param["Sensitivity"]["Value"]
        _max = self.__y.max()
        max_idx = self.__search_index(self.__y, _max)

        max_temp = 0.0
        max_temp_idx = 0
        detect_points = []
        for i in range(max_idx):
            if max_temp < self.__y[i]:
                max_temp = self.__y[i]
                max_temp_idx = i
            diff = max_temp - self.__y[i]
            if diff > th:
                detect_points.append(max_temp_idx)
                max_temp = 0.0
        detect_points.append(max_idx)

        return detect_points
