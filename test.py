import numpy as np

test = np.array([0, 1, np.nan, np.nan])
test2 = np.array([0, 1, 2, 3])
print(test, test2)
ind = np.where(np.isnan(test))
test[ind] = test2[ind]
print(test, test2)