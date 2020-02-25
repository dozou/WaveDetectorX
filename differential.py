import numpy as np


class Difference:
    def __init__(self, x: np.ndarray, y: np.ndarray):
        self.x = x
        self.y = y
        # 等間隔とは限らないのでΔxを計算しておく
        self.delta = [self.x[i + 1] - self.x[i] for i in range(len(self.x) - 1)]
        print(self.x)
        pass

    def central_differential(self, delta: float) -> (np.ndarray, np.ndarray):
        """

        @param delta:
        @return: the result is calculated differential x and y.
        """
        x_start_idx = np.where(self.x <= self.x[0] + delta)[0].max()
        x_stop_idx = np.where(self.x <= (self.x.max() - delta))[0].max()
        delta_idx = x_start_idx
        fx = []
        fy = []
        for i in range(x_start_idx, x_stop_idx):
            dx = self.x[i + delta_idx] - self.x[i]
            a = (self.y[i + delta_idx] - self.y[i - delta_idx]) / (2 * dx)
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
        x_stop_idx = np.where(self.x <= (self.x.max() - delta))[0].max()
        delta_idx = np.where(self.x <= self.x[0] + delta)[0].max()
        fx = []
        fy = []
        for i in range(x_start_idx, x_stop_idx):
            dx = self.x[i + delta_idx] - self.x[i]
            a = (self.y[i + delta_idx] - self.y[i]) / dx
            fx.append(self.x[i])
            fy.append(a)
            print(dx)
        return np.array(fx), np.array(fy)