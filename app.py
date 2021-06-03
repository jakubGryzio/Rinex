import numpy as np
from flask import Flask, render_template, request, flash, session
from werkzeug.utils import secure_filename

from CalcRecvCoord import CalcRecvCoord
from CalcTime import CalcTime
from ReadFile import ReadFile
from plot import change_xyz, change_xyz_value, change_dop, change_atmo, change_pt_mask

app = Flask(__name__)
app.secret_key = "secret_key"


def setTime(start, stop):
    CalcTime.start_day[0] = int(start[0][0])
    CalcTime.start_day[1] = int(start[0][1])
    CalcTime.start_day[2] = int(start[0][2])
    CalcTime.start_day[3] = int(start[1][0])
    CalcTime.start_day[4] = int(start[1][1])
    CalcTime.stop_day[0] = int(stop[0][0])
    CalcTime.stop_day[1] = int(stop[0][1])
    CalcTime.stop_day[2] = int(stop[0][2])
    CalcTime.stop_day[3] = int(stop[1][0])
    CalcTime.stop_day[4] = int(stop[1][1])


@app.route('/', methods=['POST', 'GET'])
def main():
    done = False
    coords = None
    dop = None
    correct_file = True
    if request.method == 'POST':
        session["start_day"] = request.form.get("date-start")
        session["stop_day"] = request.form.get("date-stop")
        session["mask"] = request.form.get("mask")
        day_start = "".join(session.get("start_day").split("T")[0]).split("-")
        time_start = "".join(session.get("start_day").split("T")[1]).split(":")
        day_stop = "".join(session.get("stop_day").split("T")[0]).split("-")
        time_stop = "".join(session.get("stop_day").split("T")[1]).split(":")
        start = (day_start, time_start)
        stop = (day_stop, time_stop)
        setTime(start, stop)
        coord = CalcRecvCoord()
        coord.mask = int(session.get("mask"))
        f_nav = request.files['nav']
        f_obs = request.files['obs']
        f_nav.save(secure_filename(f_nav.filename))
        f_obs.save(secure_filename(f_obs.filename))
        if f_nav.filename[f_nav.filename.find(".") - 1] != "N" or f_obs.filename[f_obs.filename.find(".") - 1] != "O":
            correct_file = False
        if correct_file:
            ReadFile.set_nav_to_dest(f_nav.filename)
            ReadFile.set_obs_coord_to_dest(f_obs.filename)
            coords, dop = coord.getRecvCoord()
            done = True
            if done:
                flash("Coords have been computed!")
            filename = "static/coords.txt"
            np.savetxt(filename, coords[:, 0:-1], fmt="%.3f", delimiter=" ", newline="\n", header="X Y Z")
            np.savetxt("static/dop.txt", dop, fmt="%.5f", delimiter=" ", newline="\n")
        else:
            flash("Input correct file!")
        if request.form.get("plot") == "change-xyz":
            change_xyz(coords)
        elif request.form.get("plot") == "change-xyz-value":
            change_xyz_value(coords)
        elif request.form.get("plot") == "change-dop":
            change_dop(dop)
        elif request.form.get("plot") == "change-atmo":
            coords_none, dop = coord.getRecvCoord(False, False)
            coords_iono, dop = coord.getRecvCoord(True, False)
            coords_tropo, dop = coord.getRecvCoord(False, True)
            change_atmo(coords_none, coords_iono, coords_tropo)
        elif request.form.get("plot") == "change-pt-mask":
            coords_15, dop = coord.getRecvCoord(True, True, 15)
            coords_20, dop = coord.getRecvCoord(True, True, 20)
            change_pt_mask(coords, coords_15, coords_20)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
