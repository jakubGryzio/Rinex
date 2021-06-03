from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt

from CalcTime import CalcTime
from GPS import GPS
from hirvonen import hirvonen


def func_hirvonen(x):
    fi, lam, h = hirvonen(x[0], x[1], x[2])
    return np.rad2deg(fi), np.rad2deg(lam), h


def change_xyz(coords):
    fi_recv, lam_recv, h_recv = hirvonen(GPS.approx_coords[0], GPS.approx_coords[1], GPS.approx_coords[2])
    map_coords = np.apply_along_axis(func_hirvonen, 1, coords)
    sub = map_coords - np.array([np.rad2deg(fi_recv), np.rad2deg(lam_recv), h_recv])
    start_day = datetime(CalcTime.start_day[0], CalcTime.start_day[1], CalcTime.start_day[2], CalcTime.start_day[3],
                         CalcTime.start_day[4], CalcTime.start_day[5])
    stop_day = datetime(CalcTime.stop_day[0], CalcTime.stop_day[1], CalcTime.stop_day[2], CalcTime.stop_day[3],
                        CalcTime.stop_day[4], CalcTime.stop_day[5])
    rms_x = np.power(np.sum(np.power(sub[:, 0], 2)) / len(sub[:, 0]), 0.5)
    std_x = np.std(sub[:, 0])
    rms_y = np.power(np.sum(np.power(sub[:, 1], 2)) / len(sub[:, 1]), 0.5)
    std_y = np.std(sub[:, 1])
    rms_z = np.power(np.sum(np.power(sub[:, 2], 2)) / len(sub[:, 2]), 0.5)
    std_z = np.std(sub[:, 2])
    x = [start_day + timedelta(seconds=s) for s in range(0, int((stop_day - start_day).total_seconds()), CalcTime.interval)]
    fig, ax = plt.subplots(3, figsize=(10, 7))
    fig.suptitle("NEU Coordinates change per time")
    ax[0].set_title("Coordinate B")
    ax[0].plot(x, sub[:, 0])
    ax[0].set_ylim(np.min(sub[:, 0]) - np.max(sub[:, 0]) / 5, np.max(sub[:, 0]) + np.max(sub[:, 0]) / 5)
    ax[0].text(0.8, 0.01, f'RMS: {round(rms_x, 7)}', horizontalalignment='left', transform=ax[0].transAxes, color='black', fontsize=13)
    ax[0].axhline(y=np.mean(sub[:, 0]) + std_x, xmin=0, xmax=len(x), ls='--', c='r', label="std", lw=1)
    ax[0].axhline(y=np.mean(sub[:, 0]), xmin=0, xmax=len(x), ls='-', c='g', label="mean", lw=1.5)
    ax[0].axhline(y=np.mean(sub[:, 0]) - std_x, xmin=0, xmax=len(x), ls='--', c='r', lw=1)
    ax[0].set_xlabel('GPS Time [month-day hour]')
    ax[0].set_ylabel('Difference [o]')

    ax[1].set_title("Coordinate L")
    ax[1].plot(x, sub[:, 1])
    ax[1].set_ylim(np.min(sub[:, 1]) - np.max(sub[:, 0]) / 5, np.max(sub[:, 1]) + np.max(sub[:, 0]) / 5)
    ax[1].text(0.8, 0.01, f'RMS: {round(rms_y, 7)}', horizontalalignment='left', transform=ax[1].transAxes,
               color='black', fontsize=13)
    ax[1].axhline(y=np.mean(sub[:, 1]) - std_y, xmin=0, xmax=len(x), ls='--', c='r', label="std", lw=1)
    ax[1].axhline(y=np.mean(sub[:, 1]), xmin=0, xmax=len(x), ls='-', c='g', label="mean", lw=1.5)
    ax[1].axhline(y=np.mean(sub[:, 1]) + std_y, xmin=0, xmax=len(x), ls='--', c='r', lw=1)
    ax[1].set_xlabel('GPS Time [month-day hour]')
    ax[1].set_ylabel('Difference [o]')

    ax[2].set_title("Coordinate H")
    ax[2].plot(x, sub[:, 2])
    ax[2].set_ylim(np.min(sub[:, 2]) - 10, np.max(sub[:, 2]) + 10)
    ax[2].text(0.8, 0.01, f'RMS: {round(rms_z, 3)}', horizontalalignment='left', transform=ax[2].transAxes,
               color='black', fontsize=13)
    ax[2].axhline(y=np.mean(sub[:, 2]) + std_z, xmin=0, xmax=len(x), ls='--', c='r', label="std", lw=1)
    ax[2].axhline(y=np.mean(sub[:, 2]), xmin=0, xmax=len(x), ls='-', c='g', label="mean", lw=1.5)
    ax[2].axhline(y=np.mean(sub[:, 2]) - std_z, xmin=0, xmax=len(x), ls='--', c='r', lw=1)
    ax[2].set_xlabel('GPS Time [month-day hour]')
    ax[2].set_ylabel('Difference [m]')
    ax[0].legend(bbox_to_anchor=(0.9, 1))
    fig.tight_layout()
    fig.savefig('static/plot.pdf')
    plt.show()


