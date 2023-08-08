import sys
sys.path.append('./libraries')

from ADCDevice import *
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime

class Reader:

    def __init__(self, DHTPin=11, PCF8574_address=0x27, PCF8574A_address = 0x3F) -> None:
        self.DHTPin = DHTPin
        self.PCF8574_address = PCF8574_address
        self.PCF8574A_address = PCF8574A_address
        
        self.setup_light()
        self.setup_dht()
        self.setup_lcd()

    def setup_light(self):
        self.adc = ADCDevice()
        if(self.adc.detectI2C(0x48)): # Detect the pcf8591.
            self.adc = PCF8591()
        elif(self.adc.detectI2C(0x4b)): # Detect the ads7830
            self.adc = ADS7830()
        else:
            print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
            exit(-1)

    def setup_dht(self):
        self.dht = DHT.DHT(self.DHTPin)

    def setup_lcd(self):
        # Create PCF8574 GPIO adapter.
        try:
            self.mcp = PCF8574_GPIO(self.PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(self.PCF8574A_address)
            except:
                print ('I2C Address Error!')
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)

        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)     # set number of LCD lines and columns

    def read_light(self):
        value = self.adc.analogRead(0)
        voltage = value / 255.0 * 3.3
        print ('ADC Value : %d, Voltage : %.2f'%(value,voltage))
        time.sleep(0.01)

        return {'value': value, 'voltage': voltage}

    def read_dht(self):
        for i in range(0,15):            
            chk = self.dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk is self.dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                print("DHT11,OK!")
                break
            sleep(0.1)
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(self.dht.humidity,self.dht.temperature))

        return {'humidity': self.dht.humidity, 'temp': self.dht.temperature}

    def set_lcd(self, light, humidity, temp):
        message = f"Light: {light}\nHum: {humidity}, Temp: {temp}"

        self.lcd.clear()
        self.lcd.setCursor(0,0)  # set cursor position
        self.lcd.message(message) # display

    def destroy_light(self):
        self.adc.close()
        GPIO.cleanup()

    def destroy_lcd(self):
        self.lcd.clear()

    def destroy_all(self):
        self.destroy_light()
        self.destroy_lcd()

    def debug_loop(self):
        while True:
            light_json = self.read_light()
            dht_json = self.read_dht()
            print("Light:", light_json)
            print("DHT:", dht_json)
            self.set_lcd(light_json['value'], dht_json['humidity'], dht_json['temp'])
            sleep(0.1)

if __name__ == "__main__":
    r = Reader()
    # Test components
    try:
        r.debug_loop()
    except KeyboardInterrupt:
        print("Keyboard interrupt.")
    except RuntimeError:
        print("Runtime error.")
    finally:
        r.destroy_all()