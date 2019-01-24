import os
import psycopg2
from instance.config import app_config

config_name = os.getenv('FLASK_ENV')
x = app_config[config_name]
y = x()

connString = 'dbname=%s user=%s password=%s host=%s' % (
    y.POSTGRES_DB, y.POSTGRES_USER, y.POSTGRES_PASSWORD, y.POSTGRES_HOST)


def connect():
    """
    Function to connect to a database and return connection instance
    """

    try:
        conn = psycopg2.connect(connString)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        raise error


def destroy_database():
    """
    Function to delete all tables
    """

    conn = psycopg2.connect(connString)
    curr = conn.cursor()

    curr.execute(""" DROP TABLE IF EXISTS users CASCADE; """)
    curr.execute(""" DROP TABLE IF EXISTS meetups CASCADE; """)
    curr.execute(""" DROP TABLE IF EXISTS questions CASCADE; """)

    conn.commit()
    conn.close()


def create_table_schemas():
    """
    Function to create table schemas
    """
    users = """ CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY NOT NULL,
        firstname VARCHAR (30) NOT NULL,
        lastname VARCHAR (30) NOT NULL,
        email VARCHAR (30) NOT NULL,
        phoneNumber VARCHAR (30),
        username VARCHAR (20) NOT NULL,
        registered_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
        password VARCHAR (256) NOT NULL,
        isAdmin BOOLEAN DEFAULT false);"""

    meetups = """ CREATE TABLE IF NOT EXISTS meetups (meetup_id serial PRIMARY KEY NOT NULL,
        created_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
        happeningOn VARCHAR NOT NULL,
        host VARCHAR (30) NOT NULL,
        topic VARCHAR (30) NOT NULL,
        summary VARCHAR (100) NOT NULL,
        location VARCHAR (30) NOT NULL);"""

    questions = """ CREATE TABLE IF NOT EXISTS questions (question_id serial PRIMARY KEY NOT NULL,
        meetup_id INTEGER NOT NULL,
        created_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
        title VARCHAR NOT NULL,
        body VARCHAR NOT NULL,
        author VARCHAR (30) NOT NULL,
        votes INTEGER NOT NULL DEFAULT 0);"""

    comments = """ CREATE TABLE IF NOT EXISTS comments (comment_id serial PRIMARY KEY NOT NULL,
        question_id INTEGER NOT NULL,
        created_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
        body VARCHAR NOT NULL,
        author VARCHAR (30) NOT NULL);"""

    return [users, meetups, questions, comments]


def create_tables():
    """
    Function to create tables
    """
    try:
        conn = psycopg2.connect(connString)
        curr = conn.cursor()

        tables = create_table_schemas()

        for table in tables:
            curr.execute(table)
        conn.commit()
        conn.close()
        print("tables created")

    except (Exception, psycopg2.DatabaseError) as error:
        raise error
