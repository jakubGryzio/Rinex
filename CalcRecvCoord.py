import numpy as np
import math

from CalcTime import CalcTime, calcTimeOfRinex
from Constant import Constant
from Satellite import Satellite
from GPS import GPS
from hirvonen import hirvonen


class CalcRecvCoord:
    RECV = GPS()
    obs, iobs = None, None
    mask = 0

    def getRecvCoord(self):
        recvCoord_per_time = np.zeros([0, 4])
        for next_time in range(calcTimeOfRinex(CalcTime.start_day), calcTimeOfRinex(CalcTime.stop_day) + 1,
                               CalcTime.interval):
            recv = np.zeros([0, 4])
            dist = np.zeros([0, 1])
            Satellite.set_def_prop_signal()
            Satellite.set_calc_time(next_time)
            epoch = self.getEpochSatellite(next_time)
            observation = self.obs[
                (np.isin(self.iobs[:, 0], self.getEpochSatellite(next_time)[:, -1])) & (self.iobs[:, 2] == next_time)]
            for iteration in range(4):
                XYZ, correctedXYZ, geometricalDist, pseudoDist, y, matA, elevation, azimuth = np.zeros([0, 4]), np.zeros([0, 4]), \
                                                                          np.zeros([0, 1]), np.zeros([0, 1]), \
                                                                          np.zeros([0, 1]), np.zeros([0, 4]), np.zeros([0, 1]), np.zeros([0, 1])
                for i, satellite in enumerate(epoch):
                    if iteration > 0:
                        Satellite.prop_signal = dist[i, 0] / Constant.c
                    XYZ = np.vstack([XYZ, getEpochSatelliteCoord(satellite)])
                    correctedXYZ = np.vstack([correctedXYZ, getCorrectedCoordEpochSatellite(XYZ[i])])
                    geometricalDist = np.vstack([geometricalDist, self.getGeometricalDistance(correctedXYZ[i])])
                    pseudoDist = np.vstack([pseudoDist, self.getPseudoDistance(correctedXYZ[i], geometricalDist[i])])
                    y = np.vstack([y, get_matY(pseudoDist[i], observation[i])])
                    matA = np.vstack([matA, self.get_matA(correctedXYZ[i], geometricalDist[i])])
                    elevation = np.vstack([elevation, self.getElevation(correctedXYZ[i])])
                    azimuth = np.vstack([azimuth, self.getAzimuth(correctedXYZ[i])])
                matX = get_matX(matA, y)
                self.RECV.setCoordGPS(matX)
                recv = np.vstack([recv, self.RECV.getArrayParameter()])
                dist = geometricalDist
            recvCoord_per_time = np.vstack([recvCoord_per_time, recv[-1]])
        return recvCoord_per_time, elevation, azimuth

    def getEpochSatellite(self, start_time):
        epoch = np.zeros([0, 38])
        for nrSat in self.getTimeInterval(start_time)[:, 0]:
            sat = Satellite(nrSat)
            if self.mask != 0:
                if self.getElevation(sat.getCoordSatellite()) > self.mask:
                    epoch = np.vstack([epoch, sat.getEpochSatelliteParameter()])
            else:
                epoch = np.vstack([epoch, sat.getEpochSatelliteParameter()])
        return epoch

    def getTimeInterval(self, start_time):
        return self.iobs[self.iobs[:, 2] == start_time]

    def getGeometricalDistance(self, satellite):
        ro = math.sqrt(
            (satellite[0] - self.RECV.get_x()) ** 2 + (satellite[1] - self.RECV.get_y()) ** 2 + (
                    satellite[2] - self.RECV.get_z()) ** 2)
        return ro

    def getPseudoDistance(self, satellite, dist):
        pseudoDist = dist - Constant.c * satellite[3] + Constant.c * self.RECV.delta_tr
        return pseudoDist

    def get_matA(self, satellite, dist):
        matA = [(-(satellite[0] - self.RECV.get_x()) / dist)[0], (-(satellite[1] - self.RECV.get_y()) / dist)[0],
                (-(satellite[2] - self.RECV.get_z()) / dist)[0], 1]
        return matA

    def getElevation(self, satellite):
        NEU = self.getVectorNEU(satellite)
        return np.rad2deg(math.asin(NEU[2] / (math.sqrt(NEU[0] ** 2 + NEU[1] ** 2 + NEU[2] ** 2))))

    def getAzimuth(self, satellite):
        NEU = self.getVectorNEU(satellite)
        return np.rad2deg(math.atan2(NEU[1], NEU[0])) if np.rad2deg(
            math.atan2(NEU[1], NEU[0])) > 0 else np.rad2deg(
            math.atan2(NEU[1], NEU[0])) + 360

    def getVectorSatelliteGPS(self, satellite):
        geocentric_XYZ = self.RECV.getArrayCoord()
        coordSatellite = np.array([satellite[0], satellite[1], satellite[2]])
        return np.transpose(np.array(coordSatellite - geocentric_XYZ))

    def getVectorNEU(self, satellite):
        return np.dot(np.transpose(self.getNEU()), self.getVectorSatelliteGPS(satellite))

    def getNEU(self):
        fi, lamb, h = hirvonen(self.RECV.get_x(), self.RECV.get_y(), self.RECV.get_z())
        return np.array([[-math.sin(fi) * math.cos(lamb), -math.sin(lamb), math.cos(fi) * math.cos(lamb)],
                         [-math.sin(fi) * math.sin(lamb), math.cos(lamb), math.cos(fi) * math.sin(lamb)],
                         [math.cos(fi), 0, math.sin(fi)]])


def getEpochSatelliteCoord(satellite):
    nr_satellite = satellite[len(satellite) - 1]
    return Satellite(nr_satellite).getCoordSatellite()


def getCorrectedCoordEpochSatellite(satellite_coord):
    wE = Constant.wE
    rot = np.dot([[math.cos(wE * Satellite.prop_signal), math.sin(wE * Satellite.prop_signal), 0],
                  [-math.sin(wE * Satellite.prop_signal), math.cos(wE * Satellite.prop_signal), 0],
                  [0, 0, 1]], [[satellite_coord[0]], [satellite_coord[1]], [satellite_coord[2]]])
    rot = np.transpose(np.append(rot, [satellite_coord[3]]))
    return rot


def get_matY(pseudo_dist, observation):
    return pseudo_dist - observation


def get_matX(A, y):
    return np.dot(np.dot(-np.linalg.inv(np.dot(np.transpose(A), A)), np.transpose(A)), y)

