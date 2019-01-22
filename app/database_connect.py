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
        happeningOn TIMESTAMP NOT NULL,
        host VARCHAR (30) NOT NULL,
        topic VARCHAR (30) NOT NULL,
        summary VARCHAR (30) NOT NULL,
        location VARCHAR (30) NOT NULL);"""

    return [users, meetups]


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

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        raise error
