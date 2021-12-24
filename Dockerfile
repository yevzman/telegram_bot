FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y  \
            python3     \
            pip
RUN pip install pyTelegramBotAPI
ARG TOKEN
ENV TELEGRAM_BOT_TOKEN=$TOKEN
COPY . .
ENTRYPOINT ["python3", "main.py"]
CMD ["bash"]
