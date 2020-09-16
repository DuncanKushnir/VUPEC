# Linear
MILE_KM = 1.609344
METER_INCH = 0.0254

# Volume
GALUS_L = 4.54609
GALIMP_L = 3.7854

# Mass
KG_LB = 2.2046

# Temp
C_KELVIN = 273.15

# Gravity
EARTH_G = 9.80665

# Air Standards
AIR_STD_PRES = 101325  # Pa
AIR_DENS_ISA = 1.225  # kg/m3
AIR_TEMP_ISA = 15 + C_KELVIN  # Kelvin
AIR_PRES_ISA = AIR_STD_PRES
AIR_STD_GAS_CONST = 287.058  # J/(kg.K)
AIR_UNIV_GAS_CONST = 8.31432  # N.m/mol.K
MM_EARTH_AIR = 0.0289644  # kg/mol
AIR_STD_LAPSE = -0.0065  # degK / m
AIR_ALT_EXP = (-1 * EARTH_G * MM_EARTH_AIR) / (AIR_UNIV_GAS_CONST * AIR_STD_LAPSE)


# ENERGY
KWH_MJ = 3.6
KWH_KJ = 3600
