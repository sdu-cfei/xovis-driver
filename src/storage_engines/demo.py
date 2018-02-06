import json

description = 'Demonstrate storage engine interface'

arguments = [
    {
        'name':        'FIRST_ARG',
        'description': 'Not really used',
        'example':     '1',
    },
    {
        'name':        'SECOND_ARG',
        'description': 'Also not really used',
        'example':     '2',
    },
]

async def init (cfg, args, l):
    pretty_cfg = json.dumps(cfg, sort_keys=True, indent=4, separators=(',', ': '))
    
    print('CALL: init')
    print(' - cfg: the program-wide configuration as read from JSON')
    for line in pretty_cfg.split('\n'):
        print('   | %s' % line)
    print(' - args: the storage engine specific arguments')
    for i in range(len(args)):
        print('   - %u: %s="%s"' % (i, arguments[i]['name'], args[i]))
    print(' - l: the logging function from /src/xovis-driver')
    print('')
    
    return True

async def insert (serial, camera_metadata, data):
    pretty_meta = json.dumps(camera_metadata, sort_keys=True, indent=4, separators=(',', ': '))
    pretty_data = json.dumps(data           , sort_keys=True, indent=4, separators=(',', ': '))
    
    print('CALL: insert')
    print(' - serial: the MAC address (%s) of the camera' % serial)
    print(' - camera_metadata: the metadata associated with the camera')
    for line in pretty_meta.split('\n'):
        print('   | %s' % line)
    print(' - data: the per-element data and metadata')
    for line in pretty_data.split('\n'):
        print('   | %s' % line)
    

async def uptime (t1, ut):
    print('CALL: uptime')
    print(' - t1: the current time (%f)' % t1)
    print(' - ut: the current uptime (%f)' % ut)

