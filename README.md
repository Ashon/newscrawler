# News Crawler

News crawler project using `Celery`, `BeautifulSoup4`, `mecab-ko`.

## Architecture

### Components

- `<Celery worker>` Distributer: Orchestrate jobs
- `<Celery worker>` Harvester: harvest article contents from news sites
- `<Celery worker>` Extractor: extract keywords from articles
- `<Celery worker>` Aggregator: aggregate analyzed data.
- `<RabbitMQ>` Broker: celery message broker.
- `<Redis>` Result Backend: celery task results backend.

### Tasks

- Harvest links: gather article urls from news list html page.
- Distribute chain: Demultiplex news urls to each `harvest and extract` chain tasks.
- Harvest content: gather article text from news article page.
- Extract nouns: extract nouns from news article.
- Aggregate words: aggregate and make `BoW` of articles.

### Workflow

``` txt
harvest_links --> distribute_chain -+
                                    |
+-----------------------------------+
|
+-> {harvest_content -> extract_nouns} -+
+-> {harvest_content -> extract_nouns} -+
:                                       |
                                        |
+---------------------------------------+
|
+-> aggregate_words
```

## Environment

* python `3.6.5`
* apt package dependencies (`apt-pkgs.txt`)
* pip requirements (`requirements.txt`)

## Run

``` sh
# start containers
$ docker-compose up -d
```

### Execute workflow

```
# execute test workflow
$ python main.py
▸ 07:56:02 ERR-INT $ python main.py
✔ Wait for workflow group tasks.. - Done (1 tasks / 2.12s)
✔ Wait for Chain tasks ready.. - Done (10 tasks / 0.00s)
⠙ Wait for Terminal tasks ready.. - {'PENDING': 500}

...

```

### Management ports

- `:15672`: rabbitmq management
- `:5555`: celery flower

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
