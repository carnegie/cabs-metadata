import os
import warnings

try:
    from obspy.clients.nrl import NRL

except ImportError:
    raise SystemExit('Error: This script requires ObsPy, which failed to import. Perhaps you meant to run this\n'
                     '       inside a conda environment that you forgot to activate, or such?')

nrl_home = os.getenv('NRL_HOME', False)
if not os.path.isdir(nrl_home):
    raise SystemExit('Error: This script requires access to a local copy of the Nominal Response Library (NRL).\n' 
                     '       The environment variable $NRL_HOME must point to a directory containing such copy.\n'
                     '       (See the NRL homepage https://ds.iris.edu/ds/nrl/ for download instructions;\n'
                     '       either RESP or StationXML version of the NRL should work.)')

nrl = NRL(nrl_home)

from obspy import read_inventory
from obspy.core.inventory.util import Equipment

from obspy.core.inventory import Inventory
from obspy.core.inventory import Network, Station, Channel, Site
from obspy.core.inventory import CoefficientsTypeResponseStage
from obspy.core.inventory import InstrumentSensitivity
from obspy.core.inventory import Response
from obspy import UTCDateTime


# By default this accesses the NRL online. Offline copies of the NRL can
# also be used instead
#nrl = NRL()
# The contents of the NRL can be explored interactively in a Python prompt,
# see API documentation of NRL submodule:
# http://docs.obspy.org/packages/obspy.clients.nrl.html
# Here we assume that the end point of data logger and sensor are already
# known:


# REF TEK RT72A-08 16-bit data logger configurations:
rt72a_10hz_hi = ['REFTEK', '72A08-16bit', '32', '16 bits', '10 Hz']
rt72a_10hz_lo = ['REFTEK', '72A08-16bit', '1', '16 bits', '10 Hz']
rt72a_50hz_hi = ['REFTEK', '72A08-16bit', '32', '16 bits', '50 Hz']

# Streckeisen STS-2 sensor (TODO: check generation):
sts2 = ['Streckeisen', 'STS-2', '1', '1500']

# Sensor/datalogger combinations:
resp_sts2_10hz_hi = nrl.get_response(sensor_keys=sts2, datalogger_keys=rt72a_10hz_hi)
resp_sts2_10hz_lo = nrl.get_response(sensor_keys=sts2, datalogger_keys=rt72a_10hz_lo)
resp_sts2_50hz_hi = nrl.get_response(sensor_keys=sts2, datalogger_keys=rt72a_50hz_hi)

# Instrument configurations

def sts_2(serial_number):
    return Equipment(
        type="seismometer",
        description="Streckeisen STS-2",
        manufacturer="Streckeisen",
        model="STS-2",
        serial_number=serial_number)

def rt72a(serial_number):
    return Equipment(
        type="data_logger",
        description="REF TEK RT72A-08",
        manufacturer="REF TEK",
        model="RT72A-08",
        serial_number=serial_number)

# 10Hz high-gain setup for continuous data

def append_10hz_hi_channels(sta, response, sensor, logger, start_date=None, end_date=None, location_code=""):
    def channel(code, azimuth, dip):
        return Channel(
            code=code,
            location_code=location_code,
            latitude=sta.latitude,
            longitude=sta.longitude,
            elevation=sta.elevation,
            depth=0.0,
            azimuth=azimuth,
            dip=dip,
            sample_rate=10,
            start_date=sta.start_date if start_date is None else start_date,
            end_date=sta.end_date if end_date is None else end_date,
            response=response,
            sensor=sensor,
            data_logger=logger)
    sta.channels.append(channel("LHN", 0.0, 0.0))
    sta.channels.append(channel("LHE", 90.0, 0.0))
    sta.channels.append(channel("LHZ", 0.0, -90.0))

def append_sts2_10hz_hi_channels(sta, sensor, logger, start_date=None, end_date=None, location_code=""):
    append_10hz_hi_channels(sta, resp_sts2_10hz_hi, ##
                          sts_2(sensor), rt72a(logger),
                          start_date, end_date, location_code)

# 50Hz high-gain setup for subsets of data.

def append_50hz_hi_channels(sta, response, sensor, logger, start_date=None, end_date=None, location_code=""):
    def channel(code, azimuth, dip):
        return Channel(
            code=code,
            location_code=location_code,
            latitude=sta.latitude,
            longitude=sta.longitude,
            elevation=sta.elevation,
            depth=0.0,
            azimuth=azimuth,
            dip=dip,
            sample_rate=50,
            start_date=sta.start_date if start_date is None else start_date,
            end_date=sta.end_date if end_date is None else end_date,
            response=response,
            sensor=sensor,
            data_logger=logger)
    sta.channels.append(channel("BHN", 0.0, 0.0))
    sta.channels.append(channel("BHE", 90.0, 0.0))
    sta.channels.append(channel("BHZ", 0.0, -90.0))

def append_sts2_50hz_hi_channels(sta, sensor, logger, start_date=None, end_date=None, location_code=""):
    append_50hz_hi_channels(sta, resp_sts2_50hz_hi, ##
                            sts_2(sensor), rt72a(logger),
                            start_date, end_date, location_code)

