FROM nginx:latest

COPY infra/dev/nginx/nginx.conf /etc/nginx/
COPY infra/dev/nginx/nginx-app.conf /etc/nginx/sites-enabled/
COPY photocard_market/staticfiles /staticfiles
CMD ["nginx", "-g", "daemon off;"]