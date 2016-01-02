# K2fov [![PyPI](http://img.shields.io/pypi/v/K2fov.svg)](https://pypi.python.org/pypi/K2fov/)  [![PyPI](http://img.shields.io/pypi/dm/K2fov.svg)](https://pypi.python.org/pypi/K2fov/) [![Travis status](https://travis-ci.org/KeplerGO/K2fov.svg)](https://travis-ci.org/KeplerGO/K2fov)
***Check whether targets are in the field of view of NASA's K2 mission.***

The `K2fov` Python package allows users to check whether a target is in the field of view of K2. 
In particular, the package adds the `K2onSilicon` and `K2findCampaigns` tools
to the command line, which allow the visibility of targets to be checked
during one (`K2onSilicon`) or all (`K2findCampaigns`) campaigns, respectively.
The usage of these tools is explained below.

## Installation

You will need a modern version of Python 2 or 3 on your system.
If this requirement is met, you can install `K2fov` using `pip`:
```bash
pip install K2fov
```
if you have a previous version installed, please make sure you upgrade to the
latest version using:
```bash
pip install K2fov --upgrade
```
It is important to upgrade frequently to ensure that you are using the most
up to date K2 field parameters.

## Usage

### K2onSilicon

Installing `K2fov` will automatically add a command line tool 
to your path called `K2onSilicon`, which takes a list of targets
as input and writes a new list that indicates the "silicon status"
of each target, i.e. whether or not it falls on one of the
detectors of the spacecraft's focal plane.

**Example**

The simplest thing to do is to have a CSV file with columns
"RA_degrees, Dec_degrees, Kepmag".
Do not use a header.

For example, create a file called `mytargetlist.csv` containing
the following rows:
```bash
178.19284, 1.01924, 13.2
171.14213, 5.314616, 11.3
```

You can then check whether each object in the file falls on silicon
by calling `K2onSilicon` from the command line:
```bash
K2onSilicon mytargetlist.csv 1
```
Where `mytargetlist.csv` is your CSV file and `1` is the K2 Campaign number.

Running the code will output a file with the three input columns and an additional column containing either a "0" or "2".<br>
0 = Not observable<br>
2 = Target is in the K2 field of view and on silicon<br>

The code will also write an image, called `targets_fov.png`, showing where the targets fall.

Execute `K2onSilicon --help` to be reminded of its usage:
```
$ K2onSilicon --help
usage: K2onSilicon [-h] csv_file campaign

Run K2onSilicon to find which targets in a list call on active silicon for a
given K2 campaign.

positional arguments:
  csv_file    Name of input csv file with targets, column are Ra_degrees,
              Dec_degrees, Kepmag
  campaign    K2 Campaign number

optional arguments:
  -h, --help  show this help message and exit
```


### K2findCampaigns

If instead of checking the targets in a single campaign,
you want to understand whether a target is visible in *any* past or
future K2 Campaign, you can use a different tool called `K2findCampaigns`.

**Example**

For example, to verify whether J2000 coordinate
(ra, dec) = (269.5, -28.5) degrees is visible at any point
during the K2 mission, type:
```
$ K2findCampaigns 269.5 -28.5
Success! The target is on silicon during K2 campaigns [9].
```

You can also check a list of targets using an alternative
tool called `K2findCampaigns-csv`.

Execute `K2findCampaigns --help` or `K2findCampaigns-csv --help`
to be reminded of the use:
```
$ K2findCampaigns --help
usage: K2findCampaigns [-h] ra dec

Check if a celestial coordinate is (or was) observable by any past or future
observing campaign of NASA's K2 mission.

positional arguments:
  ra          Right Ascension in decimal degrees (J2000).
  dec         Declination in decimal degrees (J2000).

optional arguments:
  -h, --help  show this help message and exit
```

```
$ K2findCampaigns-csv --help
usage: K2findCampaigns-csv [-h] input_filename

Check which objects listed in a CSV table are (or were) observable by NASA's
K2 mission.

positional arguments:
  input_filename  Path to a comma-separated table containing columns
                  'ra,dec,kepmag' with ra and dec in decimal degrees.

optional arguments:
  -h, --help      show this help message and exit
```


### K2inMicrolensRegion

Finally, this package adds the `K2inMicrolensRegion` tool to check if a
celestial coordinate is inside the 3-megapixel superstamp region
that has been allocated to the [Campaign 9 microlensing experiment](http://keplerscience.arc.nasa.gov/k2-c9.html).
The stamp covers a large, ~contiguous region towards the Galactic Bulge.
```
$ K2inMicrolensRegion --help
usage: K2inMicrolensRegion [-h] ra dec

Check if a celestial coordinate is inside the K2C9 microlensing superstamp.

positional arguments:
  ra          Right Ascension in decimal degrees (J2000).
  dec         Declination in decimal degrees (J2000).

optional arguments:
  -h, --help  show this help message and exit
```


## Authors

`K2fov` was created by Fergal Mullally, Thomas Barclay, and Geert Barentsen
on behalf of the Kepler/K2 Guest Observer Office at NASA Ames.
Please cite this tool in your publications.
