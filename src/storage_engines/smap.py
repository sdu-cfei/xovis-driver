import json
import aiohttp
from uuid import UUID
from hashlib import md5

description = 'Post to a sMAP Archiver'

arguments = [
    {
        'name':        'ARCHIVER_URL',
        'description': 'URL to push to',
        'example':     'http://server.dk:8079/add/cac7d1e0-17d8-4c87-b0e3-aa6b27e7f7f6',
    },
]

async def init (cfg, args, l):
    global config, archiver_url, uptime_uuid, log
    
    # guard: args
    if len(args)!= len(arguments):
        print('Error: Storage engine initializer received %u -- not %u -- arguments' % (len(args), len(arguments)))
        return False
    
    log          = l
    config       = cfg
    archiver_url = args[0]
    uptime_uuid  = get_uuid(config['smap']['uuid'], '/uptime')
    
    return True

async def insert (serial, camera_metadata, data):
    log('insert-smap', {'serial': serial, 'camera_metadata': camera_metadata, 'data': data})
    
    # construct structure
    s = {}
    for name in data:
        for direction in data[name]:
            generation = 1
            readings = data[name][direction]['readings']
            metadata = data[name][direction]['meta']
            
            path = '/%s/%u/%s/%s' % (serial, generation, name, direction)
            uuid = get_uuid(config['smap']['uuid'], path)
            
            s[path] = {
                'uuid': uuid,
                'Metadata': {
                    'SourceName': config['smap']['sourcename'],
                    'Relations': {
                        'uptime': uptime_uuid,
                    },
                    'Upstream': {
                        'Direction': direction,
                        'Element': metadata,
                        'Camera': camera_metadata,
                    },
                },
                'Properties': {
                    'Timezone':      'Europe/Copenhagen',
                    'UnitofMeasure': 'count',
                    'ReadingType':   'long',
                },
                'Readings': list(map(lambda pair: (int(pair[0]*1000), pair[1]), readings)),
            }
            stringify_tree(s[path]['Metadata']['Upstream'])
    
    # perform insert
    await add2smap(s)

async def uptime (t1, ut):
    log('uptime-smap', {'t1': t1, 'ut': ut})
    
    # construct
    s = {
        '/uptime': {
            'uuid': uptime_uuid,
            'Metadata': {
                'SourceName': config['smap']['sourcename'],
            },
            'Properties': {
                'Timezone':      'Europe/Copenhagen',
                'UnitofMeasure': 'ms',
                'ReadingType':   'double',
            },
            'Readings': [ (int(t1*1000), ut) ],
        },
    }
    
    # push
    await add2smap(s)

###############################################################################

def get_uuid (driver_uuid, path):
    s = '%s: %s' % (driver_uuid, path)
    return str(UUID(bytes=md5(s.encode('utf-8')).digest()))

def stringify_tree (node):
    for child in node:
        if type(node[child])==dict:
            stringify_tree(node[child])
        else:
            node[child] = str(node[child])

async def add2smap (data):
    log('add2smap', {'data': data})
    msg = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
    # transmit message
    h = {'content-type': 'application/json', 'User-Agent': 'smap-driver-xovis'}
    async with aiohttp.ClientSession() as session:
        async with session.post(archiver_url, data=msg, headers=h) as response:
            if response.status != 200:
                log('publication-failure', {'response': response.status, 'message': msg})
            response.close()

