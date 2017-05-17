# online-cf
Real-time collaborative filtering for item-item similarities

An implementation of the paper [Cloud based real-time collaborative filtering for item-item recommendations](http://dl.acm.org/citation.cfm?id=2577924).

We also stored which items every user rated and hence improved the performance.

The `cosine` branch has an experimental implementation of similarity calculation using numeric ratings instead of binary data.

## Dependencies
You must have redis.py. Install it with this instruction:
```sh
$ pip3 install redis
```

## Instructions
Scripts are written in Python 3.

Run the following redis servers running before running the scripts:
```sh
# cd redis.../src

$ redis-server --port 6379
$ redis-server --port 6380
$ redis-server --port 6381
$ redis-server --port 6382
```

Run the following python scripts via `run` script:
```sh
$ chmod +x run
$ ./run
```

Feed the scripts with data:
```sh
$ python3 client.py
```

Monitor the most similar items to an item live with `similars.py` script:
```sh
$ python3 similars.py 1
Showing the most similar items for 1
[['1220', '0.036'], ['315', '0.036'], ['4886', '0.036'], ['780', '0.036'], ['1923', '0.032'], ['586', '0.032'], ['4973', '0.030'], ['1198', '0.021'], ['457', '0.017'], ['296', '0.014']]
.
.
.
```

## Dockerized variant

docker-compose up
docker-compose scale s3=10
docker exec -it onlinecf_similars_1 /usr/local/bin/python /code/similars.py

### Redis

docker run -d --rm --name r1 -p 6379:6379 redis:alpine
docker run -d --rm --name r2 -p 6380:6379 redis:alpine
docker run -d --rm --name r3 -p 6381:6379 redis:alpine
docker run -d --rm --name r4 -p 6382:6379 redis:alpine

docker build -t ocf .

docker run -it --rm -p 8080:8080 --name s1 ocf /usr/local/bin/python /code/src/s1.py
docker run -it --rm --name s2 ocf /usr/local/bin/python /code/src/s2.py

docker run -it --rm onlinecf_s1 sh
/usr/local/bin/python /code/src/similars.py



docker exec -it onlinecf_similars_1 sh

