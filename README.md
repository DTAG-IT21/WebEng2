# Web Engineering 2 TINF21B3
## Team DTAG-IT21 (Leon Richter und Nico Merkel)

Dieses Projekt beinhaltet einen Python-Flask REST-Service für ein Gebäude-Verwaltungssystem, welcher in eine gegebene Kubernetes Kustomization Umgebung
eingefügt werden kann.
### Container Image
Das Container-Image kann mit folgendem Befehl gepullt werden:
~~~commandline
docker pull ghcr.io/dtag-it21/webeng2:main
~~~
Um eigene Dienste (Datenbank, Keycloak) oder das Log-Level zu konfigurieren, 
stehen folgende Umgebungsvariablen zur Verfügung:

| Name                     | Beschreibung                                              | Default  |
|--------------------------|-----------------------------------------------------------|----------|
| POSTGRES_ASSETS_USER     | User für die Postgres Datenbank  	                        | postgres |
| POSTGRES_ASSETS_PASSWORD | Passwort für die Postgres Datenbank  	                    | postgres |
| POSTGRES_ASSETS_DBNAME   | Name der Postgres Datenbank  	                            | assets   |
| POSTGRES_ASSETS_HOST     | Host der Postgres Datenbank  	                            | postgres |
| POSTGRES_ASSETS_PORT     | Port der Postgres Datenbank  	                            | 5432     |
| KEYCLOAK_HOST            | Host für die Keycloak Instanz    	                        | keycloak |
| KEYCLOAK_REALM           | Realm der Keycloak Instanz   	                            | biletado |
| LOGLEVEL                 | Log-Level der API (DEBUG, INFO, WARNING, ERROR, CRITICAL) | INFO     |

Das Log-Level kann zusätzlich über /api/v2/assets/log/&lt;string:level> zur Laufzeit angepasst werden.
Die Flask API innerhalb des Containers ist über Port 9000 erreichbar.