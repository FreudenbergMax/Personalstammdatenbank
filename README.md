Sehr geehrter Herr Prof. Dr.-Ing. Claßen,
sehr geehrter Herr Prof. Dr. Kempa,

dies ist das für die im Rahmen der Abschlussarbeit "Entwicklung einer Personalstammdatenbank als SaaS" entwickelte System. Damit die Tests durchlaufen können, erstellen Sie bitte eine postgres-Datenbank mit folgenden Daten:

host: "localhost"
Bezeichnung Datenbank: "Personalstammdatenbank"
user: "postgres"
Passwort: "@Postgres123"
port: 5432

Ich habe die Datenbank über DBeaver entwickelt. Bei der Erstellung wurde auch unverzüglich das Schema "public" erstellt, auf der die Produktiv-Datenbank laufen soll. 
Sobald die Datenbank erstellt ist, müssten die Tests durchgeführt werden können. Die Tests laufen auf einem Testschema mit der Bezeichnung "temp_test_schema". Es ist somit nicht notwendig, 
auf dem Schema "public" die Datenbank, die Stored Procedures und die Rolle "tenant_user" zu erzeugen. Dies wird durch die setUp-Funktion für das Schema "temp_test_schema" übernommen. 
Falls sie im Schema "public" die Datenbank, die stored Procedures und die Rolle "tenant_user" bereits erzeugt, sollten ebenfalls keine Probleme beim Durchlauf der Tests im Schema "temp_test_schema" entstehen.

Ich bitte um Entschuldigung für die Umstände, die ich Ihnen bereite.

Mit freundlichen Grüßen,
Max Freudenberg
