# air_velocity_testing

<br/>

## Using Grafana

Assuming the `a300-testing-1` server is running on the company LAN, you can access it onsite or through the VPN by going to a your browser and entering the URL [a300-testing-1:3000](http://a300-testing-1:3000).
If you cannot connect, it is likely due to:
1.  The server is not on,
2.  There is an issue with one of the programs / applications on the server,
3.  Or the company's DNS is not converting `a300-testing-1` to the server's IP address.

Once you get to the Grafana login page, enter:
- Username: `admin`
- Password: `clearpath`

<center><img src="/readme_assets/readme_grafana_login.png" width="800"/></center>

Once logged in, you should see the _Air Velocity_ dashboard.
You can change the x-axis timespan using the dropdown in the top right corner, which is labelled `Last 5 minutes` in the attached screenshot.
There is also a refresh button, which adds the latest data into the graph, though it should already be configured to update every 5 seconds.

<center><img src="/readme_assets/readme_grafana_plot.png" width="800"/></center>

<br/>

## Reviewing MariaDB / MySQL

|   Command Type | Command                                                                                          | Purpose                                                                |
|   :----------- | :----------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------|
|   bash         | `sudo mysql;`                                                                                    | enters the MySQL terminal                                              |
|   MySQL        | `use air_velocity_database;`                                                                     | connect to the air_velocity_database                                   |
|   MySQL        | `show full tables;`                                                                              | list all the tables inside the current database                        |
|   MySQL        | `show columns in AirVelocityMeasurements;`                                                       | lists the columens in the table AirVelocityMeasurements                |
|   MySQL        | `select * from AirVelocityMeasurements;`                                                         | lists all rows and related data from the table AirVelocityMeasurements |
|   MySQL        | `delete from AirVelocityMeasurements;`                                                           | deletes all rows from the table AirVelocityMeasurements                |
|   MySQL        | `SELECT user FROM mysql.user;`                                                                   | view all users                                                         |
|   MySQL        | `ALTER TABLE AirVelocityMeasurements ADD COLUMN Datetime DATETIME(6) DEFAULT CURRENT_TIMESTAMP;` | add column                                                             |
|   MySQL        | `ALTER TABLE AirVelocityMeasurements DROP COLUMN Datetime;`                                      | removes column                                                         |

<br/>

## Sensor and Microcontroller Installation

This testing setup uses a [SparkFun KIT-21310](https://www.sparkfun.com/products/21310), which includes:
-   Development board, RedBoard Artemis Nano ( _DEV-15443_ )
-   Sensor, FS3000-1015 ( _SEN-18768_ )

There are detailed instructions on the SparkFun website, but my notes are:
1.  Connect the sensor to the development board using the supplied Qwiic cable.
2.  Connect the development board to your development computer using the supplied USB cable.
3.  Open the _Arduino IDE_ application on your development computer.
4.  Make sure _Arduino IDE_'s preferences for board manager include the SparkFun JSON URL:
    ```
    https://raw.githubusercontent.com/sparkfun/Arduino_Apollo3/main/package_sparkfun_apollo3_index.json
    ```

    Note: this link worked in 2023-September, but may change over time.
5.  Set the port in _Arduino IDE_.
6.  Set the board to _SparkFun Apollo3 → RedBoard Artemis Nano_.
7.  Use the source file `air_velocity_testing.ino` from this repository.
8.  Upload the sketch.
9.  Using _Arduino IDE_'s serial monitor, confirm you are getting _cm/s_ integers every 0.1 seconds, when set to 115200 baud.

<br/>

## Computer Installation

1.  Set up a mini-ITX computer with Ubuntu 22.04
2.  Adding serial device permissions
    -   Serial device found: `Bus 001 Device 006: ID 1a86:7523 QinHeng Electronics CH340 serial converter`
    -   Added permissions for the serial port: `sudo chown administrator /dev/ttyUSB0`
3.  Install Python tools and libraries
    -   `sudo apt install python3-pip`
    -   `sudo python3 -m pip install pyserial`
    -   `sudo pip3 install mysql-connector-python`
4.  Install and configure [MariaDB](https://mariadb.com/kb/en/installing-mariadb-deb-files/#installing-mariadb-packages-with-apt)
    1.  Install the required tools on Ubuntu:
        ```
        sudo apt-get install mariadb-server libmariadb3 libmariadb-dev
        ```
    
    2.  After installing, start a MySQL terminal:
        ```
        sudo mysql
        ```
    
    3.  Then create a database, changing these vales to whatever you like.
        -   `database_administrator`
        -   `database_administrator_password`
        ```
        create user database_administrator identified by 'database_administrators_password';
        ```
        Note that the `;` line ending is important for SQL syntax.
        I used values of:
        -   `database_administrator`
        -   `clearpath`

    4.  Grant privileges to this user:
        ```
        grant all privileges on *.* to 'database_administrator' with grant option;
        ```

    5.  Next, create a database:
        ```
        create database air_velocity_database;
        ```
        -   This new database is named `air_velocity_database`

    6.  Connect to the database:
        ```
        use air_velocity_database;
        ```
        -   The prompt will change to MariaDB `[air_velocity_database]>`
        -   The prompt was MariaDB `[(none)]>`

    7.  Create a table inside the `air_velocity_database` database:
        ```
        CREATE TABLE AirVelocityMeasurements (
        ElementIdentification BIGINT NOT NULL AUTO_INCREMENT,
        AirVelocityCentimetresPerSecond SMALLINT NOT NULL,
        Datetime DATETIME(6) CURRENT_TIMESTAMP,
        PRIMARY KEY ( ElementIdentification )
        );
        ```

        -   This is a table named AirVelocityMeasurements. 
            It has columns of:
            -   ElementIdentification
            -   AirVelocityCentimetresPerSecond
            -   TimestampValue
        -   The ElementIdentification column is set as the primary key.

    8.  Confirm that the table and columns were configured:
        ```
        show columns in AirVelocityMeasurements;    
        ```
    9.  In a bash terminal, enter this command to make MariaDB start after computer startup:
        ```
        sudo systemctl enable mariadb
        ```

5.  Grafana installation and configuration
    1.  [Install Grafana](https://grafana.com/grafana/download/10.1.4)
        ```
        sudo apt-get install -y adduser libfontconfig1 musl
        wget https://dl.grafana.com/enterprise/release/grafana-enterprise_10.1.4_amd64.deb
        sudo dpkg -i grafana-enterprise_10.1.4_amd64.deb
        ```
    2.  [Starting Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/start-restart-grafana/)
        ```
        sudo systemctl daemon-reload
        sudo systemctl start grafana-server
        sudo systemctl status grafana-server
        ```
    
        To get Grafana to automatically start after the computer boot:
        ```
        sudo systemctl enable grafana-server.service
        ```
    3.  Sign into Grafana
        -   Go to Chrome or Firefox and enter the URL http://localhost:3000/
        -   Username: `admin`
        -   Password: `admin`
    4.  Click on the button `Add your first datasource`
    5.  Select `MySQL`
    6.  On the MySQL configuration page, enter these fields:
        |   Field       |   Value                   |
        |   :---------- |   :---------------------- |
        |   Name        |   Air-Velocity-Source     |
        |   Default     |   Yes / Enabled           |
        |   Host        |   localhost:3306          |
        |   Datebase    |   air_velocity_database   |
        |   User        |   database_administrator  |
        |   Password    |   clearpath               |

        Then select the `Save and Test` button.
    7.  Create a dashboard with a `Time series` plot`.
        You can manually select the fields of interest, or select `code` to enter an SQL expression.
        The `Run query` button will allow you to test the query before saving it.

        This is the SQL expression used to create the attached plot:

        ```
        SELECT AirVelocityCentimetresPerSecond, Datetime FROM air_velocity_database.AirVelocityMeasurements
        ```

        <center><img src="/readme_assets/readme_grafana_sql.png" width="800"/></center>

        Note: Grafana requires a row's time value to have the datetime format in MySQL, including six decimal points representing microseconds.
        Grafana also needs values to be aligned with UTC time, not local time.
        In Python, this is created with:
        
        ```
        datetime_for_database = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        ```
6.  Configure serial /dev/tty connection with microcontroller.

    Make sure the SparkFun development board and sensor are attached to the computer with the supplied USB cable.
    Both the development board and sensor should have red LEDs to confirm that they are powered.

    The device was not appearing as ttyUSB0 after computer startup, but would appear after unplugging and then plugging in the USB cable again.
    This led me to look into udev rules, and eventually find [this forum](https://askubuntu.com/questions/1403705/dev-ttyusb0-not-present-in-ubuntu-22-04).
    This command resolved the issue:
    ```
    sudo apt remove brltty
    ```

    Note, this was the information I got from `sudo dmesg` related to the SparkFun Artemis Nano microcontroller:
    ```
    ATTRS{product}=="USB Serial"
    ATTRS{idProduct}=="7523"
    ATTRS{idVendor}=="1a86"
    ```
    
    The full output is saved to `./readme_assets/dmesg_output`.

7.  Configure the Python program to run during computer startup:
    1.  Copy the Python file to `/usr/bin/`.
    2.  Give the Python file `data_logging.py` _Executing_ permissions, so it can run as a program:
        ```
        sudo chmod +x /usr/bin/data_logging.py
        ```
    3.  Copy _datalogging.service_ to `/etc/systemd/system/`.
    4.  In a termainal, run the commands:
        ```
        sudo systemctl daemon-reload
        sudo systemctl start datalogging.service
        sudo systemctl enable datalogging.service
        ```
        You can then confirm that the service is running using:
        ```
        sudo systemctl status datalogging.service
        ```
