import numpy as np


class Difference:
    def __init__(self, x: np.ndarray, y: np.ndarray):
        self.x = x
        self.y = y
        # 等間隔とは限らないのでΔxを計算しておく
        self.delta = [self.x[i+1] - self.x[i] for i in range(len(self.x)-1)]
        print(self.x)
        pass

    def central_differential(self, delta: float) -> (np.ndarray, np.ndarray):
        x_start_idx = np.where(self.x <= self.x[0]+delta)[0].max()
        x_stop_idx = np.where(self.x <= (self.x.max()-delta))[0].max()
        delta_idx = x_start_idx
        fx = []
        fy = []
        for i in range(x_start_idx, x_stop_idx):
            dx = self.x[i+delta_idx] - self.x[i]
            a = (self.y[i+delta_idx] - self.y[i-delta_idx])/(2*dx)
            fx.append(self.x[i])
            fy.append(a)
            print(dx)
        return np.array(fx), np.array(fy)

    def forward_differential(self, delta: float) -> (np.ndarray, np.ndarray):
        """
        @param delta:
        @return: the result is calculated differential x and y.
        """
        x_start_idx = 0
        x_stop_idx = np.where(self.x <= (self.x.max()-delta))[0].max()
        delta_idx = np.where(self.x <= self.x[0]+delta)[0].max()
        fx = []
        fy = []
        for i in range(x_start_idx, x_stop_idx):
            dx = self.x[i+delta_idx] - self.x[i]
            a = (self.y[i+delta_idx] - self.y[i])/dx
            fx.append(self.x[i])
            fy.append(a)
            print(dx)
        return np.array(fx), np.array(fy)


class Detector:
    def __init__(self, x:np.ndarray, y:np.ndarray):
        self.__x = x
        self.__y = y

    def __search_index(self, data:np.ndarray, y):
        for i, d in enumerate(data):
            if d == y:
                return i
        return -1

    def detect_diff(self, th=0.5):
        detect_points = []

        return detect_points

    def detect(self, th=0.5):
        _max = self.__y.max()
        max_idx = self.__search_index(self.__y, _max)
        
        max_temp = 0.0
        max_temp_idx = 0
        detect_points = []
        for i in range(max_idx):
            if max_temp < self.__y[i]:
                max_temp = self.__y[i]
                max_temp_idx = i
            diff = max_temp-self.__y[i]
            if diff > th:
                detect_points.append(max_temp_idx)
                max_temp = 0.0
        detect_points.append(max_idx)

        return detect_points


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from decoder import S1TDecoder

    data = S1TDecoder(r"/Users/nobunobu/Downloads/GenC_ReAx_67.5mm_PV/Salt spray_No.01_1-41.S1T")
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
