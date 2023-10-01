import serial
import time
from datetime import datetime
import mysql.connector # for database updates


time.sleep(30) # delay for 30 seconds to avoid issues during computer startup


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


def add_to_database():
    global air_velocity_reading

    air_velocity_database = mysql.connector.connect(
        host="localhost",
        user="database_administrator",
        password="clearpath",
        database="air_velocity_database"
    )
    
    cursor = air_velocity_database.cursor()

    datetime_for_database = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    data_air_velocity_element = {
        'AirVelocityCentimetresPerSecond': air_velocity_reading,
        'Datetime': datetime_for_database
    }

    add_air_velocity_element = ("INSERT INTO AirVelocityMeasurements "
              "(AirvelocityCentimetresPerSecond, Datetime) "
              "VALUES (%(AirVelocityCentimetresPerSecond)s, %(Datetime)s)")

    # ElementIdentification is not included in data_air_velocity_element or add_air_velocity_element
    # This is because the table, AirVelocityMeasurements is configured to AutoIncrement this element

    cursor.execute(add_air_velocity_element, data_air_velocity_element)
    air_velocity_database.commit()
    cursor.close()
    air_velocity_database.close()

    print("UTC Datetime:         " + datetime_for_database)
    print("Air velocity reading: " + str(air_velocity_reading) + " cm/s")
    print("\r")


while True:
  get_air_velocity_metres()
  add_to_database()
  time.sleep(0.1)
