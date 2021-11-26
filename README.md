# [WIP] rss-tg-bot
Bot which allows using Telegram as RSS reader

# :dog:	 This is a pet-project
And here I use some tools which are new for me. So don't expect much from it.
It is being developed in a spare time to see if Telegram could be used as a 
suitable (for me) replacement for RSS reader apps. It might lack some tests,
architecture patterns, and any other state-of-the-art programming stuff.

# Getting started

Install [docker](https://www.docker.com/) and 
[docker-compose](https://docs.docker.com/compose/). Then clone the repo and 
`cd` to the project directory.

**RSS Aggregator**
```shell
cd rss-reader
docker-compose up --build
```
This will build and start RSS aggregator and related API. Visit 
http://localhost:8080/docs for interactive API documentation.

**Dashboard**
```shell
cd dashboard
npm start
```

**Run tests**
```shell
cd rss-reader
docker-compose -f docker-compose.test.yml -p ci up -d --build
docker logs ci_rss_api_1
```
