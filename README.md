# mlops_hw1_wine

## Методы

- delete_model - по выбранном id модели можно её удалить
- fit - создать и обучить модель по загруженным данным
- model_types_available - посмотреть, какие типы моделей можно обучать
- predict - сделать предсказание по загруженным данным в виде файла
- saved_models_list - посмотреть список сохранённых моделей

## Docker
Создать docker image
- Зайти в директорию проекта
- забилдить образ

docker build -t wineestimatorimage .

- Посмотреть, что образ был создан

docker images
<none> <none> f435a89d615c   About a minute ago   735MB

Запустить приложение с помощью докер компоуз
- Зайти в директорию проекта
- Проверить валидность докер компоуз файла 

docker-compose config

- Запуститб докер компоуз

docker-compose up -d

- Остановить все процессы

docker-compose down
