# Persistent homology for smartphone data analysis (pedestrian recognition)

**Description.** The goal of this is project to illustrate, on a toy example, the benefit of coordinate invariance
of persistent homology. The walk of 3 pedestrians A, B and C, has been recorded using the
accelerometer sensor of a smartphone carried in the their pocket, giving rise to 3 multivariate time series
in R3: each time series represents the 3 coordinates of the acceleration of the corresponding pedestrian in
a coordinate system attached to the sensor. As, the smartphone was carried in unknown different positions
and was not fixed, these time series cannot be compared coordinates by coordinates. Using a sliding window,
each series has been splitted in a list of 100 times series made of 200 consecutive points, that are stored in
data A, data B and data C. To each set of 200 points is associated a label A, B or C stored in label (see
the data set and the Python script to load the data). The objective is to compute the persistence diagrams
of these 3D point clouds and use them to achieve a pedestrian recognition task (supervised setting).
