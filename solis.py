import minimalmodbus
import os
import paho.mqtt.client as mqtt
import json
import serial
import logging
import time

class SolisData:
  def __init__(self):
    self.acWatts = 0
    self.dcVolt = 0
    self.dcCurrent = 0
    self.acVolt = 0
    self.acCurrent = 0
    self.acFrequency = 0
    self.temperature = 0
    self.allTime = 0
    self.today = 0

logging.basicConfig(level=logging.INFO)
mqtt_host = os.getenv('MQTT_HOST')
mqtt_port = os.getenv('MQTT_PORT')  # 1883

def read_solis_data():
    """Read data from the Solis inverter."""
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 3

    success = True
    data = SolisData()
    try:
            data.acWatts = instrument.read_long(3004, functioncode=4, signed=False) #Read AC Watts as Unsigned 32-Bit (in W)
            data.dcVolt = instrument.read_register(3021, number_of_decimals=0, functioncode=4, signed=False) / 100 #Read DC volts as Unsigned 16-Bit (in V)
            data.dcCurrent = instrument.read_register(3022, number_of_decimals=0, functioncode=4, signed=False) #Read DC current as Unsigned 16-Bit (in A)
            data.acVolt = instrument.read_register(3035, number_of_decimals=0, functioncode=4, signed=False) / 10 #Read AC volts as Unsigned 16-Bit (in V)
            data.acCurrent = instrument.read_register(3038, number_of_decimals=0, functioncode=4, signed=False) #Read AC current as Unsigned 16-Bit (in A)
            data.acFrequency = instrument.read_register(3042, number_of_decimals=0, functioncode=4, signed=False) #Read AC frequency as Unsigned 16-Bit (in Hz)
            data.temperature = instrument.read_register(3041, number_of_decimals=0, functioncode=4, signed=True) / 10 #Read inverter temperature as Signed 16-Bit (in C)
            data.allTime = instrument.read_long(3008, functioncode=4, signed=False) #Read all time energy (kWh total) as Unsigned 32-Bit (in kWh)
            data.today = instrument.read_register(3014, number_of_decimals=1, functioncode=4, signed=False) #Read todays energy (kWh total) as 16-Bit (in kWh)
    except Exception as e:
            logging.error(f"Error reading data from Solis inverter: {e}")
            success = False

    return data, success

while True:
    data, success = read_solis_data()

    if success:
        client = mqtt.Client()
        try:
            client.connect(mqtt_host, int(mqtt_port), 60)
            client.publish("solis", payload=json.dumps(data.__dict__), qos=0, retain=False)
            client.disconnect()
        except Exception as e:
            logging.error(f"Error connecting to MQTT server: {e}")

    logging.info(f"Data read and published: {data.__dict__}")
    time.sleep(60)
