import serial
import time

def get_air_velocity_metres():
  global air_velocity_reading

  with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
    serial_read_bytes = ser.readline()

  # convert to string, and remove byte packaging characters
  air_velocity_string = str(serial_read_bytes)
  air_velocity_string = air_velocity_string.rstrip(air_velocity_string[-1])
  air_velocity_string = air_velocity_string.rstrip(air_velocity_string[-1])
  air_velocity_string = air_velocity_string.rstrip(air_velocity_string[-1])
  air_velocity_string = air_velocity_string.lstrip(air_velocity_string[0])
  air_velocity_string = air_velocity_string.lstrip(air_velocity_string[0])

  # return integer of the air speed in cm/s
  air_velocity_reading = int(float(air_velocity_string)*100)


while True:
  # print(str(get_air_velocity_metres()) + " cm/s")
  time.sleep(0.1)
