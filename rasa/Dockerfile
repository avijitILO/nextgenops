FROM rasa/rasa:3.6.0

WORKDIR /app

COPY . .

USER root
RUN pip install --no-cache-dir -r requirements.txt

USER 1001

EXPOSE 5005

CMD ["run", "--enable-api", "--cors", "*", "--host", "0.0.0.0"]
