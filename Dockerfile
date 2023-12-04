FROM python:3.12
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY src src

CMD [ "python", "src/main/main.py" ]