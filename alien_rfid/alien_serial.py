from .alien_rfid import _AlienReader
import time
import serial


class AlienReaderSerial(_AlienReader):
    """
    Object to interface with Alien RFID reader over serial connection.

    Designed as a contextmanager, to be used in a with statement.

    with AlienReader(*args) as ar:
        ar.send()
        ...
    """

    def __init__(self, serial_port, baud=115200, rf_level=200, timeout=2):
        super().__init__(rf_level, timeout)
        self._serial_port = serial_port
        # No flow control, but default is off.
        self.ser = serial.Serial(port=serial_port,
                                 baudrate=baud,
                                 parity=serial.PARITY_NONE,
                                 stopbits=1,
                                 timeout=timeout)

    def __del__(self):
        super().__del__()
        if self.ser:
            self.ser.close()
            self.ser = None

    @property
    def connected(self):
        try:
            return self.ser.is_open
        except:
            return False

    def _connect(self):
        try:
            if not self.connected:
                self.ser.open()
                s = self.send_receive('')
            if b'Alien>' not in s:
                raise Exception('Did not received expected prompt after connecting.')
            return True
        except RuntimeError as e:
            raise e

    def _byte_read(self):
        return self.ser.read()

    def _send(self, msg_bytes):
        self.ser.write(msg_bytes)

    def close(self, send_quit=True):
        if self.ser:
            try:
                self.ser.write(b"quit\r\n")
                time.sleep(0.1)
            except:
                pass
            self.ser.close()

