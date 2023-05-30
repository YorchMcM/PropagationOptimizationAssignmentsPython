import os
import numpy as np
from tudatpy.util import result2array
import LunarAscentUtilities as Util

from matplotlib import use
use('TkAgg')
import matplotlib.pyplot as plt

#################################################################

design_method = 'factorial_design'
model1 = 66
model2 = 67

#################################################################


def str2vec(string: str, separator: str) -> np.ndarray:
    return np.array([float(element) for element in string.split(separator)])


def read_vector_history_from_file(file_name: str) -> dict:

    with open(file_name, 'r') as file: lines = file.readlines()
    keys = [float(line.split('\t')[0]) for line in lines]
    solution = dict.fromkeys(keys)
    for idx in range(len(keys)): solution[keys[idx]] = str2vec(lines[idx], '\t')[1:]

    return solution


title = 'Trajectory difference between models ' + str(model1) + ' and ' + str(model2)

read_dir = os.getcwd() + '/DesignSpace_' + design_method + '/'
model1 = read_vector_history_from_file(read_dir + 'Run_' + str(model1) + '/state_history.dat')
model2 = read_vector_history_from_file(read_dir + 'Run_' + str(model2) + '/state_history.dat')
diff = result2array(Util.compare_models(model1, model2, list(model1.keys())))

plt.figure()
plt.semilogy((diff[:,0] - diff[0,0]) / 86400.0, abs(diff[:,1]) / 1000.0, label = 'x')
plt.semilogy((diff[:,0] - diff[0,0]) / 86400.0, abs(diff[:,2]) / 1000.0, label = 'y')
plt.semilogy((diff[:,0] - diff[0,0]) / 86400.0, abs(diff[:,3]) / 1000.0, label = 'z')
plt.semilogy((diff[:,0] - diff[0,0]) / 86400.0, np.linalg.norm(diff[:,1:4], 2, 1) / 1000.0, label = 'Norm')
plt.xlabel('Time since beginning of simulation [days]')
plt.title(title)
plt.legend()
plt.grid()