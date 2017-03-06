# The Automated Data Scientist

## Installing

Clone this project:

```bash
git clone git@github.com:TeradataBNL/autoscience.git
cd autoscience
```

Build the container image:

```bash
$ make build
```


## Getting started

Start the proxy:

```bash
$ make proxy/start
```

Start the API:

```bash
$ make python_restapi
```

Test the API:

```bash
$ curl -s localhost:8888/datasets/1 | jq . | head
{
  "cols": 13,
  "dims": 2,
  "variables": {
    "spdef": {
      "sample": [
        40,
        50,
        60,
        130,
```


When you're done, stop the proxy:

```bash
$ make proxy/stop
```

## License

Apache License, version 2.0
