# Tracker 

Tracks stuff

Database connection is establish via SSL ( you need the three SSL files to connect)

```bash
# Two env vars are needed
export MYSQL_INSTANCE_ROOT_PASSWORD=whatever_it_is
export PUBLIC_IP_ADDRESS=whatever_it_is

export FLASK_APP=tracker
export FLASK_ENV=development

flask run

```

# CLI Available

`flask init-db`

## Docs 

Check `gcp_mysql_setup.md` for some rough (and I mean rough) docs
