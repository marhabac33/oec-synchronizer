#!/usr/bin/python3
#
# Holds mappings from Open Exoplanet Catalogue (OEC) system xml tag/attribute
# values to csv column headings that hold the equivalent values from other
# catalogues.


from oec_sync_utils.constants import *


# Mapping Keys:
MAPPING = "mapping"
SOURCE = "source"
SYSTEM_MAP = "system"
BINARY_MAP = "binary"
STAR_MAP = "star"
EXOPLANET_MAP = "exoplanet"

# Index keys:
# Name tag mapping should always be first index.
NAME = 0
# Last update tag mapping should always be last index.
UPDATE = -1

# Subindex keys:
# Tag and Tag Key pair always first index.
ELM_TAG = 0
# List of element attributes always second index.
ELM_ATT = 1

# Sub-Subindex Keys
# Element/Attribute Tag always first index.
TAG = 0
# Element/Attribute Tag Key always second index.
TAG_KEY = 1


# XML Main Element Tags
ROOT_TAG = "system"
BINARY_TAG = "binary"
STAR_TAG = "star"
PLANET_TAG = "planet"

# XML Tags used in creating OEC system XML files.
# General use XML tags:
NAME_TAG = "name"
UNIT_ATT = "unit"
TYPE_ATT = "type"
ERROR_PLUS_ATT = "errorplus"
ERROR_MINUS_ATT = "errorminus"
LOWER_LIMIT_ATT = "lowerlimit"
UPPER_LIMIT_ATT = "upperlimit"

# System level XML tags:
SYSTEM_RIGHT_ASC_TAG = "rightascension"
SYSTEM_DECLINATION_TAG = "declination"
SYSTEM_DISTANCE_TAG = "distance"

# Binary level XML tags:
BINARY_POSITION_ANGLE_TAG = "positionangle"
BINARY_SEPARATION_TAG = "separation"

# Star level XML tags:
STAR_MAGB_TAG = "magB"
STAR_MAGV_TAG = "magV"
STAR_MAGR_TAG = "magR"
STAR_MAGJ_TAG = "magJ"
STAR_MAGH_TAG = "magH"
STAR_MAGI_TAG = "magI"
STAR_MAGK_TAG = "magK"
STAR_SPECTRAL_TYPE_TAG = "spectraltype"
STAR_TEMPERATURE_TAG = "temperature"
STAR_RADIUS_TAG = "radius"
STAR_MASS_TAG = "mass"
STAR_AGE_TAG = "age"
STAR_METALLICITY_TAG = "metallicity"

# Planet level XML tags:
PLANET_LIST_TAG = "list"
PLANET_MASS_TAG = "mass"
PLANET_RADIUS_TAG = "radius"
PLANET_PERIOD_TAG = "period"
PLANET_INCLINATION_TAG = "inclination"
PLANET_SEMIA_TAG = "semimajoraxis"
PLANET_ECCENTRICITY_TAG = "eccentricity"
PLANET_TRANSIT_TIME_TAG = "transittime"
PLANET_TEMPERATURE_TAG = "temperature"
PLANET_PERIASTRON_TAG = "periastron"
PLANET_PERIASTRON_TIME_TAG = "periastrontime"
PLANET_ASCENDINGNODE_TAG = "ascendingnode"
PLANET_LONGITUDE_TAG = "longitude"
PLANET_DESCRIPTION_TAG = "description"
PLANET_DISC_METHOD_TAG = "discoverymethod"
PLANET_DISC_YEAR_TAG = "discoveryyear"
PLANET_LAST_UPDATE_TAG = "lastupdate"
PLANET_IS_TRANSITING_TAG = "istransiting"
PLANET_IMAGE_TAG = "image"
PLANET_IMAGE_DES_TAG = "imagedescription"


# *****Mapping from XML tag/attribute value to csv column number*****

