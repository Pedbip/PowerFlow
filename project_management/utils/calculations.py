import math


# Conversion Functions
def amperage_to_wattage(amps, volts, pf: float | None = None) -> float:
    """Convert amperage to wattage."""
    return amps * volts * pf if pf is not None else amps * volts


def wattage_to_amperage(watts, volts, pf: float | None = None) -> float:
    """Convert wattage to amperage."""
    return watts / (volts * pf) if pf is not None else watts / volts


def wattage_to_kilowatt(watts) -> float:
    """Convert wattage to kilowatt."""
    return watts / 1000


def kilowatt_to_wattage(kilowatts) -> float:
    """Convert kilowatt to wattage."""
    return kilowatts * 1000


def kilowatt_to_amperage(kilowatts, volts, pf: float | None = None) -> float:
    """Convert kilowatt to amperage."""
    return kilowatts * 1000 / (volts * pf) if pf is not None else kilowatts * 1000 / volts


def amperage_to_kilowatt(amps, volts, pf: float | None = None) -> float:
    """Convert amperage to kilowatt."""
    return amps * volts * pf / 1000 if pf is not None else amps * volts / 1000


def kilowatt_to_horsepower(kilowatts) -> float:
    """Convert kilowatt to horsepower."""
    return kilowatts * 1.34102


def horsepower_to_kilowatt(horsepower) -> float:
    """Convert horsepower to kilowatt."""
    return horsepower / 1.34102


def horsepower_to_wattage(horsepower) -> float:
    """Convert horsepower to wattage."""
    return horsepower * 745.7


def wattage_to_horsepower(watts) -> float:
    """Convert wattage to horsepower."""
    return watts / 745.7


# Current Unit Conversions
def amps_to_milliamps(amps) -> float:
    """Convert amps to milliamps."""
    return amps * 1000


def milliamps_to_amps(milliamps) -> float:
    """Convert milliamps to amps."""
    return milliamps / 1000


def amps_to_microamps(amps) -> float:
    """Convert amps to microamps."""
    return amps * 1_000_000


def microamps_to_amps(microamps) -> float:
    """Convert microamps to amps."""
    return microamps / 1_000_000


def amps_to_nanouamps(amps) -> float:
    """Convert amps to nanouamps."""
    return amps * 1_000_000_000


def nanouamps_to_amps(nanouamps) -> float:
    """Convert nanouamps to amps."""
    return nanouamps / 1_000_000_000


def amps_to_picouamps(amps) -> float:
    """Convert amps to picouamps."""
    return amps * 1_000_000_000_000


def picouamps_to_amps(picouamps) -> float:
    """Convert picouamps to amps."""
    return picouamps / 1_000_000_000_000


def amps_to_femtoamps(amps) -> float:
    """Convert amps to femtoamps."""
    return amps * 1_000_000_000_000_000


def femtoamps_to_amps(femtoamps) -> float:
    """Convert femtoamps to amps."""
    return femtoamps / 1_000_000_000_000_000


def amps_to_attoamps(amps) -> float:
    """Convert amps to attoamps."""
    return amps * 1_000_000_000_000_000_000


def attoamps_to_amps(attoamps) -> float:
    """Convert attoamps to amps."""
    return attoamps / 1_000_000_000_000_000_000


def amps_to_zeptoamps(amps) -> float:
    """Convert amps to zeptoamps."""
    return amps * 1_000_000_000_000_000_000_000


def zeptoamps_to_amps(zeptoamps) -> float:
    """Convert zeptoamps to amps."""
    return zeptoamps / 1_000_000_000_000_000_000_000


def amps_to_yoctoamps(amps) -> float:
    """Convert amps to yoctoamps."""
    return amps * 1_000_000_000_000_000_000_000_000


def yoctoamps_to_amps(yoctoamps) -> float:
    """Convert yoctoamps to amps."""
    return yoctoamps / 1_000_000_000_000_000_000_000_000


# Ohm's Law Calculations
def resistance_to_voltage(resistance, current) -> float:
    """Calculate voltage from resistance and current."""
    return resistance * current


def voltage_to_resistance(voltage, current) -> float:
    """Calculate resistance from voltage and current."""
    return voltage / current


# Power Factor Calculations
def power_factor(real_power, apparent_power) -> float:
    """Calculate power factor."""
    return real_power / apparent_power if apparent_power != 0 else 0.0


def apparent_power(real_power, power_factor) -> float:
    """Calculate apparent power."""
    return real_power / power_factor if power_factor != 0 else 0.0


def real_power(apparent_power, power_factor) -> float:
    """Calculate real power."""
    return apparent_power * power_factor if power_factor != 0 else 0.0


def reactive_power(real_power, apparent_power) -> float:
    """Calculate reactive power."""
    return (apparent_power**2 - real_power**2)**0.5 if apparent_power > real_power else 0.0


def power_factor_angle(power_factor) -> float:
    """Calculate the power factor angle in degrees."""
    return math.degrees(math.acos(power_factor)) if -1 <= power_factor <= 1 else 0.0


def power_factor_angle_radians(power_factor) -> float:
    """Calculate the power factor angle in radians."""
    return math.acos(power_factor) if -1 <= power_factor <= 1 else 0.0


# Motor Efficiency Calculations
def motor_efficiency(rated_power, input_power) -> float:
    """Calculate motor efficiency."""
    return rated_power / input_power if input_power != 0 else 0.0


def motor_efficiency_percentage(rated_power, input_power) -> float:
    """Calculate motor efficiency in percentage."""
    return motor_efficiency(rated_power, input_power) * 100 if input_power != 0 else 0.0


def motor_power_factor(rated_power, input_power) -> float:
    """Calculate motor power factor."""
    return rated_power / input_power if input_power != 0 else 0.0


def motor_power_in_watts_monophasic(current, voltage, power_factor) -> float:
    """Calculate motor power in Watts for monophasic systems."""
    return current * voltage * power_factor if voltage != 0 else 0.0


def motor_power_in_watts_triphasic(current, voltage, power_factor) -> float:
    """Calculate motor power in Watts for triphasic systems."""
    return current * voltage * power_factor * 1.732 if voltage != 0 else 0.0

