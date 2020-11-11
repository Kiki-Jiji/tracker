# GCP SQl

Guide to using cloud SQL with flask

* Setup MYSQL on cloud SQL [setup mysql tutorial](https://towardsdatascience.com/sql-on-the-cloud-with-python-c08a30807661) on GCP
* Create table 
* Setup Python to work with the database

## Details

Create a mysql instance. Set the root password and save it somewhere, you will need it soon!

Go to connections and add network- add 0.0.0.0/0. This allows all! Big security risk so get SSL certificates- three different files.

To connect to the instance you need four things

* Username — this should be root (as in user: 'root')
* Password — we set this up earlier. Root Password
* Host — the public IP address of our SQL instance, we can find it on our Cloud SQL Instances page. - public IP address
* SSL certification — the three files, server-ca.pem, client-cert.pem, and client-key.pem.

```python
import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': 'Password123',
    'host': '94.944.94.94',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

# now we establish our connection
cnxn = mysql.connector.connect(**config)
```


# Issues

```
pip install mysql-connector-python

# If that doesn't work then try
pip install mysql-connector-python-rf
```

For SQL instance use `0.0.0.0/0` to give access to all IP's
