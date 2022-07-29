server {
    server_tokens off;
    listen 80;
    server_name 51.250.91.241 yapracticscool.sytes.net;

    location /backend_static/ {
        autoindex on;
        alias /app/backend_static/;
    }
    location /backend_media/ {
        autoindex on;
        alias /app/backend_media/;
    }

    location /api/docs/ {
        root /usr/share/nginx/html;
        try_files $uri $uri/redoc.html;
    }

    location /api/ {
        proxy_set_header        Host $host;
        proxy_set_header        X-Forwarded-Host $host;
        proxy_set_header        X-Forwarded-Server $host;
        proxy_pass http://yapracticscool.sytes.net;
    }

    location /admin/ {
        proxy_pass http://yapracticscool.sytes.net/admin/;
    }

    location / {
        root /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri /index.html;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /var/html/frontend/;
    }
}
