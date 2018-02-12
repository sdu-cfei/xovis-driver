import json, io, requests

description = 'Post data to Odense rest interface'

arguments = [
    {
        'name':        'REST_SERVER_ADDRESS',
        'description': 'URL to push to',
        'example':     'http://server.dk:8079/endpoint',
    }
]

async def init (cfg, args, l):
    global config,restServerIp
    pretty_cfg = json.dumps(cfg, sort_keys=True, indent=4, separators=(',', ': '))
    
    restServerIp = args[0]
    config = cfg

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

async def insert (serial, camera_metadata, data, handler_data):
    s = {}
    s["HandlerData"] = handler_data
    for name in data:
        for direction in data[name]:
            s[name] = {}
            readings = data[name][direction]['readings']
            metadata = data[name][direction]['meta']
            s[name]["readings"] = readings
            s[name]["camera_metadata"] = metadata
            
    await postData(json.dumps(s, indent=2, sort_keys=True, separators=(',', ': ')))        

async def uptime (t1, ut):
    print('CALL: uptime')
    print(' - t1: the current time (%f)' % t1)
    print(' - ut: the current uptime (%f)' % ut)

async def postData(json):
    headers = {'Content-type': 'application/json'}
    response = await requests.post(restServerIp, data = json, headers = headers)

