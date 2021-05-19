import numpy as np

from Constant import Constant


class GPS:
    delta_tr = 0
    recv_coord = [0, 0, 0]

    def __init__(self):
        self.x = self.recv_coord[0]
        self.y = self.recv_coord[1]
        self.z = self.recv_coord[2]

    def get_x(self):
        return self.x

    def add_x(self, x):
        self.x += x

    def get_y(self):
        return self.y

    def add_y(self, y):
        self.y += y

    def get_z(self):
        return self.z

    def add_z(self, z):
        self.z += z

    def getArrayCoord(self):
        return np.array([self.get_x(), self.get_y(), self.get_z()])

    def getArrayParameter(self):
        return np.array([self.get_x(), self.get_y(), self.get_z(), self.delta_tr])

    def setCoordGPS(self, matX):
        self.add_x(matX[0, 0])
        self.add_y(matX[1, 0])
        self.add_z(matX[2, 0])
        self.delta_tr += matX[3, 0] / Constant.c
