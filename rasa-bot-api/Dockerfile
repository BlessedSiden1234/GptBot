FROM rasa/rasa:3.6.20
WORKDIR /app
COPY . /app
EXPOSE 8080
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
