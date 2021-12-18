# fathom
Utility for collecting League of Legends match data

## Getting Started
### Python
This project is managed using [Poetry](https://python-poetry.org/docs/master/).

See the poetry documentation for installation instructions. As of poetry 1.1.12
it can be installed using:
```
$ curl -sSL https://install.python-poetry.org | python3 -
```

> **Note**: You may need to install `python3-venv` as a dependency

Once installed, run `poetry install` from the project root to install dependencies.
Then run `poetry shell` to test that the virtual environment is working.

### Redis
This project depends on [Redis](https://redis.io).
To install Redis:
```
Linux/WSL:
$ sudo apt install redis-server
```
This will install `redis-cli` and `redis-server`.

To test your installation, run:
```
$ sudo service redis-server restart
$ redis-cli
```
Then from the `redis-cli`:
```
127.0.0.1:6379> PING
PONG
127.0.0.1:6379>
```
Use `sudo service redis-server stop` to stop the background redis instance.

For this project, run:
```
$ ./start-redis.sh
```
This will start a redis-server using the project's redis configuration *inside* the
`redis` directory. This is done so that the append-only file and dump file are stored
inside the `redis` directory.
