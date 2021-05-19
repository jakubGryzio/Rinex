import time

from CalcRecvCoord import CalcRecvCoord
from ReadFile import ReadFile

if __name__ == "__main__":
    start = time.time()
    ReadFile.set_nav_to_dest('D:\Pliki_Kuby\Studia\II_ROK\SNS\Projekt2\WROC00POL_R_20210600000_01D_GN.rnx')
    ReadFile.set_obs_coord_to_dest('D:\Pliki_Kuby\Studia\II_ROK\SNS\Projekt2\WROC00POL_R_20210600000_01D_30S_MO.rnx')
    coord = CalcRecvCoord()
    test = coord.iobs
    coords, elev, azimuth = coord.getRecvCoord()
    stop = time.time()
    print(stop - start)

