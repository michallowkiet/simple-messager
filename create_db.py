import psycopg2

from db_utils import connection_params, db_close, db_connection


def create_database(connection_params, new_db):
    """Tworzy nową bazę danych w PostgreSQL, obsługując potencjalny błąd duplikacji.

    Args:
        connection_params (dict): Słownik zawierający parametry połączenia.
        new_db (str): Nazwa nowej bazy danych.
    """

    db = db_connection(connection_params)
    cursor = db["cursor"]

    try:
        cursor.execute(f"CREATE DATABASE {new_db}")
        print(f"Baza danych '{new_db}' została utworzona pomyślnie.")

        connection_params["database"] = new_db
    except psycopg2.errors.DuplicateDatabase:
        print(f"Baza danych '{new_db}' już istnieje.")

    db_close(db)


def create_users_table(connection_params):
    """Tworzy tabelę 'users' w bazie danych PostgreSQL.

    Args:
        connection_params (dict): Słownik zawierający parametry połączenia.
    """

    db = db_connection(connection_params)
    cursor = db["cursor"]

    try:
        cursor.execute(
            """
          CREATE TABLE users (
              id SERIAL PRIMARY KEY,
              username VARCHAR(255) NOT NULL UNIQUE,
              hashed_password VARCHAR(255) NOT NULL
          );
      """
        )
        print("Tabela 'users' została utworzona pomyślnie.")
    except psycopg2.errors.DuplicateTable:
        print("Tabela 'users' już istnieje.")
    except Exception as e:
        print(f"Błąd podczas tworzenia tabeli 'users': {str(e)}")

    db_close(db)


def create_messages_table(connection_params):
    """Tworzy tabelę 'messages' w bazie danych PostgreSQL.

    Args:
        connection_params (dict): Słownik zawierający parametry połączenia.
    """

    db = db_connection(connection_params)
    cursor = db["cursor"]

    try:
        cursor.execute(
            """
          CREATE TABLE messages (
              id SERIAL PRIMARY KEY,
              from_id INTEGER NOT NULL,
              to_id INTEGER NOT NULL,
              text TEXT NOT NULL,
              creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (from_id) REFERENCES users (id) ON DELETE CASCADE,
              FOREIGN KEY (to_id) REFERENCES users (id) ON DELETE CASCADE
          );
      """
        )
        print("Tabela 'messages' została utworzona pomyślnie.")
    except psycopg2.errors.DuplicateTable:
        print("Tabela 'messages' już istnieje.")
    except Exception as e:
        print(f"Błąd podczas tworzenia tabeli 'messages': {str(e)}")

    db_close(db)


if __name__ == "__main__":
    new_db_name = "messages_db"
    create_database(connection_params, new_db_name)

    create_users_table(connection_params)
    create_messages_table(connection_params)
