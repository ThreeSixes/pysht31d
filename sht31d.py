import smbus
import time

class sht31d:
    def __init__(self, i2cBusID = 1, sensAddr = 0x45):
        """
        Sensirion SHT31D high accuracy temp/humdity driver class.
        """
        
        # Get sensor address.
        self.__sensAddr = sensAddr
        
        # Single shot measurement mode commands
        self.cmdSSHighRepClkSt  = [0x24, 0x00]
        self.cmdSSMedRepClkSt   = [0x24, 0x0b]
        self.cmdSSLowRepClkSt   = [0x24, 0x16]
        self.cmdSSHighRep       = [0x24, 0x00]
        self.cmdSSMedRep        = [0x24, 0x0b]
        self.cmdSSLowRep        = [0x24, 0x16]
        
        # Periodic acquisition mode commands
        self.cmdCntHiRepx5Hz    = [0x20, 0x32]
        self.cmdCntMedRepx5Hz   = [0x20, 0x24]
        self.cmdCntLowRepx5Hz   = [0x20, 0x2f]
        self.cmdCntHiRep1Hz     = [0x21, 0x30]
        self.cmdCntMedRep1Hz    = [0x21, 0x26]
        self.cmdCntLowRep1Hz    = [0x21, 0x2d]
        self.cmdCntHiRep2Hz     = [0x22, 0x36]
        self.cmdCntMedRep2Hz    = [0x22, 0x20]
        self.cmdCntLowRep2Hz    = [0x22, 0x2b]
        self.cmdCntHiRep4Hz     = [0x23, 0x34]
        self.cmdCntMedRep4Hz    = [0x23, 0x22]
        self.cmdCntLowRep4Hz    = [0x23, 0x29]
        self.cmdCntHiRep10Hz    = [0x27, 0x37]
        self.cmdCntMedRep10Hz   = [0x27, 0x21]
        self.cmdCntLowRep10Hz   = [0x27, 0x2a]
        
        # Turn on accelerated response time measurements
        self.cmdART             = [0x2b, 0x32]
        
        # Break command
        self.cmdBreak           = [0x30, 0x93]
        
        # Fetch readings
        self.cmdFetch           = [0xe0, 0x00]
        
        # Soft reset command
        self.cmdSoftReset       = [0x30, 0xa2]
        
        # Heater commands
        self.cmdHeaterEn        = [0x30, 0x6d]
        self.cmdHeaterDis       = [0x30, 0x66]
        
        # Status register
        self.cmdReadStatus      = [0xf3, 0x2d]
        self.cmdClearStatus     = [0x30, 0x41]
        
        # CRC constants
        self.__crcPolynomial      = 0x31
        self.__crcInitialization  = 0xff
        self.__crcFinalXor        = 0x00
        
        # Humidity and temp values.
        self.__humidRH = None
        self.__tempC = None
        
        # Try to initialize the i2c bus..
        try:
            # Create the bus address.
            self.__i2cBus = smbus.SMBus(i2cBusID)
        
        except Exception as e:
            # Pass the exception up the stack.
            raise e
    
    def __verifyCRC(self, dataBytes, dataCRC):
        """
        Verify CRC sum of incoming bytes against the CRC value provided by the sensor. Returns a boolean value indicating if the CRC sum is valid.
        """
        
        # Return True until we implement CRC verification.
        retVal = True
        
        # Learn how to do CRC computations here.
        
        return retVal

    @property
    def humidity(self):
        """
        Humidity in %RH
        """
        
        return self.__humidRH
    
    @property
    def temperature(self):
        """
        Temperature in degrees C.
        """
        
        return self.__tempC
    
    def readSensor(self):
        """
        Read temperature and humdity values from sensor.
        """
        
        try:
            # Get temperature and humidity bytes.
            thBytes = self.__i2cBus.read_i2c_block_data(self.__sensAddr, 0x00, 6)
        
        except:
            raise
        
        # Get temp value as integer.
        temp = int((thBytes[0] << 8) | thBytes[1])
        humid = int((thBytes[3] << 8) | thBytes[4])
        
        self.__tempC = round(-45.0 + (175.0 * temp / 65535.0), 2)
        self.__humidRH = round(100.0 * (humid / 65535.0), 2)
    
    def sendCmd16(self, command, wait = False):
        """
        Send a 16-byte command to the SHT31-D.
        """
        
        # Send the two command bytes?
        self.__i2cBus.write_i2c_block_data(self.__sensAddr, command[0], [command[1]])
        
        if wait:
            time.sleep(0.5)
        
        return
    
class sht31dWrapper(sht31d):
    
    @property    
    def sensorMeta(self):
        """
        Dictionary containg sensor metadata.
        """
        
        return {
            'sensor': "SHT31D",
            'type': "High accuracy temperature and humidity sensor",
            'tempMin': -40,
            'tempMax': 90,
            'humidMin': 0,
            'humidMax': 100,
            'tempUnit': 'c',
            'humidUnit': '%rh',
            'tempAcc': 0.3,
            'humidAcc': 2
        }
    
    def getTemperature(self):
        """
        Get temperature data from the sensor with metadata.
        """
        
        retVal = {'temp': self.__tempC, 'unit': 'c'}
        
        return retVal
    
    def getHumidity(self):
        """
        Get humidity data from the sensor with metadata.
        """
        
        retVal = {'humid': self.__humidRH, 'unit': '%RH'}
        
        return retVal
