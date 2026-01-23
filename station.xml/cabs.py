import obspy
from obspy.core.inventory import Inventory, Network, Station, Channel, Site


#########################
from obspy.core.inventory import CoefficientsTypeResponseStage
from obspy.core.inventory import InstrumentSensitivity
from obspy.core.inventory import Response

cabsproc = CoefficientsTypeResponseStage(
    stage_sequence_number = 1,
    stage_gain = 1.0,
    stage_gain_frequency = 1.0,
    input_units = "COUNTS",
    output_units = "COUNTS",
    cf_transfer_function_type = "DIGITAL",
    name = "cabsproc",
    numerator=[1.0],
    denominator=[],
    input_units_description="Digital counts",
    output_units_description="Digital counts",
    description = "Resampling and time stamping software",
    decimation_input_sample_rate=100,
    decimation_factor=1,
    decimation_offset=0,
    decimation_delay=0.0,
    decimation_correction=0.0)

print(cabsproc)

sens = InstrumentSensitivity(
    value = 1.0,
    frequency = 1.0,
    input_units = "COUNTS",
    output_units = "COUNTS",
    input_units_description = "Digital counts",
    output_units_description = "Digitial counts",
    # frequency_range_start=None,
    # frequency_range_end=None,
    # frequency_range_db_variation=None
    )

response = Response(
    #resource_id=None,
    instrument_sensitivity = sens,
    #instrument_polynomial=None,     # should there be one?
    response_stages = [cabsproc])

print(response)

###########################################################


# We'll first create all the various objects. These strongly follow the
# hierarchy of StationXML files.
inv = Inventory(
    networks = [],
    source = "Carnegie Institution of Washington") # TODO

net = Network(
    code = "DT",
    stations = [],
    description = "Carnegie Analog Broadband Seismograph Network",
    start_date = obspy.UTCDateTime(1965, 1, 1), # TODO end date!!
    end_date = obspy.UTCDateTime(2003, 12, 31)) # TODO end date!!

cuz = Station(
    code = "CUZ",
    latitude = -13.563,
    longitude = -71.877,
    elevation = 3285.0,
    creation_date = obspy.UTCDateTime(1966, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1986, 12, 31), # TODO
    site = Site(name = "Cuzco, Peru"))

tcc = Station(
    code = "TCC",
    latitude = -22.275,
    longitude = -68.172,
    elevation = 3371.0,
    creation_date = obspy.UTCDateTime(1965, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1971, 12, 31), # TODO
    site = Site(name = "Toconce, Chile"))

tru = Station(
    code = "TRU",
    latitude = -8.078,
    longitude = -78.861,
    elevation = 208.0,
    creation_date = obspy.UTCDateTime(1967, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1986, 12, 31), # TODO
    site = Site(name = "Trujillo, Peru"))

kmu = Station(
    code = "KMU",
    latitude = 42.238,
    longitude = 142.967,
    elevation = 226.0,
    creation_date = obspy.UTCDateTime(1967, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1996, 12, 31), # TODO
    site = Site(name = "Kamikineusu, Japan"))

mat = Station(
    code = "MAT",
    latitude = 36.543,
    longitude = 138.207,
    elevation = 447.0,
    creation_date = obspy.UTCDateTime(1967, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1984, 12, 31), # TODO
    site = Site(name = "Matsushiro, Japan"))

swu = Station(
    code = "SWU",
    latitude = 39.490,
    longitude = 140.790,
    elevation = 487.0,
    creation_date = obspy.UTCDateTime(1984, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1996, 12, 31), # TODO
    site = Site(name = "Sawauchi, Japan"))

