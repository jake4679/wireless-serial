from django.shortcuts import render
from django.forms.models import modelformset_factory

from serial_configuration.models import SerialPort

def port_configuration(request):
    SerialPortFormSet = modelformset_factory(
        SerialPort,
        fields=('device_file', 'enable_tcp', 'port', 'block_mode', 'lock_file', 'baud', 'raw_mode', 'echo_mode', 'enable_file'),
        exclude=('pk',),
        extra=0)

    return render(request, 'serial_configuration/port_configuration.html', { 'serial_ports' : SerialPortFormSet})
