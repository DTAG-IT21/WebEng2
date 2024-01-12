FROM python:3.12
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY src src

ENV POSTGRES_ASSETS_USER: postgres
ENV POSTGRES_ASSETS_PASSWORD: postgres
ENV POSTGRES_ASSETS_DBNAME: assets
ENV POSTGRES_ASSETS_HOST: postgres
ENV POSTGRES_ASSETS_PORT: 5432
ENV KEYCLOAK_HOST=localhost:8080
ENV KEYCLOAK_REALM=biletado
ENV PYTHONUNBUFFERED=1

CMD [ "python","-m", "src.main.main" ]