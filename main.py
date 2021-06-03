import time

import numpy as np

from CalcRecvCoord import CalcRecvCoord
from GPS import GPS
from ReadFile import ReadFile

if __name__ == "__main__":
    coord = CalcRecvCoord()
    ReadFile.set_nav_to_dest('D:\Pliki_Kuby\Studia\II_ROK\SNS\Projekt2\WROC00POL_R_20210600000_01D_GN.rnx')
    ReadFile.set_obs_coord_to_dest('D:\Pliki_Kuby\Studia\II_ROK\SNS\Projekt2\WROC00POL_R_20210600000_01D_30S_MO.rnx')
    coords, dop = coord.getRecvCoord()
    start = time.time()
    test = coords[:, 0:-1] - np.array([GPS.approx_coords])
    stop = time.time()
    print(stop - start)

