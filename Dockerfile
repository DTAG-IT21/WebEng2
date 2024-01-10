FROM python:3.12
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY src src

ENV DB_DATABASE=assets
ENV DB_HOST=localhost
ENV DB_PASSWORD=postgres
ENV DB_PORT=5432
ENV DB_USERNAME=postgres
ENV KEYCLOAK_HOST=localhost:8080
ENV KEYCLOAK_REALM=biletado
ENV PYTHONUNBUFFERED=1

CMD [ "python","-m", "src.main.main" ]