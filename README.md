# Persistent homology for smartphone data analysis (pedestrian recognition)

**Description.** 

The goal of this is project to illustrate, on a toy example, the benefit of coordinate invariance
of persistent homology. The walk of 3 pedestrians A, B and C, has been recorded using the
accelerometer sensor of a smartphone carried in the their pocket, giving rise to 3 multivariate time series
in R3: each time series represents the 3 coordinates of the acceleration of the corresponding pedestrian in
a coordinate system attached to the sensor. As, the smartphone was carried in unknown different positions
and was not fixed, these time series cannot be compared coordinates by coordinates. Using a sliding window,
each series has been splitted in a list of 100 times series made of 200 consecutive points, that are stored in
data A, data B and data C. To each set of 200 points is associated a label A, B or C stored in label. The objective is to compute the persistence diagrams of these 3D point clouds and use them to achieve a pedestrian recognition task (supervised setting).

## Command lines

### Compute and save persistence diagrams (Q2)
The ```persistence_diagram.py``` script computes and saves (in a .npy file) the n-dimensional persistence diagram of all the point clouds in the input data file. Files are automatically named persistence_landscapes_(given_dim)dim.npy.

```
usage: persistence_diagram.py [-h] --dim {0,1} --raw-data RAW_DATA
                              [--save SAVE]

optional arguments:
  -h, --help           show this help message and exit
  --dim {0,1}          dimension of the persistence diagrams
  --raw-data RAW_DATA  path containing the data file
  --save SAVE          path of the directory where to save the persistence
                       diagrams as a numpy array
```
### Compute and save pairwise bottleneck distances (Q3)
The ```pairwise_btnck_dist.py``` script computes and saves the pairwise bottleneck distances matrix using the previously computed diagrams. 

NB: this function is computationally intensive (around 7h for 300 persistence diagram). The output files are available in the pairwise_bottleneck_distances folder.

```
usage: pairwise_btnck_dist.py [-h] --dgms DGMS --dim {0,1} --save SAVE

optional arguments:
  -h, --help   show this help message and exit
  --dgms DGMS  path containing the directory of the file with the persistence
               diagrams
  --dim {0,1}  dimension of the persistence diagrams
  --save SAVE  path containing the directory where to save a csv file
```

### Compute and save persistence landscapes features (Q4, Q5)
The ```persistence_landscape.py``` script computes and saves the landscape features using the previously computed diagrams.

```
usage: persistence_landscape.py [-h] --dgms DGMS [--dim {0,1}] [--save SAVE]
                                [--xmin XMIN] [--xmax XMAX]
                                [--n-nodes N_NODES] [--n-ld N_LD]

optional arguments:
  -h, --help         show this help message and exit
  --dgms DGMS        path containing the directory of the file with the
                     persistence diagrams
  --dim {0,1}        dimension of the persistence diagrams
  --save SAVE        path of the directory where to save the persistence
                     landscape observation matrix as a numpy array
  --xmin XMIN        left endpoint of the interval
  --xmax XMAX        right endpoint of the interval
  --n-nodes N_NODES  number of nodes of a regular grid on the interval [xmin,
                     xmax]
  --n-ld N_LD        number of landscapes
```

### Train a Random Forest Classifier (Q5)
The ```train_model.py```script trains a Random Forest classifier using previously computed features, prints an average accuracy on 5 k-fold cross-validation, and saves the model trained on the whole data.

```
usage: train_model.py [-h] --raw-data RAW_DATA --dim {0,1,2} --features
                      FEATURES --save SAVE

optional arguments:
  -h, --help           show this help message and exit
  --raw-data RAW_DATA  path containing the data file
  --dim {0,1,2}        dimension to consider consider for the features
  --features FEATURES  path of the directory which contains the features
  --save SAVE          path where to save the model
```
                     xmax]