aku = Station(
    code = "AKU",
    latitude = 65.686,
    longitude = -18.099,
    elevation = 13.0,
    creation_date = obspy.UTCDateTime(1972, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(2003, 12, 31), # TODO
    site = Site(name = "Akureyri, Iceland"))

pmg = Station(
    code = "PMG",
    latitude = -9.406,
    longitude = 147.159,
    elevation = 88.0,
    creation_date = obspy.UTCDateTime(1966, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1992, 12, 31), # TODO
    site = Site(name = "Port Moresby, Papua New Guinea"))

dtm = Station(
    code = "DTM",
    latitude = 38.959,
    longitude = -77.063,
    elevation = 76.0,
    creation_date = obspy.UTCDateTime(1966, 1, 1), # TODO
    termination_date = obspy.UTCDateTime(1994, 12, 31), # TODO
    site = Site(name = "Washington DC, USA"))

# -------------------------------------------------------------------

def CabsChannelNI(sta, code, azimuth, dip):
    equipment = obspy.core.inventory.util.Equipment(
        description = "Carnegie Seismograph"
    )

    cha = Channel(
        code = code,
        location_code = "NI", # Narrow gap. Integrated
        latitude = sta.latitude,
        longitude = sta.longitude,
        elevation = sta.elevation,
        depth = 0.0,
        azimuth = azimuth,
        dip = dip,
        sample_rate = 100,
        start_date = sta.start_date,
        end_date = sta.end_date)

    cha.response = response
    cha.sensor = equipment
    return cha

def CabsChannelNN(sta, code, azimuth, dip):
    equipment = obspy.core.inventory.util.Equipment(
        description = "Carnegie Seismograph"
    )

    cha = Channel(
        code = code,
        location_code = "NN", # Narrow gap. Non-integrated
        latitude = sta.latitude,
        longitude = sta.longitude,
        elevation = sta.elevation,
        depth = 0.0,
        azimuth = azimuth,
        dip = dip,
        sample_rate = 100,
        start_date = sta.start_date,
        end_date = sta.end_date)

    cha.response = response
    cha.sensor = equipment
    return cha

def Cabs3CompChannels(sta):
    sta.start_date = sta.creation_date
    sta.end_date = sta.termination_date
    sta.channels.append(CabsChannelNI(sta, "HLZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "HLZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "EMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "EMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "HMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "HMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "EHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "EHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "HHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "HHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "TIM", 0.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "HLN", 0.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "HLN", 0.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "EMN", 0.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "EMN", 0.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "HMN", 0.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "HMN", 0.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "EHN", 0.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "EHN", 0.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "HHN", 0.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "HHN", 0.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "HLE", 90.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "HLE", 90.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "EME", 90.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "EME", 90.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "HME", 90.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "HME", 90.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "EHE", 90.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "EHE", 90.0, 0.0))
    sta.channels.append(CabsChannelNI(sta, "HHE", 90.0, 0.0))
    sta.channels.append(CabsChannelNN(sta, "HHE", 90.0, 0.0))

def Cabs1CompChannels(sta):
    sta.start_date = sta.creation_date
    sta.end_date = sta.termination_date
    sta.channels.append(CabsChannelNI(sta, "HLZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "HLZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "EMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "EMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "HMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "HMZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "EHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "EHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNI(sta, "HHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "HHZ", 0.0, -90.0))
    sta.channels.append(CabsChannelNN(sta, "TIM", 0.0, 0.0))


Cabs3CompChannels(cuz)
net.stations.append(cuz)
Cabs3CompChannels(tcc)
net.stations.append(tcc)
Cabs1CompChannels(tru)
net.stations.append(tru)
Cabs3CompChannels(kmu)
net.stations.append(kmu)
Cabs3CompChannels(mat)
net.stations.append(mat)
Cabs3CompChannels(swu)
net.stations.append(swu)
Cabs3CompChannels(aku)
net.stations.append(aku)
Cabs1CompChannels(pmg)
net.stations.append(pmg)
Cabs3CompChannels(dtm)
net.stations.append(dtm)

inv.networks.append(net)

# And finally write it to a StationXML file. We also force a validation against
# the StationXML schema to ensure it produces a valid StationXML file.
#
# Note that it is also possible to serialize to any of the other inventory
# output formats ObsPy supports.
filename = "cabs.station.xml"
inv.write(filename, format="stationxml", validate=True)
