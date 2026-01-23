#! /bin/zsh

# Script to run cabs.py to build StationXML; then validate the output.
# `cabs.py` requires ObsPy. This script will run the python3 interpeter inside
# a conda environment named `obspy`.
# Note that some ObsPy versions do not work correctly; version 1.4.0 is known to work.

output="."
project="cabs"
strict=false

echo "Building StationXML file"
conda run -n obspy python3 $project.py # must use obspy-1.4.0 inside environment

echo "Validating StationXML file"
if $strict; then
    # Make unit capitalization consistent with modern StationXML conventions
    sed -i '' -e 's/COUNTS/counts/g ; s/M\/S/m\/s/g' $output/$project.station.xml
    java -jar stationxml-validator-1.7.5.jar --input $output/$project.station.xml
else
    # Use --ignore-warnings in validator to skip unit name conversion
    java -jar stationxml-validator-1.7.5.jar --input $output/$project.station.xml --ignore-warnings
fi
