
'''
Bram Thijssen
s4308905
Eduardo Hoefel
s1043186
'''

import scipy.io as sio
import numpy as np
from matplotlib import pyplot as plt

def correlate(sBoxLayer, traces):
	print("correlating")
	corr = []

	for y in traces:
		corr2 = []
		for x in sBoxLayer:
			corr2.append(np.corrcoef(y, x)[0][1])
	
		corr.append(corr2)
	
	corr = np.transpose(corr)

	return corr

def load_rawfiles():
	print("loading raw files")
	file_in = sio.loadmat('input.mat')
	file_traces = sio.loadmat('leakage_y0_y1.mat')
	inp = file_in['input']
	
	traces = file_traces['L']
	traces = np.transpose(traces)
	
	inp = [x[0] for x in inp]

	return (inp, traces)

def merge_k(var_in):
	print("unmerging k to create sBoxLayer")

	var_in = [[x ^ np.uint8(k) for x in var_in] for k in range(16)]

	return var_in

def hammingdistance(old_registers, new_register):
	print("doing hammingdistance")

	h = [["{0:b}".format(x[i] ^ new_register[i]).count('1') for i in range(len(new_register))] for x in old_registers]

	return h

def plot(corr):
	print("plotting")
	plt.plot(corr)
	plt.show()

def save(corr):
	print("saving data")
	mat = np.matrix(corr)
	np.savetxt('/results/raw/correlation.txt', mat, fmt='%.18f')

def load():
	print("loading data")
	f = open('correlation.txt','r') 
	return np.loadtxt(f)

def absolute(corr):
	print("calculating absolute values")
	for x in range(len(corr)):
		for y in range(len(corr[x])):
			corr[x][y] = abs(corr[x][y])

	return corr

def sboxlayer(v):
	print("calculating s function")
	return [[s(x) for x in y] for y in v]

def merge_samples(t):
	print("merging samples")
	t2 = []
	for i in range(len(t)):
		for j in range(i+1,len(t)):
			t2.append([t[i][x] * t[j][x] for x in range(2000)])
	
	return t2

def s(v):
	if v == 0:
		return 12
	if v == 1:
		return 5
	if v == 2:
		return 6
	if v == 3:
		return 11
	if v == 4:
		return 9
	if v == 5:
		return 0
	if v == 6:
		return 10
	if v == 7:
		return 13
	if v == 8:
		return 3
	if v == 9:
		return 14
	if v == 10:
		return 15
	if v == 11:
		return 8
	if v == 12:
		return 4
	if v == 13:
		return 7
	if v == 14:
		return 1
	if v == 15:
		return 2

	print("Error: ", v)
	return None


if __name__ == '__main__':

	d, t = load_rawfiles()
	v = merge_k(d)
	v = sboxlayer(v)
	t = merge_samples(t)

	m = correlate(v, t)
	m = absolute(m)
	m = np.transpose(m)

	best_correlations = [0 for x in range(16)]

	for x in m:
		for i in range(16):
			if x[i] > best_correlations[i]:
				best_correlations[i] = x[i]
	
	for i in range(16):
		print("{}\t: {}".format(i, best_correlations[i]))

