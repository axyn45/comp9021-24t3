# Written by Eric Martin for COMP9021


# Prints out a conversion table of temperatures from Fahrenheit
# to Celsius degrees, with the former ranging from 0 to 300 in
# steps of 20.


min_temperature = 0
max_temperature = 100
step = 10
# \t: A tab
print('Celsius Fahrenheit\n')
# We let fahrenheit take the values
# - min_temperature
# - min_temperature + step
# - min_temperature + 2 * step
# - min_temperature + 3 * step
# ...
# up to the largest value smaller than max_temperature + step
for celsius in range(min_temperature, max_temperature + step, step):
    # celsius = 5 * (fahrenheit - 32) / 9
    fahrenheit=celsius*9/5+32
    # {:10d} or {:10}: fahrenheit as a decimal number in a field
    # of width 10.
    # {:7.1f}: celsius as a floating point number in a field of
    # width 7 with 1 digit after the decimal point.
    print(f'{celsius:7}\t{fahrenheit:11.0f}')

