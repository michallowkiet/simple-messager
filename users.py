import argparse

from psycopg2.errors import UniqueViolation

from db_utils import connection_params, db_close, db_connection
from security import check_password, hash_password
from users_model import Users

new_connection_params = {**connection_params, "database": "messages_db"}


def is_password_valid(pass_to_check):
    if len(pass_to_check) < 8:
        raise argparse.ArgumentTypeError("Hasło musi mieć co najmniej 8 znaków.")
    return pass_to_check


def create_user(username, password, cursor):
    try:
        is_password_valid(password)
        new_user = Users(username, password)
        new_user.save_to_db(cursor)
        print(f"Utworzono nowego użytkownika: {new_user.username}")
    except UniqueViolation:
        print(f"Użytkownik o nazwie {args.username} juz istnieje.")
    except Exception as e:
        print(f"Błąd podczas tworzenia nowego użytkownika: {str(e)}")


def edit_user(username, password, new_password, cursor):
    try:
        user = Users.load_user_by_username(cursor, username)

        if not check_password(password, user.hashed_password):
            raise argparse.ArgumentTypeError("Podane hasło jest błędne.")

        if not is_password_valid(new_password):
            raise argparse.ArgumentTypeError("Hasło musi mieć co najmniej 8 znaków.")

        user.hashed_password = hash_password(new_password)
        user.save_to_db(cursor)
        print(f"Edytowano użytkownika: {user.username}")
    except Exception as e:
        print(f"Błąd podczas edycji użytkownika: {str(e)}")


def list_users(cursor):
    try:
        users = Users.load_all_users(cursor)
        for user in users:
            print(f"Użytkownik: {user.username}")
    except Exception as e:
        print(f"Błąd podczas listowania użytkowników: {str(e)}")


def delete_user(username, password, cursor):
    try:
        user = Users.load_user_by_username(cursor, username)

        if not check_password(password, user.hashed_password):
            raise argparse.ArgumentTypeError("Podane hasło jest błędne.")

        user.delete(cursor)
        print(f"Usunieto użytkownika: {user.username}")
    except Exception as e:
        print(f"Błąd podczas usuwania użytkownika: {str(e)}")


if __name__ == "__main__":
    db = db_connection(new_connection_params)
    cursor = db["cursor"]

    parser = argparse.ArgumentParser(description="Zarządzanie użytkownikami")
    parser.add_argument("-u", "--username", help="username")
    parser.add_argument("-p", "--password", help="hasło (min 8 znaków)")
    parser.add_argument("-n", "--new_password", help="nowe hasło (min 8 znaków)")
    parser.add_argument("-e", "--edit", action="store_true", help="Edytuj użytkownika")
    parser.add_argument("-d", "--delete", action="store_true", help="Usuń użytkownika")
    parser.add_argument("-l", "--list", action="store_true", help="Lista użytkowników")

    args = parser.parse_args()

    if args.list:
        list_users(cursor)

    elif args.username and args.password:
        if args.new_password:
            edit_user(args.username, args.password, args.new_password, cursor)
        elif args.delete:
            delete_user(args.username, args.password, cursor)
        else:
            create_user(args.username, args.password, cursor)
    else:
        parser.print_help()

    db_close(db)
