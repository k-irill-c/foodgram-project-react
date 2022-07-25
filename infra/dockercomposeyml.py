version: '3.3'

services:
  db:
    image: postgres:13-alpine
    volumes:
      - /var/lib/postgresql/data/
    env_file:
      - ./.env
  backend:
    build:
      context: ../backend/
   # image: mistpy/foodgram_project_react:latest
   # expose:
   #   - 8000
    restart: always
    volumes:
      - backend_static:/app/backend_static/
      - media:/app/media/
    depends_on:
      - db
    env_file:
      - ./.env
  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    #image: mistpy/foodgram_project_react:latest
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
      - ../frontend/build:/usr/share/nginx/html/
      - ../docs/:/usr/share/nginx/html/api/docs/
      - backend_static:/app/backend_static/
      - media:/app/media/
    depends_on:
      - frontend

volumes:
  db:
  backend_static:
  media:
