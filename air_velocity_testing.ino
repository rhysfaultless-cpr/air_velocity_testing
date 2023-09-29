/******************************************************************************
  air_velocity_testing
  based on Sparkfun example: Example_01_BasicReadings.ino
  
  Read values of air velocity from the FS3000 sensor, print them to terminal.
  Prints raw data
  Note, the response time on the sensor is 125ms.

  Sparkfun example details:
    ExampleSparkFun FS3000 Arduino Library
    Pete Lewis @ SparkFun Electronics
    Original Creation Date: August 5th, 2021
    https://github.com/sparkfun/SparkFun_FS3000_Arduino_Library

  Development kit:
    SparkFun Air Velocity Sensor Breakout - FS3000-1015 (Qwiic)
    https://www.sparkfun.com/products/18768
******************************************************************************/

#include <Wire.h>
#include <SparkFun_FS3000_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_FS3000

FS3000 fs;

void setup()
{
  Serial.begin(115200);
  // Serial.println("Example 1 - Reading values from the FS3000");

  Wire.begin();

  /*
  if (fs.begin() == false) //Begin communication over I2C
  {
    Serial.println("The sensor did not respond. Please check wiring.");
    while(1); //Freeze
  }
  */

  // Set the range to match which version of the sensor you are using.
  // FS3000-1005 (0-7.23 m/sec) --->>>  AIRFLOW_RANGE_7_MPS
  // FS3000-1015 (0-15 m/sec)   --->>>  AIRFLOW_RANGE_15_MPS
  //fs.setRange(AIRFLOW_RANGE_7_MPS);
  fs.setRange(AIRFLOW_RANGE_15_MPS); 

  // Serial.println("Sensor is connected properly.");
}

void loop()
{
    // Serial.print("FS3000 Readings \tRaw: ");
    // Serial.print(fs.readRaw()); // note, this returns an int from 0-3686
    
    // Serial.print("\tm/s: ");
    // Serial.print(fs.readMetersPerSecond()); // note, this returns a float from 0-7.23 for the FS3000-1005, and 0-15 for the FS3000-1015 
    
    // Serial.print("\tmph: ");
    // Serial.println(fs.readMilesPerHour()); // note, this returns a float from 0-16.17 for the FS3000-1005, and 0-33.55 for the FS3000-1015 
    
    Serial.print(fs.readMetersPerSecond()); // note, this returns a float from 0-7.23 for the FS3000-1005, and 0-15 for the FS3000-1015 
    Serial.print('\n');
    delay(1000); // note, reponse time on the sensor is 125ms
}
