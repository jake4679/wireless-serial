#!/usr/bin/env python

import os
import os.path
import sys
import logging
import argparse
import logging
import signal
import subprocess32

verbosity_to_logging = {
    'DEBUG'    : logging.DEBUG,
    'INFO'     : logging.INFO,
    'WARN'     : logging.WARNING,
    'ERROR'    : logging.ERROR,
    'CRITICAL' : logging.CRITICAL,
  }

class LogLevelArgumentAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=1, **kwargs):
        if nargs != 1:
            raise ValueError("nargs expected 1")
        super(LogLevelArgumentAction, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            verbosity_to_logging[values]
        except:
            raise ValueError('Invalid log level specified %s' % values)
        setattr(namespace, self.dest, values)

def sigchld_handler(signum, frame):
    # @todo Need to catch SIGHLD for exiting daemons
    pass

def sigquit_handler(signum, frame):
    # @todo Need to catch SIGQUIT to clean up lock file and exit cleanly
    pass

def sighup_handler(signum, frame):
    # @todo Need to catch SIGHUP to refresh configurations
    pass

def launch_socat(port):
    #process = subprocess32.Popen(['socat', 
    print port.socat_options()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpi_serial.settings")

    from serial_configuration.models import SerialPort
    from rpi_serial.settings import SERIAL_DAEMON_LOCK_FILE

    parser = argparse.ArgumentParser(description='Daemon process for wireless serial debugger.')
    parser.add_argument('--clean', action='store_true', help='Clean existing lockfile.  WARNING: Existing process may still be running.')
    parser.add_argument('-d', '--daemon', action='store_true', help='Clean existing lockfile.  WARNING: Existing process may still be running.')
    # @todo Fix error message to be correct
    parser.add_argument('-v', '--verbose', nargs=1, action=LogLevelArgumentAction, metavar='LEVEL', help='Set the logging level. Accepts DEBUG, INFO, WARN, ERROR and CRITICAL.')

    try:
        args = parser.parse_args()
    except:
        parser.error('Invalid logging level specified')

    level = logging.WARNING
    if args.verbose:
        level = verbosity_to_logging[args.verbose]
    logging.basicConfig(level=level)

    if args.clean:
        try:
          os.remove(SERIAL_DAEMON_LOCK_FILE)
        except:
            logging.critical('Unable to remove lock file %s' % SERIAL_DAEMON_LOCK_FILE)
            exit()

    if os.path.isfile(SERIAL_DAEMON_LOCK_FILE):
        logging.critical('Lock file exists.  Verify no instances running then use the --clean option')
        exit()

    try:
      # @todo Update mask to ensure only user creating file has access
      open(SERIAL_DAEMON_LOCK_FILE, 'w')
    except:
      logging.critical('Unable to create lock file %s' % SERIAL_DAEMON_LOCK_FILE)
      exit()

    try:
        # @todo Defer sigchld registration until child processes are running
        signal.signal(signal.SIGCHLD, sigchld_handler)
        signal.signal(signal.SIGQUIT, sigquit_handler)
        signal.signal(signal.SIGHUP,  sighup_handler)
        
        # Retrieve list of configured serial ports
        for port in SerialPort.objects.all():
            if os.path.isfile(port.device_file):
                port.present = True
                logging.info('Device file %s present' % port.device_file)
            else:
                port.present = True
                logging.info('Device file %s not present' % port.device_file)
            #port.pid = launch_socat(port)
            launch_socat(port)
            port.save()
    
        # Scan the device directory configured in rpi_serial.settings file for a ttyS or ttyAMA* device file and create a new model using defaults
    except Exception as e:
      print e

    os.remove(SERIAL_DAEMON_LOCK_FILE)
