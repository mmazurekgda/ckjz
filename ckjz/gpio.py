import os
from threading import Lock
import time

_export_lock = Lock()
_open_pins = {}

GPIO_ROOT = "/sys/class/gpio"
GPIO_EXPORT = os.path.join(GPIO_ROOT, "export")
GPIO_UNEXPORT = os.path.join(GPIO_ROOT, "unexport")
FMODE = "w+"  # w+ overwrites and truncates existing files
IN, OUT = "in", "out"
LOW, HIGH = 0, 1


class GPIOPin(object):
    def __init__(self, pin, direction=None, initial=LOW, active_low=None):
        if ready_pin := GPIOPin.configured(pin):
            return ready_pin

        self.value = None
        self.pin = int(pin)
        self.root = os.path.join(GPIO_ROOT, "gpio{0}".format(self.pin))

        if not os.path.exists(self.root):
            with _export_lock:
                with open(GPIO_EXPORT, "w") as f:
                    f.write(str(self.pin))
                    f.flush()

        time.sleep(0.1)  # Give udev time to set permissions
        self.value = open(os.path.join(self.root, "value"), "wb+", buffering=0)

        self.setup(direction, initial, active_low)

        _open_pins[self.pin] = self

    def setup(self, direction=None, initial=LOW, active_low=None):
        if direction is not None:
            self.set_direction(direction)

        if active_low is not None:
            self.set_active_low(active_low)

        if direction == OUT:
            self.write(initial)

    @staticmethod
    def configured(pin):
        try:
            pin = int(pin)
        except (TypeError, ValueError):
            raise ValueError("pin must be an int")

        return _open_pins.get(pin)

    def set_direction(self, mode):
        """Set the direction of pin

        Args:
            mode (str): use either gpio.OUT or gpio.IN
        """
        if mode not in (IN, OUT, LOW, HIGH):
            raise ValueError("Unsupported pin mode {}".format(mode))

        with open(os.path.join(self.root, "direction"), FMODE) as f:
            f.write(str(mode))
            f.flush()

    def set_active_low(self, active_low):
        """Set the polarity of pin

        Args:
            mode (bool): True = active low / False = active high
        """
        if not isinstance(active_low, bool):
            raise ValueError("active_low must be True or False")

        with open(os.path.join(self.root, "active_low"), FMODE) as f:
            f.write("1" if active_low else "0")
            f.flush()

    def read(self):
        """Read pin value

        Returns:
            int: gpio.HIGH or gpio.LOW
        """
        self.value.seek(0)
        value = self.value.read()
        try:
            # Python > 3 - bytes
            # Subtracting 48 converts an ASCII "0" or "1" to an int
            # ord("0") == 48
            return value[0] - 48
        except TypeError:
            # Python 2.x - str
            return int(value)
