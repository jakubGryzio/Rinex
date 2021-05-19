import math

import numpy as np

hort = 140.857
el = np.deg2rad(90)

p = 1013.25 * ((1 - 0.0000226 * hort) ** 5.225)
t = 291.15 - 0.0065 * hort
e = 6.11 * (0.5 * math.exp(-0.0006396 * hort)) * (10 ** ((7.5 * (t - 273.15)) / (t - 35.85)))
Nd = 77.64 * (p / t)
Nw = -12.96 * (e / t) + (3.718 * 10 ** 5) * (e / (t ** 2))
hd = 40136 + 148.72 * (t - 273.15)
hw = 11000
delta_Td0 = (10 ** (-6) / 5) * Nd * hd
delta_Tw0 = (10 ** (-6) / 5) * Nw * hw
md = 1 / math.sin((math.sqrt(el ** 2 + 6.25)))
mw = 1 / math.sin((math.sqrt(el ** 2 + 2.25)))
delta_Td = md * delta_Td0
delta_Tw = mw * delta_Tw0

delta_T = delta_Td + delta_Tw

print(delta_T)
