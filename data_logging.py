import serial
import time

def get_air_velocity_metres():
  with serial.Serial('COM5', 115200, timeout=1) as ser:
    serial_read_bytes = ser.readline()

  # convert to string, and remove byte packaging characters
  air_velocity_string = str(serial_read_bytes)
  air_velocity_string = air_velocity_string.rstrip(air_velocity_string[-1])
  air_velocity_string = air_velocity_string.rstrip(air_velocity_string[-1])
  air_velocity_string = air_velocity_string.rstrip(air_velocity_string[-1])
  air_velocity_string = air_velocity_string.lstrip(air_velocity_string[0])
  air_velocity_string = air_velocity_string.lstrip(air_velocity_string[0])

  # return float of the air speed in m/s
  return float(air_velocity_string)


while True:
  print(str(get_air_velocity_metres()) + " m/s")
  time.sleep(0.1)
