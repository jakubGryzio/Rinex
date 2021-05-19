from datetime import date


class CalcTime:
    start_day = [2021, 3, 1, 0, 0, 0]
    stop_day = [2021, 3, 1, 1, 00, 00]
    interval = 60

    def set_start_day(self, start):
        self.start_day = start

    def set_stop_day(self, stop):
        self.stop_day = stop

    def set_interval(self, interval):
        self.interval = interval


def calcTimeOfRinex(epoch):
    year, month, day, hour, minute, second = setVariableFromRNX(epoch)
    daysFromStartGPStoDate = date.toordinal(date(year, month, day)) - date.toordinal(date(1980, 1, 6))
    numberOfDayInWeek = daysFromStartGPStoDate % 7
    towParameter = numberOfDayInWeek * 86400 + hour * 3600 + minute * 60 + second
    return towParameter


def setVariableFromRNX(SatelliteRow):
    return int(SatelliteRow[0]), int(SatelliteRow[1]), \
           int(SatelliteRow[2]), int(SatelliteRow[3]), \
           int(SatelliteRow[4]), int(SatelliteRow[5])
