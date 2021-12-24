FROM ubuntu:20.04
COPY . .
RUN apt-get update
RUN apt-get install -y  \
            python3     \
            pip
RUN pip install -r requirements.txt
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ENTRYPOINT ["python3", "main.py"]
CMD ["bash"]
