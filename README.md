GeoJSON Visualization
=====================

Quick visualization during prototyping.

How?
----

1. Start `server.py`
2. Open <http://localhost:8000>
3. POST GeoJSON data to `/save` using `curl` and have the data listed in the web page
4. Open the data in the web browser to see the GeoJSON data
5. Want to save the data permanently? Just POST `/store/[data-index]`

API
---

### GET /status

Response:

```
{"status": "ok", "total": 0}
```

### POST /save

Parameters:

* `data`: GeoJSON data

Response:

```
{"status": "ok", "data_index": 1}
```

Example:

```
$ curl http://localhost:8000/save -d data='{
    "type": "LineString",
    "coordinates": [[-100, 40], [-105, 45], [-110, 55]]
}'
```

### GET /update?start=[index]

Parameters:

* `start`: start index

Response:

```
{"status": "ok",
 "start": 0,
 "data": [
   {"timestamp": "2013-10-10 15:46:54", "id": null, "index": 0}
 ]
}
```

### POST /get/[index]

Parameters:

* `index`: data index

Response:

```
{"status": "ok",
 "data": {
   "timestamp": "2013-10-10 15:46:54",
   "data": {"type": "LineString", "coordinates": [[-100, 40], [-105, 45], [-110, 55]]},
   "data_id": null
 }
}
```

### POST /store/[index]

Store data to database for later retrieval

Parameter:

* `index`: data index

Response:

```
{"status": "ok", "data_id": 1}
```





