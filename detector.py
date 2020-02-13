import numpy as np


class Detector:
    def __init__(self, x:np.ndarray, y:np.ndarray):
        self.__x = x
        self.__y = y

    def __search_index(self, data:np.ndarray, y):
        for i, d in enumerate(data):
            if d == y:
                return i
        return -1

    def detect(self, th=0.5):
        _max = self.__y.max()
        max_idx = self.__search_index(self.__y, _max)
        
        max_temp = 0.0
        max_temp_idx = 0
        detect_point = []
        for i in range(max_idx):
            if max_temp < self.__y[i]:
                max_temp = self.__y[i]
                max_temp_idx = i
            diff = max_temp-self.__y[i]
            if diff > th:
                detect_point.append(max_temp_idx)
                max_temp = 0.0
        detect_point.append(max_idx)

        return detect_point