# TODO there should be also 10Hz low-gain data


# Helper functions
# TODO is the fix_dates step really necessary in this way?

def fix_dates(sta):
    sta.start_date = sta.creation_date
    sta.end_date = sta.termination_date
    return sta

def append_station(net, sta):
    sta.start_date = sta.creation_date
    sta.end_date = sta.termination_date
    net.stations.append(sta)

# Network setup

inv = Inventory(
    networks=[],
    source="Carnegie Institution for Science")

# CABS network code DT:
# https://fdsn.org/networks/detail/DT/

network_end=UTCDateTime(2003, 12, 31)

net = Network(
    code="DT",
    stations=[],
    description="Carnegie Analog Broadband Seismograph Network",
    start_date=UTCDateTime(1994, 1, 1),
    end_date=network_end)

# -------------------------------------------------------------------------
# DT.AKU
aku = fix_dates(Station(
    code="AKU",
    latitude=65.686,
    longitude=-18.099,
    elevation=25.0,
    creation_date=UTCDateTime(1972, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Akureyri, Iceland")))
append_sts2_10hz_hi_channels(aku, "", "")
append_station(net, aku)

# DT.CUZ
cuz = fix_dates(Station(
    code="CUZ",
    latitude=-13.525,
    longitude=-71.938,
    elevation=3390.0,
    creation_date=UTCDateTime(1966, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Cuzco, Peru")))
append_sts2_10hz_hi_channels(cuz, "", "")
append_station(net, cuz)

# DT.DTM
dtm = fix_dates(Station(
    code="DTM",
    latitude=38.959,
    longitude=-77.063,
    elevation=100.0,
    creation_date=UTCDateTime(1966, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Washington DC, USA")))
append_sts2_10hz_hi_channels(dtm, "", "")
append_station(net, dtm)

# DT.KMU
kmu = fix_dates(Station(
    code="KMU",
    latitude=42.238,
    longitude=142.967,
    elevation=50.0,
    creation_date=UTCDateTime(1967, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Kamikineusu, Japan")))
append_sts2_10hz_hi_channels(kmu, "", "")
append_station(net, kmu)

# DT.MAT
mat = fix_dates(Station(
    code="MAT",
    latitude=36.543,
    longitude=138.207,
    elevation=650.0,
    creation_date=UTCDateTime(1967, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Matsushiro, Japan")))
append_sts2_10hz_hi_channels(mat, "", "")
append_station(net, mat)

# DT.PMG
pmg = fix_dates(Station(
    code="PMG",
    latitude=-9.406,
    longitude=147.159,
    elevation=60.0,
    creation_date=UTCDateTime(1966, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Port Moresby, Papua New Guinea")))
append_sts2_10hz_hi_channels(pmg, "", "")
append_station(net, pmg)

# DT.SWU
swu = fix_dates(Station(
    code="SWU",
    latitude=39.49,
    longitude=140.79,
    elevation=50.0, # TODO check
    creation_date=UTCDateTime(1984, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Sawauichi, Japan")))
append_sts2_10hz_hi_channels(swu, "", "")
append_station(net, swu)

# DT.TCC
tcc = fix_dates(Station(
    code="TCC",
    latitude=-22.275,
    longitude=-68.172,
    elevation=2500.0,
    creation_date=UTCDateTime(1965, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Toconce, Chile")))
append_sts2_10hz_hi_channels(tcc, "", "")
append_station(net, tcc)

# DT.TRU
tru = fix_dates(Station(
    code="TRU",
    latitude=-8.078,
    longitude=-78.861,
    elevation=2200.0, # TODO check
    creation_date=UTCDateTime(1967, 1, 1, 0),
    termination_date=network_end,
    site=Site(name="Trujillo, Peru")))
append_sts2_10hz_hi_channels(tru, "", "")
append_station(net, tru)

# -------------------------------------------------------------------------

# Finish up ObsPy inventory data structure

inv.networks.append(net)

# Setup output directory

OUTPUT_DIR = "output"
os.mkdir(OUTPUT_DIR)

# Write metadata to a StationXML file. We also force a validation against
# the StationXML schema to ensure it produces a valid StationXML file.
#
# Note that it is also possible to serialize to any of the other inventory
# output formats ObsPy supports.
filename = f"{OUTPUT_DIR}/cabs.station.xml"
inv.write(filename, format="stationxml", validate=True)

filename = f"{OUTPUT_DIR}/cabs.station.kml"
inv.write(filename, format="kml")

# ---------------------
# From here onwards:
# Produce SAC-PZ files for local use

def polezero_f_mod(network, station, channel, sac_pz):
    return f"""* **********************************
* NETWORK   (KNETWK): {network}
* STATION    (KSTNM): {station}
* LOCATION   (KHOLE): 
* CHANNEL   (KCMPNM): {channel}
* **********************************
{sac_pz}"""

for network in inv:
    for station in network:
        for channel in station:
            selected_inv = inv.select(network=network.code, station=station.code, channel=channel.code)
            filename = f"{OUTPUT_DIR}/{network.code}.{station.code}..{channel.code}.pz"

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                selected_inv.write(filename, format="sacpz")
