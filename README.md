Backend для службы обмена короткими сообщениями

docker compose -p tweets_main -f docker-compose.yml up -d --build

docker compose -p tweets_test -f docker-compose.test.yml up -d --build