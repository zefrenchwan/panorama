from psycopg import  connect
from psycopg.rows import dict_row
from datetime import datetime
from os import getenv


dbconf_url = getenv('DBCONF_URL')
connection = connect(conninfo=dbconf_url,row_factory=dict_row)

def upsert_task(task_id: str, processor_name: str, start: datetime, end: datetime, success: bool, errors: list[str]|None= None):
    with connection.cursor() as cursor:
        cursor.execute("call collections.upsert_task(%s,%s,%s,%s,%s,%s)",(task_id, processor_name, start, end, success, errors))