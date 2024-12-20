import psycopg2

connection_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres",
    "port": 5432,
}


def db_connection(connection_params):
    try:
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True
        cursor = conn.cursor()
        return {"conn": conn, "cursor": cursor}
    except psycopg2.errors.OperationalError as e:
        print(f"Błąd połączenia z baza danych: {str(e)}")
        return None


def db_close(dict):
    dict["cursor"].close()
    dict["conn"].close()
