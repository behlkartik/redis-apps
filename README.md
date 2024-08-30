# Try Redis

Exploring redis by building script, apps using it.

## Running script

You can install redis as a standalone server on your local machine or run it as a docker container (recommended).

1. Make a directory which will act as a volume to store/restore redis data on container startup/shutdown:

```
mkdir -pv $HOME/redis-volume/data
```

2. Run redis as a docker container with the volume attached:

```
docker run -d --name redis-server -p 6379:6379 -v $HOME/db-backups/redis/data:/data redis
```

- By default redis will be available on localhost and on port 6379. You can check this by connecting to redis via RedisInsights (visually tool) or via redis-cli (I use both).

3. Install redis cli:

```
 brew tap ringohub/redis-cli
 brew install redis-cli
```

4. Run redis-cli (will connect by default to 127.0.0.1:6379):

```
redis-cli
```

5. Finally install redis for python and run the script:

```
cd project_root
pip install redis
python flash-sale-redis/flash_sale.py
```
