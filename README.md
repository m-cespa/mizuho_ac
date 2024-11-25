Server setup:

identify PostgreSQL version:
`psql --version`

edit PostgreSQL conf file:
`sudo nano /etc/postgresql/{version}/main/postgresql.conf`

enable listening to specific or all ip addresses:
`listen_addresses = '*'`

setup password authentication:
`sudo nano /etc/postgresql/{version}/main/pg_hba.conf`
`host    all             all             0.0.0.0/0            md5`

restart postgresql to implement changes:
`sudo systemctl restart postgresql`

login as superuser postgres to create new user profiles with passwords:
`psql -U postgres`
`CREATE USER new_user WITH PASSWORD 'new_password';`
`GRANT ALL PRIVILEGES ON DATABASE your_database TO new_user;`

to view all users:
`\du`
enable logging of user activity:
```
ALTER SYSTEM SET logging_collector = 'on';
ALTER SYSTEM SET log_statement = 'all';
```

require user passwords to have certain complexity level:
`ALTER SYSTEM SET password_encryption = 'scram-sha-256';`

