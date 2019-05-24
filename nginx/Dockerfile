FROM nginx:1.15.5-alpine

COPY ./config/nginx.conf /etc/nginx/nginx.conf

#RUN mkdir -p /etc/nginx/sites-available

COPY ./config/restaurant.conf /etc/nginx/sites-available/
COPY ./config/uwsgi_params /etc/nginx/uwsgi_params
COPY ./config/nginx.service /lib/systemd/system/nginx/nginx.service


RUN mkdir -p /etc/nginx/sites-enabled/ \
    && ln -s /etc/nginx/sites-available/restaurant.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]