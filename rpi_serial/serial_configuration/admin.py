from django.contrib import admin
from serial_configuration.models import SerialPort

class SerialPortAdmin(admin.ModelAdmin):
    readonly_fields = ('device_file',)
    fieldsets = [
        ('Serial Options', {'fields' : ['device_file', 'block_mode', 'lock_file', 'baud', 'raw_mode', 'echo_mode']}),
        ('TCP Logging',    {'fields' : ['enable_tcp', 'port']}),
        ('File Logging',   {'fields' : ['enable_file']}),
      ]

# Register your models here.
admin.site.register(SerialPort, SerialPortAdmin)
