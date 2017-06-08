from .alien_rfid import _AlienReader
import socket
import time


class AlienReaderNetwork(_AlienReader):
    """
    Object to interface with Alien RFID reader over network connection.

    Designed as a contextmanager, to be used in a with statement.

    with AlienReader(*args) as ar:
        ar.send()
        ...
    """

    def __init__(self, ipaddress='localhost', port=23, username='alien', password='password',
                 rf_level=200, timeout=2):
        super().__init__(rf_level)
        self.ipaddress = ipaddress
        self.username = username
        self.password = password
        self.port = port
        self.sock = None

    def __del__(self):
        super().__del__()
        if self.sock:
            self.sock = None

    def _login(self):
        try:
            result = self.send_receive(self.username)
            result = self.send_receive(self.password)

            if 'Error:' in result:
                errmsg = result.split('Error:')[1]
                self.close(False)
                self._connected = False
                raise Exception("Trouble logging in: " + errmsg)

            result = self.send_receive('RFLevel={}'.format(self.rf_level))

        except Exception as e:
            raise e

    def _connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.ipaddress, self.port))
            self._connected = True
            s = self.receive()
            if "later." in s:
                message = "Trouble Connecting to #{0}. (Someone else is talking to the reader.)".format(self.ipaddress)
                raise Exception(message)
            return True
        except RuntimeError as e:
            raise e

    def _byte_read(self):
        return self.sock.recv(1)

    def _send(self, msg_bytes):
        self.sock.send(msg_bytes)

    def close(self, send_quit=True):
        if self.sock:
            try:
                self.sock.send(b"quit\r\n")
                time.sleep(0.1)
            except:
                pass
            self.sock.close()
