FROM python:3.11-buster
WORKDIR /app
RUN pip install pdm
COPY . /app
RUN pdm sync
EXPOSE 8000
CMD ["pdm", "start"]
