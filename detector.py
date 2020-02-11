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
        max_range = self.__search_index(self.__y, _max)
        
        max_temp = 0.0
        detect_point = 0
        for i in range(max_range):
            if max_temp < self.__y[i]:
                max_temp = self.__y[i]
            diff = max_temp-self.__y[i]
            detect_point = i
            if diff > th:
                detect_point = self.__search_index(self.__y, max_temp)
                break
            
        return detect_point
