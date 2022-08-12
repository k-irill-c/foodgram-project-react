
version: '3.3'
services:
  db:
    image: postgres:13.0-alpine

    volumes:
      - db:/var/lib/postgresql/data/
    #environment:
      #- POSTGRES_PASSWORD=postgres
    env_file:
      - ./.env
  # Примеры наполнения файла .env представлены в README и .env.template

  web:
    build:
      context: ../backend
    restart: always
    volumes:
      - backend_static:/app/backend_static/
      - backend_media:/app/backend_media/
    depends_on:
      - db
    env_file:
      - ./.env

  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    volumes:
      - ../frontend/:/app/result_build/
  nginx:
    image: nginx:1.19.3
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ../frontend/build:/usr/share/nginx/html/
      - ../docs/:/usr/share/nginx/html/api/docs/
      - backend_static:/usr/share/nginx/html/backend_static/:ro
      - media_value:/usr/share/nginx/html/backend_media/:ro


volumes:
  db:
  backend_static:
  backend_media:

