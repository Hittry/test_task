Для запуска api и БД (postgres):
1) cd main
2) docker-compose up -d

Приложение развернется автоматически. При изменение параметров подключение - менять postgres.env и const в сервис провайдере.

Добавлен swagger, доступен после развертывания с endpoint - /api/doc/. Endpoint для запросов - /task.

Запустить скрипт можно:
./script_version.py -d 4 -N 5000

Флаг -d: глубина вложенности json файлов;

Флаг -N: число запросов в БД.