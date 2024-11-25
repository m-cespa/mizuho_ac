**SERVER SETUP**

Identify PostgreSQL version:
```
psql --version
```

Edit PostgreSQL conf file:
```
sudo nano /etc/postgresql/{version}/main/postgresql.conf
```

Enable listening to specific or all ip addresses:
```
listen_addresses = '*'
```

Setup password authentication:
```
sudo nano /etc/postgresql/{version}/main/pg_hba.conf
```
This allows authentication from any ip address by passing `0.0.0.0/0` or a specified ip:
```
host    all             all             0.0.0.0/0            md5
```

Restart postgresql to implement changes:
```
sudo systemctl restart postgresql
```

Login as superuser postgres to create new user profiles with passwords:
```
psql -U postgres
CREATE USER new_user WITH PASSWORD 'new_password';
GRANT ALL PRIVILEGES ON DATABASE your_database TO new_user;
```

To view all users:
```
\du
```
Enable logging of user activity:
```
ALTER SYSTEM SET logging_collector = 'on';
ALTER SYSTEM SET log_statement = 'all';
```

Require user passwords to have certain complexity level:
```
ALTER SYSTEM SET password_encryption = 'scram-sha-256';
```