# Nasa Exoplanet Archive confirmed exoplanets mapping:
# Nasa Confirmed Planet System level mappings.
NASA_CON_SYSTEM_MAP = [
    ((NAME_TAG, "pl_hostname"),
     []),

    ((SYSTEM_RIGHT_ASC_TAG, "ra"),
     []),

    ((SYSTEM_DECLINATION_TAG, "dec_str"),
     []),

    ((SYSTEM_DISTANCE_TAG, "st_dist"),
     [(ERROR_PLUS_ATT, "st_disterr1"),
      (ERROR_MINUS_ATT, "st_disterr2")])
]
# Nasa Confirmed Planet Star level mappings.
NASA_CON_STAR_MAP = [
    ((NAME_TAG, "pl_hostname"),
     []),

    ((STAR_MASS_TAG, "st_mass"),
     [(ERROR_PLUS_ATT, "st_masserr1"),
      (ERROR_MINUS_ATT, "st_masserr2"),
      (TYPE_ATT, None)]),

    ((STAR_RADIUS_TAG, "st_rad"),
     [(ERROR_PLUS_ATT, "st_raderr1"),
      (ERROR_MINUS_ATT, "st_raderr2")]),

    ((STAR_TEMPERATURE_TAG, "st_teff"),
     [(ERROR_PLUS_ATT, "st_tefferr1"),
      (ERROR_MINUS_ATT, "st_tefferr2")]),

    ((STAR_MAGB_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGV_TAG, "st_optmag"),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGR_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGJ_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGH_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGI_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGK_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_SPECTRAL_TYPE_TAG, "st_spstr"),
     []),

    ((STAR_AGE_TAG, "st_age"),
     [(ERROR_PLUS_ATT, "st_ageerr1"),
      (ERROR_MINUS_ATT, "st_ageerr2")]),

    ((STAR_METALLICITY_TAG, "st_metfe"),
     [(ERROR_PLUS_ATT, "st_metfeerr1"),
      (ERROR_MINUS_ATT, "st_metfeerr2")])
]
# Nasa Confirmed Planet Planet level mappings.
# PLANET_LAST_UPDATE_TAG should always be last tag value.
NASA_CON_EXOPLANET_MAP = [
    ((NAME_TAG, "pl_name"),
     []),

    ((PLANET_LIST_TAG, None),
     []),

    ((PLANET_MASS_TAG, "pl_bmassj"),
     [(ERROR_PLUS_ATT, "pl_bmassjerr1"),
      (ERROR_MINUS_ATT, "pl_bmassjerr2"),
      (TYPE_ATT, "pl_bmassprov")]),

    ((PLANET_PERIOD_TAG, "pl_orbper"),
     [(ERROR_PLUS_ATT, "pl_orbpererr1"),
      (ERROR_MINUS_ATT, "pl_orbpererr2")]),

    ((PLANET_SEMIA_TAG, "pl_orbsmax"),
     [(ERROR_PLUS_ATT, "pl_orbsmaxerr1"),
      (ERROR_MINUS_ATT, "pl_orbsmaxerr2")]),

    ((PLANET_ECCENTRICITY_TAG, "pl_orbeccen"),
     [(ERROR_PLUS_ATT, "pl_orbeccenerr1"),
      (ERROR_MINUS_ATT, "pl_orbeccenerr2")]),

    ((PLANET_INCLINATION_TAG, "pl_orbincl"),
     [(ERROR_PLUS_ATT, "pl_orbinclerr1"),
      (ERROR_MINUS_ATT, "pl_orbinclerr2")]),

    ((PLANET_PERIASTRON_TAG, "pl_orblper"),
     [(ERROR_PLUS_ATT, "pl_orblpererr1"),
      (ERROR_MINUS_ATT, "pl_orblpererr2")]),

    ((PLANET_PERIASTRON_TIME_TAG, "pl_orbtper"),
     [(ERROR_PLUS_ATT, "pl_orbtpererr1"),
      (ERROR_MINUS_ATT, "pl_orbtpererr2")]),

    ((PLANET_ASCENDINGNODE_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((PLANET_RADIUS_TAG, "pl_radj"),
     [(ERROR_PLUS_ATT, "pl_radjerr1"),
      (ERROR_MINUS_ATT, "pl_radjerr2")]),

    ((PLANET_TEMPERATURE_TAG, "pl_eqt"),
     [(ERROR_PLUS_ATT, "pl_eqterr1"),
      (ERROR_MINUS_ATT, "pl_eqterr2")]),

    ((PLANET_LONGITUDE_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((PLANET_TRANSIT_TIME_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((PLANET_IS_TRANSITING_TAG, None),
     []),

    ((PLANET_DESCRIPTION_TAG, None),
     []),

    ((PLANET_IMAGE_TAG, None),
     []),

    ((PLANET_IMAGE_DES_TAG, None),
     []),

    ((PLANET_DISC_METHOD_TAG, "pl_discmethod"),
     []),

    ((PLANET_DISC_YEAR_TAG, "pl_disc"),
     []),

    ((PLANET_LAST_UPDATE_TAG, "rowupdate"),
     [])
]
NASA_CON_MAP = {MAPPING: NASA_CON_NAME,
                SOURCE: NASA_URL,
                SYSTEM_MAP: NASA_CON_SYSTEM_MAP,
                BINARY_MAP: None,
                STAR_MAP: NASA_CON_STAR_MAP,
                EXOPLANET_MAP: NASA_CON_EXOPLANET_MAP}


# Exoplanet.eu catalogue exoplanets mapping:
# Exoplanet.eu Confirmed Planet System level mappings.
EXO_EU_SYSTEM_MAP = [
    ((NAME_TAG, "star_name"),
     []),

    ((SYSTEM_RIGHT_ASC_TAG, "ra"),
     []),

    ((SYSTEM_DECLINATION_TAG, "dec"),
     []),
    
    ((SYSTEM_DISTANCE_TAG, "star_distance"),
     [(ERROR_PLUS_ATT, "star_distance_error_max"),
      (ERROR_MINUS_ATT, "star_distance_error_min")])
]
# Exoplanet.eu Confirmed Planet Star level mappings.
EXO_EU_STAR_MAP = [
    ((NAME_TAG, "star_name"),
     []),

    ((STAR_MASS_TAG, "star_mass"),
     [(ERROR_PLUS_ATT, "star_mass_error_max"),
      (ERROR_MINUS_ATT, "star_mass_error_min"),
      (TYPE_ATT, None)]),

    ((STAR_RADIUS_TAG, "star_radius"),
     [(ERROR_PLUS_ATT, "star_radius_error_max"),
      (ERROR_MINUS_ATT, "star_radius_error_min")]),

    ((STAR_TEMPERATURE_TAG, "star_teff"),
     [(ERROR_PLUS_ATT, "star_teff_error_max"),
      (ERROR_MINUS_ATT, "star_teff_error_min")]),

    ((STAR_MAGB_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGV_TAG, "mag_v"),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGR_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGJ_TAG, "mag_j"),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGH_TAG, "mag_h"),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGI_TAG, "mag_i"),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_MAGK_TAG, "mag_k"),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((STAR_SPECTRAL_TYPE_TAG,  "star_sp_type"),
     []),

    ((STAR_AGE_TAG, "star_age"),
     [(ERROR_PLUS_ATT, "star_age_error_max"),
      (ERROR_MINUS_ATT, "star_age_error_min")]),

    ((STAR_METALLICITY_TAG, "star_metallicity"),
     [(ERROR_PLUS_ATT, "star_metallicity_error_max"),
      (ERROR_MINUS_ATT, "star_metallicity_error_min")])
]
# Exoplanet.eu Confirmed Planet Star level mappings.
# PLANET_LAST_UPDATE_TAG should always be last tag value.
EXO_EU_EXOPLANET_MAP = [
    ((NAME_TAG, "# name"),
     []),

    ((PLANET_LIST_TAG, None),
     []),

    ((PLANET_MASS_TAG, "mass_sini"),
     [(ERROR_PLUS_ATT, "mass_sini_error_max"),
      (ERROR_MINUS_ATT, "mass_sini_error_min"),
      (TYPE_ATT, None)]),

    ((PLANET_PERIOD_TAG, "orbital_period"),
     [(ERROR_PLUS_ATT, "orbital_period_error_max"),
      (ERROR_MINUS_ATT, "orbital_period_error_min")]),

    ((PLANET_SEMIA_TAG, "semi_major_axis"),
     [(ERROR_PLUS_ATT, "semi_major_axis_error_max"),
      (ERROR_MINUS_ATT, "semi_major_axis_error_min")]),

    ((PLANET_ECCENTRICITY_TAG, "eccentricity"),
     [(ERROR_PLUS_ATT, "eccentricity_error_max"),
      (ERROR_MINUS_ATT, "eccentricity_error_min")]),

    ((PLANET_INCLINATION_TAG, "inclination"),
     [(ERROR_PLUS_ATT, "inclination_error_max"),
      (ERROR_MINUS_ATT, "inclination_error_min")]),

    ((PLANET_PERIASTRON_TAG, "omega"),
     [(ERROR_PLUS_ATT, "omega_error_max"),
      (ERROR_MINUS_ATT, "omega_error_min")]),

    ((PLANET_PERIASTRON_TIME_TAG, "tperi"),
     [(ERROR_PLUS_ATT, "tperi_error_max"),
      (ERROR_MINUS_ATT, "tperi_error_min")]),

    ((PLANET_ASCENDINGNODE_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((PLANET_RADIUS_TAG, "radius"),
     [(ERROR_PLUS_ATT, "radius_error_max"),
      (ERROR_MINUS_ATT, "radius_error_min")]),

    ((PLANET_TEMPERATURE_TAG, "temp_calculated"),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((PLANET_LONGITUDE_TAG, None),
     [(ERROR_PLUS_ATT, None),
      (ERROR_MINUS_ATT, None)]),

    ((PLANET_TRANSIT_TIME_TAG, "tzero_tr"),
     [(ERROR_PLUS_ATT, "tzero_tr_error_max"),
      (ERROR_MINUS_ATT, "tzero_tr_error_min")]),

    ((PLANET_IS_TRANSITING_TAG, None),
     []),

    ((PLANET_DESCRIPTION_TAG, None),
     []),

    ((PLANET_IMAGE_TAG, None),
     []),

    ((PLANET_IMAGE_DES_TAG, None),
     []),

    ((PLANET_DISC_METHOD_TAG, "detection_type"),
     []),

    ((PLANET_DISC_YEAR_TAG, "discovered"),
     []),

    ((PLANET_LAST_UPDATE_TAG, "updated"),
     [])
]
EXO_EU_MAP = {MAPPING: EXO_EU_NAME,
              SOURCE: EXOPLANET_URL,
              SYSTEM_MAP: EXO_EU_SYSTEM_MAP,
              BINARY_MAP: None,
              STAR_MAP: EXO_EU_STAR_MAP,
              EXOPLANET_MAP: EXO_EU_EXOPLANET_MAP}


# Sets containing elements that requier conversion to OEC values:
SYSTEM_RIGHT_ASC = set(["ra", "ra"])
DECLINATION = set(["dec"])
NASA_DECLINATION = set(["dec_str"])
NASA_EXOPLANET_NAME = set(["pl_name"])
ERROR_PLUS_MINUS = set([ERROR_PLUS_ATT, ERROR_MINUS_ATT])
DATES = set([PLANET_LAST_UPDATE_TAG])


# Catalogs to monitor. (test_planets.csv is temporary for testing.)
MONITORED_CATALOGUES = [NASA_CON_NAME, EXO_EU_NAME, 'test_planets.csv']
CATALOGUE_URLS = [(NASA_CON_NAME, NASA_URL), (EXO_EU_NAME, EXOPLANET_URL)]

# Tuples of catalogue names and their respective mappings.
CATALOGUE_TO_MAP = {NASA_CON_NAME: NASA_CON_MAP, EXO_EU_NAME: EXO_EU_MAP}

