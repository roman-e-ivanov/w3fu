import sys
import MySQLdb

from w3fu import config


select_cities_sql = '''
    select id from city
'''

clear_sql = '''
    truncate table iprange
'''

insert_sql = '''
    insert ignore into iprange (city_id, start, end)
    values (%s, %s, %s)
'''

conn = MySQLdb.connect(host=config.conn_host,
                       db=config.conn_db,
                       user=config.conn_user,
                       passwd=config.conn_passwd,
                       use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()
cursor.execute(select_cities_sql)
cities = set([id for (id,) in cursor.fetchall()])
good = []
bad = []
for line in sys.stdin:
    (start, end, _, country, city_id) = line.split('\t')[:5]
    try:
        city_id = int(city_id)
    except ValueError:
        continue
    if city_id not in cities:
        bad.append((city_id, start, end))
    else:
        good.append((city_id, start, end))
if bad:
    print(bad)
else:
    cursor.execute(clear_sql)
    for (city_id, start, end) in good:
        cursor.execute(insert_sql, (city_id, start, end))
    conn.commit()
