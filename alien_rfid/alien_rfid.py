from binascii import hexlify


class NotConnectedException(Exception):
    pass


class _AlienReader(object):
    """
    This is the base device for common functionality of Alien RFID Reader, regardless of connection type.

    Some methods raise NotImplementedError, as they need to be defined in the lower level interface, specific
    to connection type.

    Try to implement all methods that can be in here, so there isn't duplication.  Only break out when required.
    """

    def __init__(self, rf_level=200, timeout=2):
        self.timeout = timeout
        if not 170 <= rf_level <= 290:
            raise ValueError('rf_level must be between 170 and 290.')
        self.rf_level = rf_level
        self._connected = False

    @property
    def connected(self):
        return self._connected

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.__del__()

    def __del__(self):
        if self.connected:
            self.close()

    def _connect(self):
        raise NotImplementedError()

    def receive(self):
        """
        Receive Data from RFID Reader

        :return: raw text data from reader (hex if memory read)
        """
        reopened = False
        data = None
        while True:
            try:
                data = self._receive()
                if 'Connection Timeout' in data:
                    raise Exception('Need to reconnect.')
                break
            except Exception as e:
                if reopened:
                    raise e
                self.close()
                self.open()
                reopened = True
        return data

    def _byte_read(self):
        raise NotImplementedError()

    def _receive(self):
        s = []
        cur_char = self._byte_read()
        while cur_char != b'\x00':
            s.append(cur_char)
            cur_char = self._byte_read()
        packet = b''.join(s)
        packet = packet.strip()

        if b'Goodbye!' in packet:
            # Response to Quit, so socket will be automatically closed
            self.close(False)
        return packet.decode('UTF-8')

    def _send(self, msg_bytes):
        """
        Connection Specific Send method.
        """
        raise NotImplementedError

    def send(self, msg=""):
        """
        Send method that must be redefined in the connection specific object
        :param msg: message to send
        :return: Exception, as this isn't defined.
        """
        self._send(bytes("{0}\r\n".format(msg), 'UTF-8'))

    def send_receive(self, msg=""):
        """
        Perform a send immediately followed by a receive and return received data
        :param msg: Message to send
        :return: raw text data from reader (hex if memory read)
        """
        reopened = False
        data = None
        while True:
            try:
                data = self._send_receive(msg)
                if 'Connection Timeout' in data:
                    raise Exception('Need to reconnect.')
                break
            except Exception as e:
                if reopened:
                    raise e
                self.close()
                self.open()
                reopened = True
        return data

    def _send_receive(self, msg=""):
        self.send(msg)
        # Calling internal _receive to bypass error handling in receive
        # This same error handling is in send_receive and we need to
        # resend if error required relogin, as send is needed to be
        # resent.
        return self._receive()

    def _login(self):
        """
        Login only required for network based.
        """
        pass

    def open(self):
        """
        Open connection to reader.

        :return: None
        """
        if self._connect():
            self._login()
            _ = self.send_receive('RFLevel={}'.format(self.rf_level))

    def close(self, send_quit=True):
        """
        Close connection to reader and shut down interfaces.

        :param send_quit: Default True, sends the quit command to cleanly shutdown on reader side, before disconnecting.
        :return: None
        """
        raise NotImplementedError()

    def read_tags(self, retry_count=2):
        """
        Read default RFID tag

        :param retry_count: attempts before aborting after failure
        :return: list of tags
        """
        return_text = ''
        for i in range(retry_count + 1):
            return_text = self.send_receive('t')
            if '(No Tags)' not in return_text:
                break
        tags = []
        for line in return_text.split('\n'):
            if line[:4] == 'Tag:':
                tags.append(bytearray.fromhex(line[4:33].replace(' ', '')))
        return tags

    def g2_read(self, bank_number, start_word, word_count, retry_count=2):
        """
        Read memory with low lever G2Read

        :param bank_number: 0-3
        :param start_word: position of first word to read (0-2097151)
        :param word_len: number of words to read (0-32)
        :param retry_count: attemps before aborting after failure
        :return: Hexadecimal as str
        """
        if not 0 <= bank_number <= 3:
            raise ValueError('Valid bank_number is 0-3.')
        if not 0 <= word_count <= 32:
            raise ValueError('Valid word_count is 0-32 (unless less supported by bank.)')
        for i in range(retry_count + 1):
            values = self.send_receive('G2Read={},{},{}'.format(bank_number, start_word, word_count))
            if 'Read error.' in values:
                raise Exception(values)
            if 'G2Read' in values:
                values = values.strip().replace(' ', '')
                values = values.rsplit('G2Read=')[-1]
                return bytearray.fromhex(values)
        else:
            raise Exception('Error getting G2Read({},{},{})'.format(bank_number, start_word, word_count))

    def g2_write(self, bank_number, start_word, byte_data):
        """
        Write to memory with low level G2Write

        :param bank_number: 0-3
        :param start_word: position of first word to write (0-2097151)
        :param byte_data: even number of bytes
        :return: None
        """
        assert len(byte_data) % 2 == 0, 'byte_data must be an even number of bytes, due to word boundaries of data.'
        # Convert to uppercase and space delimited hex string expected
        hexed = hexlify(byte_data).upper().decode('UTF-8')
        spaced_hexed = ' '.join([hexed[i:i + 2] for i in range(0, len(hexed), 2)])
        result = self.send_receive('G2Write={},{},{}'.format(bank_number, start_word, spaced_hexed))
        if 'Success!' not in result:
            raise Exception("'Success!' not received: {}".format(result))
