import math

import numpy as np

from Constant import Constant


def iono(time):
    alpha = [9.3132E-09, 0.0000E+00, -5.9605E-08, 0.0000E+00]
    beta = [9.0112E+04, 0.0000E+00, -1.9661E+05, 0.0000E+00]

    fir = 52
    lamr = 21
    tow = time * 3600 + 86400

    el = 15
    az = 180

    els = el / 180

    # kat geocentryczny
    psi = 0.0137 / (els + 0.11) - 0.022

    # szerokosc_ipp
    fi_ipp = fir / 180 + psi * math.cos(np.deg2rad(az))

    if fi_ipp > 0.416:
        fi_ipp = 0.416
    elif fi_ipp < -0.416:
        fi_ipp = -0.416

    # długość geo IPP
    lam_ipp = lamr / 180 + psi * math.sin(np.deg2rad(az)) / math.cos(fi_ipp * np.pi)

    # szerokosc geomagnetyczna
    fi_m = fi_ipp + 0.064 * math.cos((lam_ipp - 1.617) * np.pi)

    # czas lokalny
    t = 43200 * lam_ipp + tow

    t = math.fmod(t, 86400)

    if t >= 86400:
        t -= 86400
    elif t < 0:
        t += 86400

    Aion = alpha[0] + alpha[1] * fi_m + alpha[2] * fi_m ** 2 + alpha[3] * fi_m ** 3
    if Aion < 0:
        Aion = 0

    Pion = beta[0] + beta[1] * fi_m + beta[2] * fi_m ** 2 + beta[3] * fi_m ** 3
    if Pion < 72000:
        Pion = 72000

    # faza opóźnienia jono
    fi_ion = 2 * np.pi * (t - 50400) / Pion

    # funkcja mapująca
    mf = 1 + 16 * (0.53 - els) ** 3

    delta_L1 = Constant.c * mf * (5 * 10 ** (-9) + Aion * (1 - (fi_ion ** 2) / 2 + (fi_ion ** 4) / 24)) \
        if abs(fi_ion <= math.pi / 2) \
        else Constant.c * mf * (5 * 10 ** (-9))
    return delta_L1


if __name__ == "__main__":
    print(iono(7))
