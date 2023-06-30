# gg-submission 🐋

## Building and running

Running the docker container

```ps
docker compose up --build
```

```ps
PS C:\Users\muham\OneDrive\Documents\GitHub\gg-submission> docker compose up --build
[+] Building 5.5s (12/12) FINISHED
 => [server internal] load .dockerignore                                                                                                                                                                                    0.0s
 => => transferring context: 680B                                                                                                                                                                                           0.0s
 => [server internal] load build definition from Dockerfile                                                                                                                                                                 0.0s
 => => transferring dockerfile: 1.57kB                                                                                                                                                                                      0.0s
 => [server] resolve image config for docker.io/docker/dockerfile:1                                                                                                                                                         2.8s
 => CACHED [server] docker-image://docker.io/docker/dockerfile:1@sha256:39b85bbfa7536a5feceb7372a0817649ecb2724562a38360f4d6a7782a409b14                                                                                    0.0s
 => [server internal] load metadata for docker.io/library/python:3.11.4-slim                                                                                                                                                2.0s
 => [server base 1/5] FROM docker.io/library/python:3.11.4-slim@sha256:53a67c012da3b807905559fa59fac48a3a68600d73c5da10c2f0d8adc96dbd01                                                                                     0.0s
 => [server internal] load build context                                                                                                                                                                                    0.0s
 => => transferring context: 63B                                                                                                                                                                                            0.0s
 => CACHED [server base 2/5] WORKDIR /app                                                                                                                                                                                   0.0s
 => CACHED [server base 3/5] RUN adduser     --disabled-password     --gecos ""     --home "/nonexistent"     --shell "/sbin/nologin"     --no-create-home     --uid "10001"     appuser                                    0.0s
 => CACHED [server base 4/5] RUN --mount=type=cache,target=/root/.cache/pip     --mount=type=bind,source=requirements.txt,target=requirements.txt     python -m pip install -r requirements.txt                             0.0s
 => CACHED [server base 5/5] COPY . .                                                                                                                                                                                       0.0s
 => [server] exporting to image                                                                                                                                                                                             0.0s
 => => exporting layers                                                                                                                                                                                                     0.0s
 => => writing image sha256:a1c3115f86b1e4e82f6c60c8c4bcf7abc700f2d189ca443b863716aa57e083ff                                                                                                                                0.0s
 => => naming to docker.io/library/gg-submission-server                                                                                                                                                                     0.0s
time="2023-07-01T01:17:22+05:30" level=warning msg="buildx: git was not found in the system. Current commit information was not captured by the build"
[+] Running 2/2
 ✔ Network gg-submission_default     Created                                                                                                                                                                                0.1s
 ✔ Container gg-submission-server-1  Created                                                                                                                                                                                0.2s
Attaching to gg-submission-server-1
gg-submission-server-1  |  * Serving Flask app 'app' (lazy loading)
gg-submission-server-1  |  * Environment: production
gg-submission-server-1  |    WARNING: This is a development server. Do not use it in a production deployment.
gg-submission-server-1  |    Use a production WSGI server instead.
gg-submission-server-1  |  * Debug mode: off
gg-submission-server-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
gg-submission-server-1  |  * Running on http://127.0.0.1:5000
gg-submission-server-1  | Press CTRL+C to quit

```

## Automated testing

First, need to start the server and then run the following `unittest` command.

```ps
$> python -m unittest test_app.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.013s

OK
```

## Manual testing

Testing using `Invoke-RestMethod`

### Setting TLS, TLS 1.1 and TLS 1.2

```ps
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12
```

### Insertion

```ps
Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/insert" -Method POST -ContentType "application/json" -Body (@{
    dim = @(
        @{key = "device"; val = "mobile"},
        @{key = "country"; val = "US"}
    )
    metrics = @(
        @{key = "webreq"; val = 70},
        @{key = "timespent"; val = 302}
    )
} | ConvertTo-Json)
```

```ps
Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/insert" -Method POST -ContentType "application/json" -Body (@{
    dim = @(
        @{key = "device"; val = "mobile"},
        @{key = "country"; val = "IN"}
    )
    metrics = @(
        @{key = "webreq"; val = 7},
        @{key = "timespent"; val = 32}
    )
} | ConvertTo-Json)
```

```ps
Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/insert" -Method POST -ContentType "application/json" -Body (@{
    dim = @(
        @{key = "device"; val = "desktop"},
        @{key = "country"; val = "US"}
    )
    metrics = @(
        @{key = "webreq"; val = 50},
        @{key = "timespent"; val = 208}
    )
} | ConvertTo-Json)
```

### Querying

```ps
Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/query" -Method POST -ContentType "application/json" -Body (@{
    dim = @(
        @{key = "device"; val = "mobile"},
        @{key = "country"; val = "US"}
    )
} | ConvertTo-Json)

```

## Output

```ps
PS C:\Users\muham> Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/insert" -Method POST -ContentType "application/json" -Body (@{
>>     dim = @(
>>         @{key = "device"; val = "mobile"},
>>         @{key = "country"; val = "US"}
>>     )
>>     metrics = @(
>>         @{key = "webreq"; val = 70},
>>         @{key = "timespent"; val = 302}
>>     )
>> } | ConvertTo-Json)

message
-------
Data inserted successfully.


PS C:\Users\muham> Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/insert" -Method POST -ContentType "application/json" -Body (@{
>>     dim = @(
>>         @{key = "device"; val = "mobile"},
>>         @{key = "country"; val = "IN"}
>>     )
>>     metrics = @(
>>         @{key = "webreq"; val = 7},
>>         @{key = "timespent"; val = 32}
>>     )
>> } | ConvertTo-Json)

message
-------
Data inserted successfully.

PS C:\Users\muham> Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/insert" -Method POST -ContentType "application/json" -Body (@{
>>     dim = @(
>>         @{key = "device"; val = "desktop"},
>>         @{key = "country"; val = "US"}
>>     )
>>     metrics = @(
>>         @{key = "webreq"; val = 50},
>>         @{key = "timespent"; val = 208}
>>     )
>> } | ConvertTo-Json)

message
-------
Data inserted successfully.

PS C:\Users\muham> Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/query" -Method POST -ContentType "application/json" -Body (@{
>>     dim = @(
>>         @{key = "device"; val = "mobile"},
>>         @{key = "country"; val = "US"}
>>     )
>> } | ConvertTo-Json)

timespent webreq
--------- ------
      302     70


PS C:\Users\muham> Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/query" -Method POST -ContentType "application/json" -Body (@{
>>     dim = @(
>>         @{key = "device"; val = "mobile"},
>>         @{key = "country"; val = "IN"}
>>     )
>> } | ConvertTo-Json)

timespent webreq
--------- ------
       32      7


PS C:\Users\muham> Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/insert" -Method POST -ContentType "application/json" -Body (@{
>>     dim = @(
>>         @{key = "device"; val = "mobile"},
>>         @{key = "country"; val = "IN"}
>>     )
>>     metrics = @(
>>         @{key = "webreq"; val = 7},
>>         @{key = "timespent"; val = 32}
>>     )
>> } | ConvertTo-Json)

message
-------
Data inserted successfully.


PS C:\Users\muham> Invoke-RestMethod -Uri "http://127.0.0.1:5000/v1/query" -Method POST -ContentType "application/json" -Body (@{
>>     dim = @(
>>         @{key = "device"; val = "mobile"},
>>         @{key = "country"; val = "IN"}
>>     )
>> } | ConvertTo-Json)

timespent webreq
--------- ------
       64     14


PS C:\Users\muham>
```
