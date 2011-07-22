import sys
import codecs
import MySQLdb

from w3fu import config


insert_sql = '''
    insert ignore into city (id, name, region, district)
    values (%s, %s, %s, %s)
'''

conn = MySQLdb.connect(host=config.conn_host,
                       db=config.conn_db,
                       user=config.conn_user,
                       passwd=config.conn_passwd,
                       use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()
for line in codecs.getreader('cp1251')(sys.stdin):
    (id, city, region, district) = line.split('\t')[:4]
    cursor.execute(insert_sql, (id, city, region, district))
conn.commit()
