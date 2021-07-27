FROM python:3.9.6

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

EXPOSE 5698
CMD ["python", "code/main.py"]