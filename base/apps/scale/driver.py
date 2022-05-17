import re
import time
from os import listdir
from threading import Thread
from threading import Lock
import serial


@staticmethod
def parse_weight_systel(scale_connection, scale_config):
    try:
        scale_connection.write(scale_config.weight_command)
        time.sleep(0.01)
        serial_value = scale_connection.readline().decode("utf-8")
        print(serial_value)
        scale_connection.write(b"\x06")
        if re.search("^\x02", serial_value):
            scale_value = re.findall(r"^\x02([0-9]{6})\x03", serial_value)
            return int(scale_value[0])
        else:
            return 0
    except Exception as e:
        # _logger.error(e)
        return 0


@staticmethod
def parse_weight_temis_v2(scale_connection, scale_config):
    scale_connection.write(scale_config.weight_command)
    time.sleep(1)
    serial_value = scale_connection.readline()
    scale_value = serial_value.decode()
    try:
        return int(scale_value)
    except ValueError:
        return 0


@staticmethod
def parse_weight_temis_v1(scale_connection, scale_config):
    # Take the last value in a continuous series of send values
    scale_connection.flushInput()
    time.sleep(1)
    serial_value = scale_connection.readline()
    if not serial_value:
        return 0

    scale_value = serial_value.decode()
    try:
        return int(scale_value)
    except ValueError:
        return 0


class ScaleConfig:
    path = "/dev"
    baudrate = 9600
    bytesize = serial.EIGHTBITS
    stopbits = serial.STOPBITS_ONE
    parity = serial.PARITY_NONE
    timeout = 1
    write_timeout = 1
    weight_command = b"\x05"
    # parse_weight = parse_weight_temis_v2
    parse_weight = parse_weight_systel
    tare_command = b"t\n"


class Singleton(type):
    """
    Threading singleton implementation
    """

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]


class Scale(metaclass=Singleton):
    instance = None
    connection = None
    status = None
    device = None

    def __init__(self, config: ScaleConfig):
        self.status = {"status": "connecting", "messages": ""}
        self.config = config
        self.weight = 0

    def connect(self, device):
        self.device = device
        try:
            self.connection = serial.Serial(
                self.device,
                baudrate=self.config.baudrate,
                bytesize=self.config.bytesize,
                stopbits=self.config.stopbits,
                parity=self.config.parity,
                timeout=self.config.timeout,
                write_timeout=self.config.write_timeout,
            )
            self.status = {
                "status": "connected",
                "messages": f"Connected to {self.device}",
            }
            # returning path device if it's ok
            return self.device
        except Exception as e:
            print(e)
            self.status = {
                "status": "error",
                "messages": f"Failed to connect to {self.device}",
            }
            # returning None if there isn't connection
            return None

    def readValue(self):
        if self.connection:
            return self.weight
            # return self.config.parse_weight(self.connection, self.config)
        else:
            return 0

    def runTare(self):
        if self.connection:
            self.connection.write(self.config.tare_command)

    def getStatus(self):
        print(self.status)

    def readValueDaemon(self):
        if self.connection:
            self.weight = self.config.parse_weight(self.connection, self.config)
        else:
            return 0


import time
from serial.tools.list_ports import comports

# arduino_port = "/dev/cu.usbmodem1421101"
# SCALE =  ""
# import threading


class ScaleFinder(Thread):
    def __init__(self):
        Thread.__init__(self)
        # 1 second to sleep
        self.interval = 1
        self.daemon = True

    def run(self):
        scale_connected = None
        infinit = True
        while infinit:
            devices = [tuple(p)[0] for p in list(comports())]
            devices = list(filter(lambda x: re.search("usb", x), devices))
            # if arduino_port is None
            if not scale_connected:
                for device in devices:
                    config = ScaleConfig()
                    scale = Scale(config)
                    scale_connected = scale.connect(device)
                    if scale_connected:
                        print(f"{scale_connected} has been connected!")
                        break
                print("Without connection!")
            # if arduino_port is set and it isn't present in devices
            else:
                if scale_connected not in devices:
                    scale_connected = None
                    print("Arduino has been disconnected!")
            time.sleep(self.interval)


# def ScaleDaemonGetWeight():
#     while True:
#         config = ScaleConfig()
#         systel = Scale(config)
#         weight = systel.readValue()
#         print(f"Weight: {weight}")
#         time.sleep(1)
#
#
# def pedir():
#     while True:
#         config = ScaleConfig()
#         systel = Scale(config)
#         systel.readValueDaemon()
#         time.sleep(0.5)
#
#
# def pedir2():
#     while True:
#         config = ScaleConfig()
#         systel = Scale(config)
#         weight = systel.readValue()
#         print(f"Weight: {weight}")
#         time.sleep(1)
#
#
# sf = ScaleFinder()
# b = Thread(target=pedir, daemon=True)
# c = Thread(target=pedir2, daemon=True)
# sf.start()
# b.start()
# c.start()
# sf.join()
# b.join()
# c.join()
