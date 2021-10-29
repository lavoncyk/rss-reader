import React from "react";

class App extends React.Component {
  render() {

    const postsData = [
      {
        "id": 1331,
        "rss_feed_id": 3,
        "title": "Берлин: невсратый гайд",
        "url": "https://vas3k.club/guide/berlin/",
        "published_at": "2021-09-20T22:05:35"
      },
      {
        "id": 1332,
        "rss_feed_id": 3,
        "title": "Как мы в Черногории затусили с бездомным в разгар пандемии",
        "url": "https://vas3k.ru/world/montenegro/",
        "published_at": "2021-07-21T06:00:00"
      },
      {
        "id": 1333,
        "rss_feed_id": 3,
        "title": "Вастрик.Бус: Work in Progress",
        "url": "https://vas3k.ru/notes/bus_wip/",
        "published_at": "2021-06-30T13:22:58"
      },
      {
        "id": 1334,
        "rss_feed_id": 3,
        "title": "Латекс [NSFW]",
        "url": "https://vas3k.ru/notes/latex/",
        "published_at": "2021-04-01T03:00:31"
      },
      {
        "id": 1335,
        "rss_feed_id": 3,
        "title": "Бекстейдж: квантовые компьютеры",
        "url": "https://vas3k.ru/notes/quantum_backstage/",
        "published_at": "2021-03-22T12:00:52"
      },
      {
        "id": 1336,
        "rss_feed_id": 3,
        "title": "Квантовый Компьютер",
        "url": "https://vas3k.ru/blog/quantum_computing/",
        "published_at": "2021-03-16T08:00:00"
      },
      {
        "id": 1337,
        "rss_feed_id": 3,
        "title": "Итоги Года 2̶0̶2̶0̶",
        "url": "https://vas3k.ru/blog/2020/",
        "published_at": "2020-12-23T07:00:05"
      },
      {
        "id": 1338,
        "rss_feed_id": 3,
        "title": "Вастрик.Бус",
        "url": "https://vas3k.ru/blog/bus/",
        "published_at": "2020-11-03T06:00:00"
      },
      {
        "id": 1339,
        "rss_feed_id": 3,
        "title": "Цифровой модернизм, постмодернизм и метамодернизм",
        "url": "https://vas3k.ru/notes/metamodern/",
        "published_at": "2020-10-12T04:00:37"
      },
      {
        "id": 1340,
        "rss_feed_id": 3,
        "title": "Очарованные циферками",
        "url": "https://vas3k.ru/notes/datadriven/",
        "published_at": "2020-09-29T07:16:38"
      },
      {
        "id": 1341,
        "rss_feed_id": 3,
        "title": "Права",
        "url": "https://vas3k.ru/notes/got_a_loicense/",
        "published_at": "2020-08-10T07:30:45"
      },
      {
        "id": 1342,
        "rss_feed_id": 3,
        "title": "А как делать блог?",
        "url": "https://vas3k.ru/notes/how_to_blog/",
        "published_at": "2020-07-31T17:09:52"
      },
      {
        "id": 1343,
        "rss_feed_id": 3,
        "title": "Путь в облака",
        "url": "https://vas3k.ru/notes/clouds/",
        "published_at": "2020-06-28T20:53:25"
      },
      {
        "id": 1344,
        "rss_feed_id": 3,
        "title": "No Code",
        "url": "https://vas3k.ru/blog/nocode/",
        "published_at": "2020-05-20T06:00:00"
      },
      {
        "id": 1345,
        "rss_feed_id": 3,
        "title": "Супераппы и пессимистический период технологий",
        "url": "https://vas3k.ru/notes/tech_pessimism/",
        "published_at": "2020-04-12T19:13:57"
      },
      {
        "id": 1346,
        "rss_feed_id": 3,
        "title": "К — Команда",
        "url": "https://vas3k.ru/blog/team/",
        "published_at": "2020-03-24T08:00:00"
      },
      {
        "id": 1347,
        "rss_feed_id": 3,
        "title": "Оставайся посередине",
        "url": "https://vas3k.ru/notes/in_the_middle/",
        "published_at": "2020-03-09T05:00:00"
      },
      {
        "id": 1348,
        "rss_feed_id": 3,
        "title": "Дополненная Реальность",
        "url": "https://vas3k.ru/blog/augmented_reality/",
        "published_at": "2020-02-18T04:00:00"
      },
      {
        "id": 1349,
        "rss_feed_id": 3,
        "title": "Психотерапия",
        "url": "https://vas3k.ru/notes/therapy/",
        "published_at": "2020-01-29T20:48:21"
      },
      {
        "id": 1350,
        "rss_feed_id": 3,
        "title": "Никосия",
        "url": "https://vas3k.ru/world/nicosia/",
        "published_at": "2020-01-21T07:00:00"
      },
      {
        "id": 1351,
        "rss_feed_id": 3,
        "title": "Анонс Infomate.club",
        "url": "https://vas3k.ru/notes/infomate/",
        "published_at": "2020-01-12T14:00:00"
      },
      {
        "id": 1352,
        "rss_feed_id": 3,
        "title": "Итоги Года 2019",
        "url": "https://vas3k.ru/blog/2019/",
        "published_at": "2019-12-22T09:00:00"
      },
      {
        "id": 1353,
        "rss_feed_id": 3,
        "title": "300кк/сек",
        "url": "https://vas3k.ru/notes/300k/",
        "published_at": "2019-11-28T16:22:12"
      },
      {
        "id": 1354,
        "rss_feed_id": 3,
        "title": "Берлинское Айти",
        "url": "https://vas3k.ru/notes/berlin_it/",
        "published_at": "2019-11-20T09:00:00"
      },
      {
        "id": 1355,
        "rss_feed_id": 3,
        "title": "Как работает Wi-Fi в самолете над атлантикой?",
        "url": "https://vas3k.ru/notes/plane_wifi/",
        "published_at": "2019-11-17T01:48:31"
      },
      {
        "id": 1356,
        "rss_feed_id": 3,
        "title": "Руин бары Будапешта",
        "url": "https://vas3k.ru/world/ruin_pubs/",
        "published_at": "2019-11-04T08:00:00"
      },
      {
        "id": 1357,
        "rss_feed_id": 3,
        "title": "Перешагнуть критическую точку",
        "url": "https://vas3k.ru/notes/the_club/",
        "published_at": "2019-10-20T13:48:14"
      },
      {
        "id": 1358,
        "rss_feed_id": 3,
        "title": "Вастрик.Инсайд: последний выпуск",
        "url": "https://vas3k.ru/inside/49/",
        "published_at": "2019-09-23T17:50:49"
      },
      {
        "id": 1359,
        "rss_feed_id": 3,
        "title": "Вастрик.Инсайд #49: Последний выпуск",
        "url": "https://vas3k.ru/inside/49/",
        "published_at": "2019-09-23T08:06:23"
      },
      {
        "id": 1360,
        "rss_feed_id": 3,
        "title": "Пробую альтернативы популярных продуктов",
        "url": "https://vas3k.ru/inside/48/alternatives/",
        "published_at": "2019-08-13T17:50:49"
      },
    ]
    const feedData = {
      "name": "Vas3k",
      "url": "https://vas3k.ru/rss/",
      "id": 3,
      "parsed_at": "2021-10-28T14:11:03",
      "modified_at": "2021-09-20T22:05:35",
      "etag": null,
      "created_at": "2021-10-09T07:35:49"
    }

    return (
      <div className="App">
      </div>
    )
  }
}

export default App