def change_xyz_value(coords):
    fi_recv, lam_recv, h_recv = hirvonen(GPS.approx_coords[0], GPS.approx_coords[1], GPS.approx_coords[2])
    map_coords = np.apply_along_axis(func_hirvonen, 1, coords)
    sub = map_coords - np.array([np.rad2deg(fi_recv), np.rad2deg(lam_recv), h_recv])
    std_x = np.std(sub[:, 0])
    std_y = np.std(sub[:, 1])
    std_z = np.std(sub[:, 2])
    fig, ax = plt.subplots(3, figsize=(10, 6), tight_layout=True)
    fig.suptitle("Coordinates differences histogram")
    ax[0].set_title("Coordinate B")
    ax[0].hist(sub[:, 0], bins=30)
    ax[0].axvline(x=np.mean(sub[:, 0]) - std_x, ls='--', c='r', label="std", lw=1)
    ax[0].axvline(x=np.mean(sub[:, 0]), ls='-', c='g', label="mean", lw=2)
    ax[0].axvline(x=np.mean(sub[:, 0]) + std_x, ls='--', c='r', lw=1)
    ax[0].set_xlabel("Difference [o]")
    ax[1].set_title("Coordinate L")
    ax[1].hist(sub[:, 1], bins=30)
    ax[1].axvline(x=np.mean(sub[:, 1]) - std_y, ls='--', c='r', label="std", lw=1)
    ax[1].axvline(x=np.mean(sub[:, 1]), ls='-', c='g', label="RMS", lw=2)
    ax[1].axvline(x=np.mean(sub[:, 1]) + std_y, ls='--', c='r', lw=1)
    ax[1].set_xlabel("Difference [o]")
    ax[2].set_title("Coordinate H")
    ax[2].hist(sub[:, 2], bins=30)
    ax[2].axvline(x=np.mean(sub[:, 2]) - std_z, ls='--', c='r', label="std", lw=1)
    ax[2].axvline(x=np.mean(sub[:, 2]), ls='-', c='g', label="mean", lw=2)
    ax[2].axvline(x=np.mean(sub[:, 2]) + std_z, ls='--', c='r', lw=1)
    ax[2].set_xlabel("Difference [m]")
    ax[0].legend(bbox_to_anchor=(1, 1.6))
    fig.savefig('static/plot.pdf')


def change_dop(dop):
    start_day = datetime(CalcTime.start_day[0], CalcTime.start_day[1], CalcTime.start_day[2], CalcTime.start_day[3],
                         CalcTime.start_day[4], CalcTime.start_day[5])
    stop_day = datetime(CalcTime.stop_day[0], CalcTime.stop_day[1], CalcTime.stop_day[2], CalcTime.stop_day[3],
                        CalcTime.stop_day[4], CalcTime.stop_day[5])
    x = [start_day + timedelta(seconds=s) for s in range(0, int((stop_day - start_day).total_seconds()), CalcTime.interval)]
    fig, ax = plt.subplots(figsize=(14, 6), tight_layout=True)
    ax.set_title("DOP Parameters")
    ax.plot(x, dop[:, 0], label="Geometrical")
    ax.plot(x, dop[:, 1], label="Position")
    ax.plot(x, dop[:, 2], label="Time")
    ax.plot(x, dop[:, 3], label="Horizontal")
    ax.plot(x, dop[:, 4], label="Vertical")
    ax.set_xlabel("GPS Time [month-day hour]")
    ax.set_ylabel("DOP's value")
    ax.legend(loc="upper right")
    fig.savefig('static/plot.pdf')


