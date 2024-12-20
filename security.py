import bcrypt


# Hash a password using scrypt
def hash_password(password):
    password = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password.decode("utf-8")


# Check if a password is correct
def check_password(password, hashed):
    password = bytes(password, "utf-8")
    hashed_password = hashed.encode("utf-8")
    return bcrypt.checkpw(password, hashed_password)
