import os
from flask import jsonify
import mysql.connector
from mysql.connector.constants import ClientFlag
import click
from flask.cli import with_appcontext
from mysql.connector import ProgrammingError

root_password = os.environ.get('MYSQL_INSTANCE_ROOT_PASSWORD')
host = os.environ.get('PUBLIC_IP_ADDRESS')


def create_database():
    if root_password is not None and host is not None:
        config = {
            'user': 'root',
            'password': root_password,
            'host': host,
            'client_flags': [ClientFlag.SSL],
            'ssl_ca': 'server-ca.pem',
            'ssl_cert': 'client-cert.pem',
            'ssl_key': 'client-key.pem'
        }
    else:
        raise ValueError('GLobal Variables missing')
    conn = open_connection(config=config)
    cursor = conn.cursor()  # initialize connection cursor
    try:
        cursor.execute('CREATE DATABASE IF NOT EXISTS tracker') 
        conn.close()
    except Exception as e:
        conn.close()
        return(e)


def generate_table_songs(cursor):
    try:
        cursor.execute("CREATE TABLE songs ("    
                        "song_id INT NOT NULL AUTO_INCREMENT,"
                        "title VARCHAR(255),"
                        "artist VARCHAR(255),"
                        "genre VARCHAR(255),"
                        "PRIMARY KEY(song_id) )")
    except ProgrammingError as e:
        return(e.msg)

def generate_table_users(cursor):
    try:
         cursor.execute("CREATE TABLE user ("
                        "id VARCHAR(255) PRIMARY KEY,"
                        "name VARCHAR(255) NOT NULL,"
                        "email VARCHAR(255) UNIQUE NOT NULL,"
                        "profile_pic VARCHAR(255) NOT NULL )" )
    except ProgrammingError as e:
        return(e.msg)

def delete_table(cursor, table):
    cursor.execute(f"DROP TABLE {table}")

def open_connection(config=None):
    if config is None:
        if root_password is not None and host is not None:
            config = {
                'user': 'root',
                'password': root_password,
                'host': host,
                'client_flags': [ClientFlag.SSL],
                'ssl_ca': 'server-ca.pem',
                'ssl_cert': 'client-cert.pem',
                'ssl_key': 'client-key.pem',
                'database': 'tracker'
            }
        else:
            raise ValueError('GLobal Variables missing')
    else:
        config = config
    cnxn = mysql.connector.connect(**config)
    return cnxn

def init_tables():

    create_database()

    errors = []
    conn = open_connection()
    cursor = conn.cursor()
    errors.append(generate_table_songs(cursor))
    errors.append(generate_table_users(cursor))
    cursor.close()
    if errors is not None:
        return errors


def show_tables():
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    for i in cursor:
        print(i)
    conn.close()

def get_songs():
    conn = open_connection()
    cursor = conn.cursor()

    result = cursor.execute('SELECT * FROM songs;')
    songs = cursor.fetchall()

    got_songs = jsonify(songs)

    conn.close()
    return got_songs

def add_songs(song):
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO songs (title, artist, genre) VALUES(%s, %s, %s)', (song["title"], song["artist"], song["genre"]))
    conn.commit()
    conn.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_tables()
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command)