import psycopg2
import bcrypt
from psycopg2 import Error
import re


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt(10))


def check_password(passwd, hashed):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(passwd, hashed)


def password_check(password):
    """
    Verify the strength and sanitize the password
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """
    # calculating the length
    length_error = len(password) < 8
    if (length_error):
        return "Your password has less than 8 characters"
    # searching for symbols
    symbol_error = re.search(
        r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    if (symbol_error):
        return "Your password should have \n at least 1 symbol"
    # searching for digits
    digit_error = re.search(r"\d", password) is None
    if (digit_error):
        return "Your password should have \n at least 1 digit"
    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None
    if (uppercase_error):
        return "Your password should have \n at least 1 uppercase"
    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None
    if (lowercase_error):
        return "Your password should have \n at least 1 lowercase"

    return "Good password"


def register(username, password, password2):
    if (password != password2):
        return False, "Confirm password doesn't match"

    checkMessage = password_check(password)
    if (checkMessage != "Good password"):
        return False, checkMessage

    try:
        # Connect to an existing database
        connection = psycopg2.connect(
            'postgresql://bronto.ewi.utwente.nl/dab_di20212b_40', user="dab_di20212b_40", password="7M+HS5VHgf9aZ00a")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        query = "SELECT u.username FROM mod5_project.user u WHERE username = %s;"
        cursor.execute(query, [username])
        newrecord = cursor.fetchall()

        if len(newrecord) != 0:
            return False, "Username already exists"
        else:
            hashedPass = get_hashed_password(str(password).encode('utf-8'))
            insertQuery = "INSERT INTO mod5_project.user(password_hash, username, num_fail, is_admin) VALUES (%s, %s , 0, FALSE)"
            cursor.execute(
                insertQuery, [hashedPass.decode('utf8', 'strict'), username])
            connection.commit()
            return True, "Register successfully"

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def login(username, password):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(
            'postgresql://bronto.ewi.utwente.nl/dab_di20212b_40', user="dab_di20212b_40", password="7M+HS5VHgf9aZ00a")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")


        query = "SELECT u.username, u.password_hash FROM mod5_project.user u WHERE username = %s;"
        cursor.execute(query, [username])
        # example of bug code with SQL injection
        # query = "SELECT u.username, u.password_hash FROM mod5_project.user u WHERE username = " + username
        # cursor.execute(query)
        newrecord = cursor.fetchall()

        print(newrecord)

        if len(newrecord) == 0:
            return False
            # return "Username does not exist"
        else:
            hashedPassFromDatabase = newrecord[0][1]
            encoded_pass = str(password).encode('utf-8')
            return check_password(encoded_pass, str(hashedPassFromDatabase).encode('utf-8'))

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# SQL injection example
# login("'' OR '0' = '0'; SELECT * FROM mod5_project.score", "ascsac1")
