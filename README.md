# ASURSO-API

**Проект находиться в глубокой разработке**

## Пример

```shell
from asurso_api import ASURSOClient
from asurso_api.auth import AuthPlaceData

# Данные о входе для вашей школы
place = AuthPlaceData(country_id=2, region_id=1, region_area_id=-1, city_id=1, school_type_id=2, school_id=2436)

# Создание клиента из данных аккаунта для Самарской Области
client = ASURSOClient.from_account_data("Login", "Password", place, region=Region.SAM)
client.init()

# Информация об ученике
print(client.student)

# Контекстная информация
print(client.context)

# Дневник, по умолчанию на текущую неделю, можно передать date, и покажется неделя с ним
diary = client.get_diary(date)
print(diary)
```

Спасибо [VityaSchel](https://github.com/VityaSchel), в разработке участвовали его
наработки [обертки АСУ РСО на JavaScript](https://github.com/VityaSchel/asurso)
