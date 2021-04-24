# solis 4g reader to mqtt

The script reads the solis 4g converter and push the data to a MQ server.


## Requirements
- Raspberry pi or equal (python3 need to be installed)
- Two kabels that need to be solderd or crocodile kabels
- MAX485 module for RS485 serial communication USB OR some other hardware that can do this

## Hardware setup
On the MAX485 module you have two input ports called A and B. On the Solis 4g converter you have 4 numbered COM ports.
You need to connect port 3 of the Solis to port A of the MAX485 module and port 4 to the B.

## Software setup
In my case I needed a driver for my MAX485 module. If you have the same please check [this site](https://learn.sparkfun.com/tutorials/how-to-install-ch340-drivers/all#drivers-if-you-need-them).

Download the python file on your system and try to run it using ```python3 solis.py```.
It is possible you need to install additional python modules. You can do this by calling ```pip3 install <module>```.

The Python script does use following modules:
- minimalmodbus
- paho.mqtt

To run the script on a regular basis create a cron job for it (```contab -e```).
For example I have a cronjob that calls the script every five minutes:
```*/5 * * * *  python3 /home/ubuntu/solisApp/solis.py```.

## Configuration
The script need to be changed to connect to the correct mqtt host.
You can do this by changing ```mqtt_host``` en ```mqtt_port``` properties in the file.