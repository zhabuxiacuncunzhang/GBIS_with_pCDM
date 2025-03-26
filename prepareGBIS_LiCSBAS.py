from scipy import io
import numpy as np
from osgeo import gdal

heading = -168.04655
inc = 33.8573
tif_file = "./20220105_20221207.cum.geo.tif"
save_name = "20220105_20221207.mat"

dataset = gdal.Open(tif_file)
if not dataset:
    print(f"Unable to open {tif_file}")
    # return False

geotransform = dataset.GetGeoTransform()
xfirst = geotransform[0]
xstep = geotransform[1]
yfirst = geotransform[3]
ystep = geotransform[5]

band = dataset.GetRasterBand(1)
data = band.ReadAsArray()

width = dataset.RasterXSize
height = dataset.RasterYSize
data = data.reshape([width * height, 1])

lon = np.zeros(shape=(width * height, 1))
lat = np.zeros(shape=(width * height, 1))
inc_v = np.zeros(shape=(width * height, 1))
heading_v = np.zeros(shape=(width * height, 1))


for i in range(height*width):
    lon[i] = xfirst+(i % width)*xstep
    lat[i] = yfirst+int(i/width)*ystep
    inc_v[i] = inc
    heading_v[i] = heading

save_data = np.c_[data, lon, lat, inc_v, heading_v]
# print(save_data.shape)

save_data = save_data[np.all(save_data != 0, axis=1)]
row_with_nan = np.isnan(save_data).any(axis=1)
save_data = np.delete(save_data, np.where(row_with_nan), axis=0)
# print(save_data)

new_num=np.size(save_data,0)

io.savemat(save_name, {'Phase': np.reshape(save_data[:, 0], [new_num, 1]), 'Lon': np.reshape(save_data[:, 1], [new_num, 1]), 'Lat': np.reshape(
    save_data[:, 2], [new_num, 1]), 'Incidence': np.reshape(save_data[:, 3], [new_num, 1]), 'Heading': np.reshape(save_data[:, 4], [new_num, 1])})
