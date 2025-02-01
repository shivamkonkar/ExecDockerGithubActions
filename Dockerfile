FROM python

WORKDIR /app

COPY . .

RUN chmod u+x startup.sh

CMD ["./startup.sh"]