import uuid
from pprint import pprint
import psycopg2 as pgres
import time
import json

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = pgres.connect("dbname='bh-db' user='postgres' host='localhost' password='pass' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print('')
            print("CALL: Connected successfully to database.")
        except:
            print('')
            print("CALL: Cannot connect to database")

    def create_metadata_table(self):
        create_table_json = "CREATE TABLE metadata(uuid varchar(50), data jsonb)"
        self.cursor.execute(create_table_json)

    def insert_metadata(self, json, serial_number):
        temp_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(serial_number)))
        insert_metadata_json = "INSERT INTO metadata VALUES ('" + temp_uuid + "', '" + json + "')"
        self.cursor.execute(insert_metadata_json)

    def get_uuid(self, serial_number):    
        select_camera = "SELECT uuid FROM metadata WHERE data -> 'sensor-info' ->> 'serial-number' = '" + str(serial_number) + "'"   
        self.cursor.execute(select_camera)
        uuid = str(self.cursor.fetchone()[0])
        uuid_temp = str(uuid).split("-")
        uuid_joined = "".join(uuid_temp)
        return uuid_joined
    
    def exists(self, serial_number):
        select_camera = "SELECT uuid FROM metadata WHERE data -> 'sensor-info' ->> 'serial-number' = '" + str(serial_number) + "'" 
        self.cursor.execute(select_camera)
        answer = self.cursor.fetchall()
        if len(answer) > 0:
            return True
        else:
            return False
    
    def table_exists(self, TABLE_NAME):
        show_table = "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_catalog='bh-db' AND table_schema='public' AND table_name='" + TABLE_NAME + "')"
        self.cursor.execute(show_table)
        answer = self.cursor.fetchone()[0]
        return answer

    def create_sensordata_table(self, uuid):
        create_table_json = 'CREATE TABLE "' + str(uuid) + '"(datatype varchar(50), data jsonb, time_stamp varchar(50))'
        self.cursor.execute(create_table_json)
    
    def insert_sensordata(self, json_dt, uuid, handler_data):

        json_dt = json.loads(json_dt)
        s =  json_dt[list(json_dt.keys())[0]]

        jsondata = json.dumps(s)

        insert_metadata_json = 'INSERT INTO "' + str(uuid) + '"VALUES' + "('" + handler_data + "', '" + jsondata + "', '" + str(time.time()) + "')"
        self.cursor.execute(insert_metadata_json)

    def query_all(self, table):
        query_sql = "SELECT * FROM " + table
        self.cursor.execute(query_sql)
        cameras = self.cursor.fetchall()
        for camera in cameras:
            print("camera_metadata : {0}".format(camera))

    def drop_table(self, table):
        drop_table_sql = "DROP TABLE " + table
        self.cursor.execute(drop_table_sql)
