import re
import time
from os import listdir
from threading import Thread
from threading import Lock
import serial
import logging


logger = logging.getLogger(__name__)


@staticmethod
def parse_weight_systel(scale_connection, scale_config):
    try:
        scale_connection.write(scale_config.weight_command)
        time.sleep(0.01)
        serial_value = scale_connection.readline().decode("utf-8")
        # print(serial_value)
        scale_connection.write(b"\x06")
        if re.search("^\x02", serial_value):
            scale_value = re.findall(r"^\x02([0-9]{6})\x03", serial_value)
            return int(scale_value[0])
        else:
            return 0
    except Exception as e:
        logger.critical(f"Error: {e}")
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

# TODO: Carry that bunch of params to ENV file
class ScaleConfig:
    name = "Systel"
    path = "/dev"
    baudrate = 9600
    bytesize = serial.EIGHTBITS
    stopbits = serial.STOPBITS_ONE
    parity = serial.PARITY_NONE
    timeout = 1
    write_timeout = 1
    weight_command = b"\x05"
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
    """
    Scale object +connection


    Attributes
    ----------
    connection : object
        Scales's serial connection

    Methods
    -------
    connect(device)
        Connect with a specific device
    readValue()
        Reading values of scale
    runTare()
        Sending to scale a command tare

    """

    connection = None

    def __init__(self, config: ScaleConfig):
        self.config = config
        self.weight = 0

    def connect(self, device):
        try:
            self.connection = serial.Serial(
                device,
                baudrate=self.config.baudrate,
                bytesize=self.config.bytesize,
                stopbits=self.config.stopbits,
                parity=self.config.parity,
                timeout=self.config.timeout,
                write_timeout=self.config.write_timeout,
            )
            # returning path device if it's ok
            return device
        except Exception as e:
            raise Exception(f"Failed to connect to {device} -> {e}")

    def readValue(self):
        if self.connection:
            return self.weight
        else:
            return 0

    def runTare(self):
        if self.connection:
            self.connection.write(self.config.tare_command)

    def readValueDaemon(self):
        if self.connection:
            self.weight = self.config.parse_weight(self.connection, self.config)
        else:
            return 0


import time
from serial.tools.list_ports import comports


class ScaleFinder(Thread):
    """
    Scan Plug/Unplug specific a path /dev/serial/by-path where posbox mount the scale device


    Attributes
    ----------
    status : object
        Status of monitoring scale

    Methods
    -------
    get_status()
        This method is called by hw_proxy to show in status page
    set_status()
        Set the status in correct way
    run()
        Sending to scale a command tare
    """

    status = None

    def __init__(self):
        Thread.__init__(self)
        # retry each 10 seconds
        self.interval = 10
        self.daemon = True
        self.set_status("connecting")

    def get_status(self):
        return self.status

    def set_status(self, status, message=None):
        self.status = {"status": status, "messages": [message]}

    def run(self):
        scale_connected = None
        infinit = True
        self.set_status("connecting", "Waiting")
        while infinit:
            try:
                devices = [tuple(p)[0] for p in list(comports())]
                devices = list(filter(lambda x: re.search("usb", x), devices))
                # if serial_scale_port is None
                if not scale_connected:
                    for device in devices:
                        config = ScaleConfig()
                        scale = Scale(config)
                        scale_connected = scale.connect(device)
                        if scale_connected:
                            self.set_status(
                                "connected", f"Connected to {device} with {config.name}"
                            )
                            logger.info(f"Connected to {device} with {config.name}")
                            break
                    # logger.info("Without connection!")
                # if serial_scale_port is set and it isn't present in devices
                else:
                    if scale_connected not in devices:
                        scale_connected = None
                        logger.info("Scale device has been disconnected!")
            except Exception as e:
                scale_connected = None
                logger.error(f"Error: {e}")
                self.set_status("error", f"{e}")
            time.sleep(self.interval)
