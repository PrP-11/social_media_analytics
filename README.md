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
1. Whenver a user creates a new post, an async celery task is triggered to perform the analysis of the post.
2. Once the analysis is done, it store the data in redis.
3. The analysis endpoint then fetches the cached data and returns it to the user.

### Future Scope
1. For further distributed computations we can break down the analysis tasks into smaller, parallelizable units of work, such as analyzing individual sentences or paragraphs within a post.
2. Implement a message broker (e.g., RabbitMQ or Redis) to distribute analysis tasks to workers.
3. Monitor the task queue and worker performance to ensure efficient processing of analysis tasks.
4. Distribute the workload across multiple servers or containers to horizontally scale your microservice.
5. Implement load balancing to evenly distribute incoming requests to multiple microservice instances.

By implementing these scalability considerations, the analytics microservice can handle large datasets and high request volumes efficiently while reducing computation time through caching and distributing analysis tasks for parallel processing.


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