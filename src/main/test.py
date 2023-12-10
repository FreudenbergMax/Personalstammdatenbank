from datetime import datetime
from datetime import timedelta

date_daten = '01.01.2024'
date_daten = datetime.strptime(date_daten, '%d.%m.%Y').date()

tag_abziehen = timedelta(1)

letzter_tag_alter_eintrag = date_daten - tag_abziehen

date_daten = date_daten
print(type(date_daten))
print(date_daten)
print(type(letzter_tag_alter_eintrag))
print(letzter_tag_alter_eintrag)
