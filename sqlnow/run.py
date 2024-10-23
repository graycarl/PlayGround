import sys
import datetime
import MySQLdb


def insert_static_data(conn, count):
    sql = """
    INSERT INTO `record_deletions_v2` (`object_int_id`, `record_id`, `record_external_id`, `operator_id`, `created_on`)
    VALUES (%s, %s, %s, %s, %s);
    """
    now = datetime.datetime.now()
    data = []
    for i in range(count):
        data.append((i, i, f'external_id_{i}', i, now))
    with conn.cursor() as cursor:
        cursor.executemany(sql, data)
    conn.commit()


def insert_now_data(conn, count):
    sql = """
    INSERT INTO `record_deletions_v2` (`object_int_id`, `record_id`, `record_external_id`, `operator_id`, `created_on`)
    VALUES (%s, %s, %s, %s, NOW());
    """
    data = []
    for i in range(count):
        data.append((i, i, f'external_id_{i}', i))
    with conn.cursor() as cursor:
        cursor.executemany(sql, data)
    conn.commit()


def main(conn, mode):
    if mode == 'static':
        insert_static_data(conn, 10000)
    elif mode == 'now':
        insert_now_data(conn, 10000)


if __name__ == "__main__":
    conn = MySQLdb.connect(
        host='127.0.0.1',
        port=10012,
        user='orion',
        passwd='orion',
        db='ODL_POC'
    )
    start_time = datetime.datetime.now()
    main(conn, sys.argv[1])
    end_time = datetime.datetime.now()
    print(f"Time taken: {end_time - start_time}")
