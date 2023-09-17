# Installation

1. Activate a virtual environment.
```
source <path_to_venv>/bin/activate
```
2. Install the dependencies in it using the following commands
```
pip install -r requirements.txt
pip install django-redis
pip install 'celery[redis]'
```
3. To apply the db migrations, run the following
```
python manage.py makemigrations analytics_service
python manage.py migrate
```

# Running the application locally
1. Start the docker engine
2. Run the redis server
```
docker run -d -p 6379:6379 redis
```
3. Run the RabbitMQ message broker
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```
4. Run the celery worker
```
celery -A social_media_analytics worker --loglevel=info
```
5. Run the app
```
python manage.py runserver
```

# Architecture
There are three main components of the application. These are as follows:
1. An API server
2. Redis (for cache)
3. Celery (task queue)

## Flow



# Endpoints
##  1. Post Creation
```
POST /api/v1/posts
{
    "content": "Hello world. What's up"
}
```

Response
```
{
    "id": "880011c4-7291-43fe-98ea-7b7a7c99bc3c",
    "content": "Hello world. What's up"
}
```

## 2. Post Analysis
```
GET /api/v1/posts/880011c4-7291-43fe-98ea-7b7a7c99bc3c/analysis
```

Response
```
{
    "word_count": 4,
    "average_word_length": 4.75
}
```