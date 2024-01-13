# Fragebogen zum Programmentwurf Webengineering 2 DHBW Karlsruhe TINF21B3

## Gruppeninformationen

Gruppenname: DTAG-IT21

Gruppenteilnehmer:

- Leon Richter
- Nico Merkel

## Quellcode

Links zu den Versionskontrollendpunkten:

- https://github.com/DTAG-IT21/WebEng2

## Lizenz

Siehe [LICENSE](LICENSE)

## Sprache und Framework

| Frage                                 | Beispiel                                           | Antwort                                               |
|---------------------------------------|----------------------------------------------------|-------------------------------------------------------|
| Programmiersprache                    | go                                                 | Python                                                |
| Sprachversion                         | 1.17                                               | 3.10                                                  |
| Version ist aktuell und wird gepflegt | [X]                                                | [X]                                                   |
| Framework (FW)                        | "gin-gonic" oder "stdlib"                          | Flask                                                 |
| FW-Version                            | v1.8.1                                             | 3.0.0                                                 |
| FW-Version ist aktuell                | [X]                                                | [X]                                                   |
| Website zum FW                        | [gin-gonic](https://gin-gonic.com)                 | [Flask](https://flask.palletsprojects.com/en/3.0.x/)  |
| Prepared statements/ORM               | "doctrine", "FW-Integriert", "prepared statements" | ORM-FW (SQLAlchemy)                                   |
| ORM Version                           | 2.13                                               | 2.0                                                   |
| ORM Version ist aktuell               | [X]                                                | [X]                                                   |
| Website zum ORM                       | [doctrine-orm](https://www.doctrine-project.org/)  | [SQLAlchemy](https://www.sqlalchemy.org/)             | 

## Automatisierung

Art der Automatisierung: GitHub Actions (siehe [deploy-image.yml](.github/workflows/deploy-image.yml))

## Testautomatisierung

* Die CI Pipeline verwendet einen Linter zur Überprüfung des Codes, 
bevor das Docker Image gebaut wird (verwendeter Linter: [Ruff](https://github.com/astral-sh/ruff)).
* Die Ergebnisse können in der Workflow-Zusammenfassung des GitHub-Actions Tabs im Repo eingesehen werden.

## Authentifizierung

* JWT wird berücksichtigt: [ ]
* Signatur wird geprüft: [ ]

Ein erster Ansatz zur Signaturprüfung ist im Code enthalten, 
jedoch wird kein Gebrauch davon gemacht, da er nicht funktioniert.

## Konfiguration und Dokumentation

* Dokumentation existiert in bedarfsgerechtem Umfang: [X]
* Konfigurationsparameter sind sinnvoll gewählt: [X]
* keine hardcoded Zugänge zu angeschlossenenen Systemen (URLs, Passwörter, Datenbanknamen, etc.): [X]
* Umgebungsvariablen und Konfurationsdateien sind gelistet und beschrieben: [X]

## Logging
* Logsystem des Frameworks oder Bibliothek wurde genutzt: [X]
* Logs enthalten alle geforderten Werte: [ ]
* LogLevel ist konfigurierbar: [X]

Für den LogLevel gibt es die standardmäßigen fünf Stufen (DEBUG, INFO, WARNING, ERROR, CRITICAL).  
Umgesetzt wurden hauptsächlich nur DEBUG und INFO.
* INFO: Bei jedem Request werden Zeitstempel, Methodenaufruf und Response Code geloggt
* DEBUG: Es werden auch zusätzlich der Request- (falls vorhanden) und Response-Body geloggt.