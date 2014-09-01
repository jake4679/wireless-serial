import os
from django.db import models

# Create your models here.

class SerialPort(models.Model):
    # Options related to network connectivity for port

    # True if network connectivity for serial port is enabled, default is True
    enable_tcp = models.BooleanField(default=True)
    # Default port number, default is 54321, see socat documentation for more info 
    port = models.IntegerField(default=54321)

    # Options related to the underlying hardware connection

    # Filesystem name of device, see socat documentation for more info
    device_file = models.CharField(unique=True, max_length=255)
    # Blocking mode of the port, default is False, see socat documentation for more info
    block_mode = models.BooleanField(default=False)
    # If True a lockfile will be created to lock the port, default uses /var/run/<serial device file>.lock, see socat documentation for more info
    lock_file = models.BooleanField(default=True)
    # Speed of the device connected, default is 115200, see socat documentation for more info
    baud = models.IntegerField(default=115200)
    # If True raw mode will be used, default is True, see socat documentation for more info
    raw_mode = models.BooleanField(default=True)
    # If True echo is turned on, default is False, see socat documentation for more info
    echo_mode = models.BooleanField(default=False)
    # If true the hardware device is present, False otherwise.  Updated by the system resident daemon not by the user
    present = models.BooleanField(default=False)

    # Options related to local file logging

    # True if local file logging is enabled, default is False
    enable_file = models.BooleanField(default=False)

    # Options related to the running process

    # Process identifier for the serial port monitoring daemon
    pid = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.device_file

    def device(self):
        return os.path.basename(self.device_file)

    def socat_options(self):
        # Sample options string below
        #     -d -d -ly tcp4-listen:54321,reuseaddr,fork file:/dev/ttyUSB0,nonblock,waitlock=/var/run/ttyUSB0.lock,b115200,raw,echo=0 &
        str = "-d -d -ly "
        if self.enable_tcp:
            str += 'tcp4-listen:%s,reuseaddr,fork' % self.port
        str += ' file:%s' % self.device_file
        if self.block_mode:
            str += ',block'
        else:
            str += ',nonblock'
        if self.lock_file:
            str += ',waitlock=/var/run/%s.lock' % self.device()
        str += ',b%s' % self.baud
        if self.raw_mode:
            str += ',raw'
        if self.echo_mode:
            str += ',echo=1'
        else:
            str += ',echo=0'
        return str
