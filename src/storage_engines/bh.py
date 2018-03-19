import json, io, requests
import db_comm.db_sort as retriever

description = 'Post camera data to BH database.'

arguments = [
    {
        'name':        'REST_SERVER_ADDRESS',
        'description': 'URL to push to',
        'example':     'http://server.dk:8079/endpoint',
    }
]

async def init (cfg, l):
    global config
    pretty_cfg = json.dumps(cfg, sort_keys=True, indent=4, separators=(',', ': '))
    
    config = cfg

    write = "Continues to use old 'metadata' table for camera reference."
    database = retriever.DatabaseConnection()
    if(database.table_exists("metadata")==False):
        database.create_metadata_table()
        write = "Created new 'metadata' table for camera reference."

    print('Description:', description)
    print('CALL: init')
    print(' - db:', write)
    print(' - cfg: the program-wide configuration as read from JSON')
    for line in pretty_cfg.split('\n'):
        print('   | %s' % line)  
    print('')
    
    return True

async def insert (serial, camera_metadata, data, handler_data):
    database = retriever.DatabaseConnection()
    meta_data = json.dumps(camera_metadata)
    sensor_data = json.dumps(data)
    if(database.exists(str(serial))==False):
        database.insert_metadata(meta_data, str(serial))
        database.create_sensordata_table(database.get_uuid(str(serial)))
    database.insert_sensordata(sensor_data, database.get_uuid(str(serial)), str(handler_data))   

async def uptime (t1, ut):
    print('CALL: uptime')
    print(' - t1: the current time (%f)' % t1)
    print(' - ut: the current uptime (%f)' % ut)


