import psycopg2
from psycopg2 import Error
from datetime import datetime


def storingscores(username, score):
    try:
        # Connect to an existing database
        connection = psycopg2.connect('postgresql://bronto.ewi.utwente.nl/dab_di20212b_40', user="dab_di20212b_40",
                                      password="7M+HS5VHgf9aZ00a")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        currentime = datetime.now()

        query = "INSERT INTO mod5_project.score(username, score, date) VALUES (%s, %s, %s)"
        cursor.execute(query, [username, score, currentime])
        connection.commit()
        return('het is gelukt')

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def gethighscores(is_unique=True):
    try:
        # Connect to an existing database
        connection = psycopg2.connect('postgresql://bronto.ewi.utwente.nl/dab_di20212b_40', user="dab_di20212b_40",
                                      password="7M+HS5VHgf9aZ00a")

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        currentime = datetime.now()

        if is_unique:
            query = "SELECT MAX(score),username FROM mod5_project.score GROUP BY username ORDER BY MAX(score) DESC LIMIT 10;"
        # else:
        #     query = "SELECT username,score FROM mod5_project.score ORDER BY score DESC LIMIT 10;"
        cursor.execute(query)
        topscores = cursor.fetchall()
        return topscores

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
