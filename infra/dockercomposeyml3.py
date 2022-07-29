version: '3.3'

services:

  db:
    image: postgres:13-alpine
    volumes:
      - /var/lib/postgresql/data/
    env_file:
      - ./.env

  backend:
    image: mistpy/foodgram_project_react:v1.1
    expose:
      - 8000
    restart: always
    volumes:
      - static_value:/app/backend_static/
      - media_value:/app/backend_media/
    depends_on:
      - db
    env_file:
      - ./.env

  frontend:
    image: mistpy/foodgram_project_react:v1.1
    volumes:
      - ../frontend/:/app/result_build/
    depends_on:
      - backend

  nginx:
    image: nginx:1.19.3
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_value:/app/backend_static/
      - media_value:/app/backend_media/
      - ../frontend/build:/usr/share/nginx/html/
      - ../docs:/usr/share/nginx/html/api/docs/
    restart: always
    depends_on:
      - frontend

volumes:
  db:
  #postgres_data:
  static_value:
  media_value:
