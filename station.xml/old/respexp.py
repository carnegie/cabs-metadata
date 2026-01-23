import obspy
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
from obspy.clients.nrl import NRL
from obspy.core.inventory import Response


# By default this accesses the NRL online. Offline copies of the NRL can
# also be used instead
nrl = NRL()
# The contents of the NRL can be explored interactively in a Python prompt,
# see API documentation of NRL submodule:
# http://docs.obspy.org/packages/obspy.clients.nrl.html
# Here we assume that the end point of data logger and sensor are already
# known:
response = nrl.get_response( # doctest: +SKIP
    sensor_keys = ['Generic', 'Unity Velocity Sensor'],
    datalogger_keys = ['Generic', 'Unity'])
print(response)
# TODO working with NRL above will be main difficulty!!!


print("-------------------")
for s in response.response_stages:
    print(s)
print("-------------------")

##############

from obspy.core.inventory import CoefficientsTypeResponseStage
from obspy.core.inventory import PolesZerosResponseStage
from obspy.core.inventory import InstrumentSensitivity


# for later
stage1 = PolesZerosResponseStage(
    stage_sequence_number = 1,
    stage_gain = 1.0,
    stage_gain_frequency = 1.0,
    input_units = "V",
    output_units = "V",
    pz_transfer_function_type = "LAPLACE (RADIANS/SECOND)",
    normalization_frequency = 1.0,
    zeros = [],
    poles = [],
    normalization_factor=1.0,
    #resource_id=None,
    #resource_id2=None,
    #name=None,
    input_units_description="Volts",
    output_units_description="Volts",
    description="Playback amplifier",
    decimation_input_sample_rate=None,
    decimation_factor=None,
    decimation_offset=None,
    decimation_delay=None,
    decimation_correction=None)



#########################

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




resp = Response(
    #resource_id=None,
    instrument_sensitivity = sens,
    #instrument_polynomial=None,
    response_stages = [cabsproc])

print(resp)
