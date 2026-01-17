# Базовый образ Nginx Alpine (легковесный)
FROM nginx:alpine

# Если context = . (корень репозитория):
COPY nginx/nginx-main.conf /etc/nginx/nginx.conf
COPY nginx/site.conf /etc/nginx/conf.d/default.conf

# Копируем статику Frontend
COPY frontend /usr/share/nginx/html

# Создаём директории для Certbot (чтобы Nginx не ругался при старте)
RUN mkdir -p /var/www/certbot

# Открываем порты
EXPOSE 80 443

# Запуск Nginx
CMD ["nginx", "-g", "daemon off;"]