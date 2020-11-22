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


def generate_table_weight(cursor):
    try:
        cursor.execute("CREATE TABLE weight ("    
                        "weight_id INT NOT NULL AUTO_INCREMENT,"
                        "weight FLOAT,"
                        "date VARCHAR(255),"
                        "PRIMARY KEY(weight_id),"
                        "id VARCHAR(255),"
                        "FOREIGN KEY (id) REFERENCES user(id) )")
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
    delete_all_tables()
    errors = []
    conn = open_connection()
    cursor = conn.cursor()
    errors.append(generate_table_users(cursor))
    errors.append(generate_table_weight(cursor))
    cursor.close()
    if errors is not None:
        return errors


def show_tables():
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor]
    conn.close()
    return(tables)

def delete_all_tables():
    conn = open_connection()
    cursor = conn.cursor()
    tables = show_tables()

    for table in tables:
        delete_table(cursor, table)

def add_weight(weight, date, user_id):
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO weight (weight, date, id) VALUES(%s, %s, %s)', (weight, date, user_id))
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


data = {
    "weight": 86,
    "date": "2020-01-04",
    "id": 106443255120553717039
}