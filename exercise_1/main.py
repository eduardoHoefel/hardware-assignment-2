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
	file_in = sio.loadmat('in.mat')
	file_traces = sio.loadmat('traces.mat')
	inp = file_in['in']
	
	traces = file_traces['traces']
	traces = np.transpose(traces)
	
	var_in = [x[0] for x in inp]
	#var_in = inp

	return (var_in, traces)

def merge_k(var_in):
	print("merging k to create sBoxLayer")
	sBoxLayer = [[x ^ np.uint8(k) for x in var_in] for k in range(16)]

	return sBoxLayer

def hammingweight(sBoxLayer):
	print("doing hammingweight")
	h = [["{0:b}".format(x).count('1') for x in y] for y in sBoxLayer]

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

def plot_rankings(results):
	labels = [500, 1000, 2000, 4000, 8000, 12000, 14990]

	plt.plot(results)
	plt.gca().invert_yaxis()
	plt.yticks(list(range(1, 17)))
	plt.xticks(list(range(len(labels))), labels)
	plt.xticks(rotation=70)
	plt.show()
	exit()

if __name__ == '__main__':

	d, t = load_rawfiles()
	v = merge_k(d)
	v = sboxlayer(v)
	h = hammingweight(v)

	results = []
	attacks = [500, 1000, 2000, 4000, 8000, 12000, -1]

	for i in attacks:
		print("Calculating colleration for {} elements".format(i))
		if i == -1:
			t2 = t
			h2 = h
		else:
			t2 = [x[0:i] for x in t]
			h2 = [x[0:i] for x in h]

		m = correlate(h2, t2)
		m = absolute(m)

		max_values = np.array([max(k) for k in m])
		print("Max values:")
		for k in range(len(max_values)):
			print("{}: {}".format(k, max_values[k]))

		max_value_6 = max_values[6]
		max_values_sorted = np.sort(max_values)[::-1]
		print("Sorted max values:")
		for k in range(len(max_values_sorted)):
			print("{}: {}".format(k, max_values_sorted[k]))

		key_6_pos, = np.where(max_values_sorted == max_values[6])[0]
		print("Position of key 6: ")
		print(key_6_pos)

		results.append([np.where(max_values_sorted == max_values[x])[0][0]+1 for x in range(16)])
	
	plot_rankings(results)

	exit()