def change_atmo(none, iono, tropo):
    fi_recv, lam_recv, h_recv = hirvonen(GPS.approx_coords[0], GPS.approx_coords[1], GPS.approx_coords[2])
    map_coords_none = np.apply_along_axis(func_hirvonen, 1, none)
    map_coords_iono = np.apply_along_axis(func_hirvonen, 1, iono)
    map_coords_tropo = np.apply_along_axis(func_hirvonen, 1, tropo)
    sub_none = map_coords_none - np.array([np.rad2deg(fi_recv), np.rad2deg(lam_recv), h_recv])
    sub_iono = map_coords_iono - np.array([np.rad2deg(fi_recv), np.rad2deg(lam_recv), h_recv])
    sub_tropo = map_coords_tropo - np.array([np.rad2deg(fi_recv), np.rad2deg(lam_recv), h_recv])
    start_day = datetime(CalcTime.start_day[0], CalcTime.start_day[1], CalcTime.start_day[2], CalcTime.start_day[3],
                         CalcTime.start_day[4], CalcTime.start_day[5])
    stop_day = datetime(CalcTime.stop_day[0], CalcTime.stop_day[1], CalcTime.stop_day[2], CalcTime.stop_day[3],
                        CalcTime.stop_day[4], CalcTime.stop_day[5])
    rms_x_none = np.power(np.sum(np.power(sub_none[:, 0], 2)) / len(sub_none[:, 0]), 0.5)
    rms_x_tropo = np.power(np.sum(np.power(sub_tropo[:, 0], 2)) / len(sub_tropo[:, 0]), 0.5)
    rms_x_iono = np.power(np.sum(np.power(sub_iono[:, 0], 2)) / len(sub_iono[:, 0]), 0.5)
    rms_y_none = np.power(np.sum(np.power(sub_none[:, 1], 2)) / len(sub_none[:, 1]), 0.5)
    rms_y_tropo = np.power(np.sum(np.power(sub_tropo[:, 1], 2)) / len(sub_tropo[:, 1]), 0.5)
    rms_y_iono = np.power(np.sum(np.power(sub_iono[:, 1], 2)) / len(sub_iono[:, 1]), 0.5)
    rms_z_none = np.power(np.sum(np.power(sub_none[:, 2], 2)) / len(sub_none[:, 2]), 0.5)
    rms_z_tropo = np.power(np.sum(np.power(sub_tropo[:, 2], 2)) / len(sub_tropo[:, 2]), 0.5)
    rms_z_iono = np.power(np.sum(np.power(sub_tropo[:, 2], 2)) / len(sub_iono[:, 2]), 0.5)
    x = [start_day + timedelta(seconds=s) for s in
         range(0, int((stop_day - start_day).total_seconds()), CalcTime.interval)]
    fig, ax = plt.subplots(3, figsize=(10, 7))
    fig.suptitle("NEU Coordinates change for different atmospheric corrections")
    ax[0].set_title("Coordinate B")
    ax[0].plot(x, sub_iono[:, 0], ls="--", c='g', label="ionospheric")
    ax[0].plot(x, sub_tropo[:, 0], ls="-.", c='y', label="tropospheric")
    ax[0].plot(x, sub_none[:, 0], ls=":", c='r', label="none")
    ax[0].text(0.4, 0.01, f'RMS None: {round(rms_x_none, 7)}', horizontalalignment='left', transform=ax[0].transAxes,
                color='black', fontsize=11)
    ax[0].text(0.6, 0.01, f'RMS IONO: {round(rms_x_iono, 7)}', horizontalalignment='left', transform=ax[0].transAxes,
               color='black', fontsize=11)
    ax[0].text(0.8, 0.01, f'RMS TROPO: {round(rms_x_tropo, 7)}', horizontalalignment='left', transform=ax[0].transAxes,
               color='black', fontsize=11)
    ax[0].set_xlabel('GPS Time [month-day hour]')
    ax[0].set_ylabel('Difference [o]')

    ax[1].set_title("Coordinate L")
    ax[1].plot(x, sub_iono[:, 1], ls="--", c='g')
    ax[1].plot(x, sub_tropo[:, 1], ls="-.", c='y')
    ax[1].plot(x, sub_none[:, 1], ls=":", c='r')
    ax[1].text(0.4, 0.01, f'RMS None: {round(rms_y_none, 7)}', horizontalalignment='left', transform=ax[1].transAxes,
               color='black', fontsize=11)
    ax[1].text(0.6, 0.01, f'RMS IONO: {round(rms_y_iono, 7)}', horizontalalignment='left', transform=ax[1].transAxes,
               color='black', fontsize=11)
    ax[1].text(0.8, 0.01, f'RMS TROPO: {round(rms_y_tropo, 7)}', horizontalalignment='left', transform=ax[1].transAxes,
               color='black', fontsize=11)
    ax[1].set_xlabel('GPS Time [month-day hour]')
    ax[1].set_ylabel('Difference [o]')

    ax[2].set_title("Coordinate H")
    ax[2].plot(x, sub_iono[:, 2], ls="--", c='g')
    ax[2].plot(x, sub_tropo[:, 2], ls="-.", c='y')
    ax[2].plot(x, sub_none[:, 2], ls=":", c='r')
    ax[2].text(0.4, 0.01, f'RMS None: {round(rms_z_none, 3)}', horizontalalignment='left', transform=ax[2].transAxes,
               color='black', fontsize=11)
    ax[2].text(0.6, 0.01, f'RMS IONO: {round(rms_z_iono, 3)}', horizontalalignment='left', transform=ax[2].transAxes,
               color='black', fontsize=11)
    ax[2].text(0.8, 0.01, f'RMS TROPO: {round(rms_z_tropo, 3)}', horizontalalignment='left', transform=ax[2].transAxes,
               color='black', fontsize=11)
    ax[2].set_xlabel('GPS Time [month-day hour]')
    ax[2].set_ylabel('Difference [m]')
    ax[0].legend(bbox_to_anchor=(0.9, 1))
    fig.tight_layout()
    fig.savefig('static/plot.pdf')


