from .alien_rfid import _AlienReader
import socket
import time


class TesterIO(object):
    """

**************************************************************
GENERAL COMMANDS
**************************************************************
  Help:
     Display descriptive help text.
  Info:
     Display current settings.
  !:
     Repeat last command.
  Save:
     Save current settings to permanent storage.
  Quit:
     Quit the current connection (Telnet only).
  Function:
     Get|Set the operating mode.
  ReaderName:
     Get|Set the user-defined name for the reader.
  ReaderType:
     Get a brief description of the reader.
  ReaderVersion:
     Get the release number for the reader firmware.
  DSPVersion:
     Get the version of the reader's DSP firmware.
  ReaderNumber:
     Get|Set the numerical identifier for this reader.
  BaudRate:
     Get|Set the serial interface baud rate.
  Uptime:
     Get the elapsed time since the reader was booted.
  Username:
     Get|Set the username (default: "alien").
  Password:
     Get|Set the password (default: "password").
  MaxAntenna:
     Get the index of the maximum addressable antenna.
  AntennaSequence:
     Get|Set antenna sequence.
  RFAttenuation:
     Get|Set the RF attenuation from max power.
  RFLevel:
     Get|Set the RF power level.
  RFModulation:
     Get|Set the RF modulation scheme.
  FactorySettings:
     Return all settings to their factory defaults.
  Reboot:
     Reboot the reader.
  Service:
     View status, start/stop, and enable autostarting of auxiliary services.
  MyData:
     Get|Set the user-defined data string.
**************************************************************
NETWORK COMMANDS
**************************************************************
  MACAddress:
     Get this reader's unique network interface identifier.
  DHCP:
     Get|Set whether to dynamically configure network settings.
  DHCPTimeout:
     Get|Set the delay, in seconds, before giving up on the DHCP server.
  IPAddress:
     Get|Set this reader's IP Address.
  Hostname:
     Get|Set this reader's network Hostname.
  UpgradeAddress:
     Get|Set the URL of Reader Upgrades.
  NetworkUpgrade:
     Get|Set whether to attempt to fetch new firmware on next boot.
  UpgradeNow:
     Triggers reader firmware update.
  Gateway:
     Get|Set the address of the Gateway server on the LAN.
  Netmask:
     Get|Set this reader's network subnet mask.
  DNS:
     Get|Set the address of the DNS server on the LAN.
  NetworkTimeout:
     Get|Set the delay (in secs) before closing an idle network connection.
  CommandPort:
     Get|Set the port used to connect to the reader.
  CommandPortLocal:
     Get|Set the port used to connect to the reader locally (for on-reader programming).
  HeartbeatAddress:
     Get|Set the destination address for Heartbeat messages.
  HeartbeatPort:
     Get|Set the destination port for Heartbeat messages.
  HeartbeatTime:
     Get|Set the delay (in secs) between Heartbeat messages.
  HeartbeatCount:
     Get|Set the total number of heartbeat messages to send.
  HeartbeatNow:
     Manually trigger a Heartbeat.
  WWWPort:
     Get|Set the web server's port number (0 turns off web server).
  Ping:
     Ping a network address.
  DebugHost:
     Enables logging of all commands that are issued over TCP or Serial.
  HostLog:
     Dumps the log of host activity.
  AcceptConnections:
     Specifies whether only secure/local TCP connections are allowed.
**************************************************************
TIME COMMANDS
**************************************************************
  TimeServer:
     Get|Set the IP address of a network time server.
  Time:
     Get|Set current local time (YYYY/MM/DD hh:mm:ss).
  TimeZone:
     Get|Set the local timezone (+/- hours from GMT).
**************************************************************
MACRO COMMANDS
**************************************************************
  MacroList:
     Lists the names of all of the installed macros.
  MacroView:
     Displays the contents of a named macro.
  MacroDel:
     Deletes a named macro.
  MacroDelAll:
     Deletes all macros.
  MacroRun:
     Executes the named macro.
  MacroStartRec:
     Begins recording a named macro.
  MacroStopRec:
     Stops the macro currently being recorded.
**************************************************************
TAGLIST COMMANDS
**************************************************************
  TagList:
     Get the current TagList held in memory.
  t:
     Get the current TagList held in memory.
  to:
     Get the current TagList held in memory with G2Ops, regardless of AcqG2OpsMode.
  TagListFormat:
     Get|Set the format for the TagList.
  TagListCustomFormat:
     Get|Set the custom TagList format.
  TagDataFormatGroupSize:
     Get|Set the data group size in bytes when formatting a TagList.
  TagListMillis:
     Get|Set the flag enabling millisecond time resolution in TagLists.
  PersistTime:
     Get|Set the time (in secs) that a tag remains on the TagList.
  TagListAntennaCombine:
     Get|Set whether to combine tag reads from many antennas into one entry.
  Clear:
     Clears the TagList or IOList (given by command argument)
  TagStreamMode:
     Get|Set the TagStreamMode-active flag.
  TagStreamAddress:
     Get|Set the destination address for streamed Tag data.
  TagStreamFormat:
     Get|Set the format for the TagStream.
  TagStreamCustomFormat:
     Get|Set the custom TagStream format.
  TagStreamKeepAliveTime:
     Get|Set the time (in seconds) to hold the TagStream socket open.
  TagStreamCountFilter:
     Get|Set a tag's minimum (and optional maximum) read count before streaming it.
  StreamHeader:
     Get|Set the StreamHeader-active flag.
**************************************************************
ACQUIRE COMMANDS
**************************************************************
  AcquireMode:
     Get|Set the method used to acquire tags.
  TagType:
     Get|Set the bitmap specifying which tag protocols to use.
  AcqG2Cycles:
     Get|Set outer loops on Gen 2 reads.
  AcqG2Count:
     Get|Set inner loops on Gen 2 reads.
  AcqG2Q:
     Get|Set Q parameter for Gen 2 reads.
  AcqG2QMax:
     Get|Set the maximum value of the Q parameter for Gen 2 reads.
  AcqG2Select:
     Get|Set the number of times B->A select is issued at the start of a Gen2 inventory cycle.
  AcqG2Session:
     Get|Set Gen2 session used in inventory.
  AcqG2Mask:
     Get|Set C1G2 tag mask. Format: Bank(dec), BitPtr(dec), BitLen(dec), XX XX... (hex)
  AcqG2MaskAction:
     Get|Set whether the mask selects the tags that match it (include) or do not match it (exclude).
  AcqG2AccessPwd:
     Get|Set the Access Pwd used to gain write access to access-protected C1G2 tags.
  AcqG2Target:
     Get|Set the C1G2 inventory target
  RSSIFilter:
     Get|Set the range of tag RSSI measurements (min, max) to filter.
**************************************************************
I/O COMMANDS
**************************************************************
  ExternalInput:
     Get the current state of the digital input pins.
  ExternalOutput:
     Get|Set the current state of the digital output pins.
  InvertExternalInput:
     Get|Set whether to invert the reported state of the digital input pins.
  InvertExternalOutput:
     Get|Set whether to invert the reported and applied state of the digital output pins.
  InitExternalOutput:
     Get|Set the state of the digital output pins on startup.
  IOList:
     Get the current IOList held in memory.
  IOType:
     Get|Set which IOs to track in the IOList, and how they are reported.
  IOListFormat:
     Get|Set the format for the IOList.
  IOListCustomFormat:
     Get|Set the custom IOList format.
  IOStreamMode:
     Get|Set the IOStreamMode-active flag.
  IOStreamAddress:
     Get|Set the destination address for streamed IO data.
  IOStreamKeepAliveTime:
     Get|Set the time (in seconds) to hold the IOStream socket open.
  IOStreamFormat:
     Get|Set the format for the IOStream.
  IOStreamCustomFormat:
     Get|Set the custom IOStream format.
  IOPersistTime:
     Get|Set the time (in secs) that a tag remains on the IOList.
  BlinkLED:
     Blinks LEDs. Format: <bit-state-1> <bit-state-2> <duration> <count>
**************************************************************
AUTOMODE COMMANDS
**************************************************************
  AutoMode:
     Get|Set the AutoMode-active flag.
  AutoAction:
     Get|Set the action to perform in AutoMode.
  AutoWaitOutput:
     Get|Set the output state while waiting for a start trigger.
  AutoStartTrigger:
     Get|Set the I/O edges to start AutoMode.
  AutoStartPause:
     Get|Set the delay (in msec) after a trigger before starting AutoAction.
  AutoWorkOutput:
     Get|Set the output state while performing the AutoMode action.
  AutoStopTrigger:
     Get|Set the I/O edges to stop AutoMode.
  AutoStopTimer:
     Get|Set maximum time (in msec) to spend performing AutoAction.
  AutoStopPause:
     Get|Set the delay (in msec) after a trigger before stopping AutoAction.
  AutoTrueOutput:
     Get|Set the output state when AutoMode evaluates to TRUE.
  AutoFalseOutput:
     Get|Set the output state when AutoMode evaluates to FALSE.
  AutoErrorOutput:
     Get|Set the error-dependent output state while performing the AutoMode action.
  AutoProgError:
     Get|Set the error value reported when programming operation fails in AutoMode.
  AutoTruePause:
     Get|Set time (in msec) to pause after AutoMode evaluates to TRUE.
  AutoFalsePause:
     Get|Set time (in msec) to pause after AutoMode evaluates to FALSE.
  AutoModeTriggerNow:
     Manually trigger AutoMode.
  AutoModeReset:
     Turn OFF AutoMode and reset AutoMode parameters to default values.
**************************************************************
NOTIFY COMMANDS
**************************************************************
  NotifyMode:
     Get|Set the NotifyMode-active flag.
  NotifyAddress:
     Get|Set the destination addresses for notification messages.
  NotifyFormat:
     Get|Set the format used for notification messages.
  NotifyHeader:
     Get|Set whether to include headers and footers in notifications.
  NotifyTime:
     Get|Set the period at which timed notifications are sent.
  NotifyTrigger:
     Get|Set the trigger for issuing notification messages.
  NotifyKeepAliveTime:
     Get|Set the time (in seconds) to hold the notify socket open.
  NotifyRetryCount:
     Get|Set the number of times to retry a failed TCP notification.
  NotifyRetryPause:
     Get|Set the time (in seconds) between TCP notification retries.
  NotifyQueueLimit:
     Get|Set the number of failed TCP notifications to queue for later delivery.
  NotifyNow:
     Manually trigger NotifyMode.
  NotifyInclude:
     Get|Set fields to include in the notifications messages.
  MailServer:
     Get|Set the address of the server used to send e-mail notifications.
  MailFrom:
     Get|Set the reported sender of e-mail notifications.
**************************************************************
PROGRAM COMMANDS
**************************************************************
  ProgProtocol:
     Get|Set the protocol for programming a tag.
  ProgAntenna:
     Get|Set the antenna on which to program tags.
  ProgramEPC:
     Program tag's EPC memory bank.
  ProgramUser:
     Program tag's user memory bank.
  ProgramKillPwd:
     Writes the Kill Pwd.
  ProgramAccessPwd:
     Write the Access Pwd.
  ProgEPCData:
     Get|Set the default EPC used to program tags.
  ProgEPCDataInc:
     Get|Set whether to increment ProgEPCData when programming.
  ProgEPCDataIncCount:
     Get|Set the number of remaining increments of ProgEPCData.
  ProgG2KillPwd:
     Get|Set the Kill Pwd used to kill C1G2 tags.
  ProgG2AccessPwd:
     Get|Set the Access Pwd data used by Lock with no parameters, or ProgramAndLock with a non-permanent lock type.
  ProgUserData:
     Get|Set the default User data used to program tags.
  ProgUserDataInc:
     Get|Set whether to increment ProgUserData when programming.
  ProgUserDataIncCount:
     Get|Set the number of remaining increments of ProgUserData.
  ProgG2LockType:
     Get|Set the G2 lock type to be used when programming.
  ProgBlockSize:
     Get|Set the size in words of the data block for programming C1G2 tags in block mode.
  ProgBlockAlign:
     Get|Set whether the data block pointer must be aligned on the blocksize boundary.
  LockEPC:
     Lock a tag's EPC memory bank using the supplied or currently set Access Pwd.
  LockUser:
     Lock a tag's User memory bank using the supplied or currently set Access Pwd.
  LockKillPwd:
     Lock a tag's Kill Pwd using the supplied or currently set Access Pwd.
  LockAccessPwd:
     Lock a tag's Access Pwd using the supplied or currently set Access Pwd.
  UnlockEPC:
     Unlock a tag's EPC memory bank using the supplied or currently set Access Pwd.
  UnlockUser:
     Unlock a tag's User memory bank using the supplied or currently set Access Pwd.
  UnlockKillPwd:
     Unlock a tag's Kill Pwd using the supplied or currently set Access Pwd.
  UnlockAccessPwd:
     Unlock a tag's Access Pwd using the supplied or currently set Access Pwd.
  Erase:
     Erase a tag in the field.
  Kill:
     Kill a tag in the field with the supplied ID and passcode.
  ProgAttempts:
     Get|Set the number of attempts to program a tag.
  ProgSuccessFormat:
     Get|Set the flag determining the format of successful programming responses.
  ProgSingulate:
     Get|Set whether to verify that the tag is singulated before programming.
  G2Read:
     C1G2 protocol low-level read. Format: Bank(dec), WrdPtr(dec), WordCount(dec)
  G2Write:
     C1G2 protocol low-level write. Format: Bank(dec), WrdPtr(dec), XX XX... (even number of hex values)
  G2Erase:
     C1G2 protocol erase command. Format: Bank(dec), WrdPtr(dec), WordCount(dec)
  TagInfo:
     Fetch information about a tag.
  ProgDataUnit:
     Get|Set the data unit size to use when programming C1G2 tags.
  ProgG2NSI:
     Get|Set the value of NSI bits to be inserted into the PC Word when programming a tag's ID
    """


class AlienReaderTester(_AlienReader):
    """
    Object to interface with Alien RFID reader over network connection.

    Designed as a contextmanager, to be used in a with statement.

    with AlienReader(*args) as ar:
        ar.send()
        ...
    """

    def __init__(self, fake_interface, rf_level=200, timeout=2):
        super().__init__(rf_level, timeout)
        self.io = fake_interface

    def __del__(self):
        super().__del__()
        if self.io:
            self.io = None

    def _connect(self):
        try:
            s = self.receive()
            if b'Alien>' not in s:
                raise Exception('Did not received expected prompt after connecting.')
            return True
        except RuntimeError as e:
            raise e

    def _byte_read(self):
        return self.io.read()

    def _send(self, msg_bytes):
        self.io.write(msg_bytes)

    def close(self, send_quit=True):
        if self.io:
            try:
                self.io.send(b"quit\r\n")
                time.sleep(0.1)
            except:
                pass
            self.io.close()
