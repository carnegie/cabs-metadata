# Carnegie Analog Broadband Seismograph (CABS) Tape Metadata

This repository contains tape specific metadata for the CABS dataset. These
files provide information about each tape, which is not available as part of the
tape's magnetically recorded data, but collected from station service sheets,
notes written on the tape's reel or box cover, or deduced from observations
about the tape's content made during tape data processing.

## Parameter files

Parameter files for each tape, sorted by station. Parameter files are text files
formatted in Tom's Obvious, Minimal Language (TOML), which contain processing
parameters to turn raw digitized tape data into resample and properly time
stamped MiniSEED files using the program `capsproc`. Included parameters
describe the station clock model and its configuration, the start time of the
tape, and any other tape specific information necessary for processing.
Parameter files may also contain a list of 'hints', which provide information to
guide the time track decoding by augmenting missing or incorrect time stamps.
See the project documentation for details about parameter file contents.

## Calibration files

Information about known station calibration events recorded on each tape, sorted
by station. These files are tables in Comma Separated Value (CSV) format, that
list approximate start times for each known calibration event recorded on the
tape. The listed start times are merely meant to aid in locating any calibration
data in the time series; they may precede the exact start of each calibration
event by several minutes up to around an hour.

Most of the calibration times making up these tables were read from station
service sheets, but some were added after spotting additional calibration events
in the tape data. There may be additional undocuemnted calibration events
recorded in the dataset beyond the ones listed in these tables.

Calibration files are not needed for tape data processing via `cabsproc`.
However, they are useful for tape data quality control, and they may be of
interest for researchers trying to validate instrument response fucntions.

## Field notes

Scans of field notes for all tapes, except for a few tapes for which no original
notes could be found. Notes were mostly recorded on preprinted forms. Although
the forms varied by station and over time, they mostly record the same kind of
information throughout. Field notes were scanned to PDF files, some of which were
post-processed for improved contrast and to correct page orientation. A few files
contain annotations added after scanning.

Note: Since the PDF files are quite large, they are managed through the git Large
File Storage extension. You may need to install git-lfs on your system to work
with this part of the repository. See https://git-lfs.com/ for instructions.

## StationXML

ObsPy script to create channel metadata descriptions in StationXML format.