def change_pt_mask(coords, coords_15, coords_20):
    sub = coords - np.array([3835751.6257, 1177249.7445, 4941605.0540])
    sub_15 = coords_15 - np.array([3835751.6257, 1177249.7445, 4941605.0540])
    sub_20 = coords_20 - np.array([3835751.6257, 1177249.7445, 4941605.0540])
    start_day = datetime(CalcTime.start_day[0], CalcTime.start_day[1], CalcTime.start_day[2], CalcTime.start_day[3],
                         CalcTime.start_day[4], CalcTime.start_day[5])
    stop_day = datetime(CalcTime.stop_day[0], CalcTime.stop_day[1], CalcTime.stop_day[2], CalcTime.stop_day[3],
                        CalcTime.stop_day[4], CalcTime.stop_day[5])
    pt = np.power(np.power(sub[:, 0], 2) + np.power(sub[:, 1], 2) + np.power(sub[:, 2], 2), 0.5)
    pt_15 = np.power(np.power(sub_15[:, 0], 2) + np.power(sub_15[:, 1], 2) + np.power(sub_15[:, 2], 2), 0.5)
    pt_20 = np.power(np.power(sub_20[:, 0], 2) + np.power(sub_20[:, 1], 2) + np.power(sub_20[:, 2], 2), 0.5)
    x = [start_day + timedelta(seconds=s) for s in
         range(0, int((stop_day - start_day).total_seconds()), CalcTime.interval)]
    fig, ax = plt.subplots(3, figsize=(10, 7))
    fig.suptitle("XYZ Coordinates error change for different masks")
    ax[0].set_title("Mask 10")
    ax[0].plot(x, pt, c='magenta')
    ax[0].set_xlabel('GPS Time [month-day hour]')
    ax[0].set_ylabel('Difference [m]')

    ax[1].set_title("Mask 15")
    ax[1].plot(x, pt_15, c='magenta')
    ax[1].set_xlabel('GPS Time [month-day hour]')
    ax[1].set_ylabel('Difference [m]')

    ax[2].set_title("Mask 20")
    ax[2].plot(x, pt_20, c='magenta')
    ax[2].set_xlabel('GPS Time [month-day hour]')
    ax[2].set_ylabel('Difference [m]')
    fig.tight_layout()
    fig.savefig('static/plot.pdf')