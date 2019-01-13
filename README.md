# News Crawler

## Environment

* python `3.6.5`
* apt package dependencies (`apt-pkgs.txt`)
* pip requirements (`requirements.txt`)

## Development

### Lint & Run unittest

### In `docker-compose`

``` sh
# run lint
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up lint

# run unittest
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up pytest
```

### In `native`

``` sh
# lint
$ flake8

# unittest
$ pytest
```
