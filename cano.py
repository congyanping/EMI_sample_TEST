import h5py
import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
data = h5py.File('/home/congyanping/Desktop/EMI_sample_test/result.hdf5','r')
data = data['result'][...][1:,:]

data = data.reshape(-1)

data[np.where(np.abs(data)==0)] = np.nan
print 'haha',data[np.where(np.abs(data)==0)]
print min(np.abs(data))
data = data.reshape(-1,2048)

###

nullfmt = NullFormatter()         # no labels

# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h = left_h = left + width + 0.02

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom_h, width, 0.2]
rect_histy = [left_h, bottom, 0.2, height]

# start with a rectangular Figure
plt.figure(1, figsize=(8, 8))
axScatter = plt.axes(rect_scatter)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

# no labels
axHistx.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)

#data = np.angle(data,deg = True) + 360
data = np.abs(data)

print 'min(data)',min(data.reshape(-1))
extent = [0,4e7,6288,0]
axScatter.imshow(np.log10(data[:,1024:]),aspect = 'auto',extent = extent)
axHistx.plot(range(data[:,1024:].shape[1]), np.log10(np.std(data[:,1024:],axis=0)))
axHistx.set_xlim((0,data[:,1024:].shape[1]))
axHistx.set_ylabel("Standard deviation(log=True)")

axHisty.plot(data[:,1024:][:,100], range(data[:,1024:][:,1].shape[0]))
axHisty.set_ylim((0,data[:,1024:][:,1].shape[0]))
axHisty.set_ylabel("Amplitude")

plt.show()
#plt.close()


