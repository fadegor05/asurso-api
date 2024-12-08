## Пример

```shell
# Создание клиента из данных аккаунта для Самарской Области
client = ASURSOClient.from_account_data("Login", "Password", region=Region.SAM)
client.init()

# Информация об ученике
print(client.student)

# Контекстная информация
print(client.context)

# Дневник, по умолчанию на текущую неделю, можно передать date, и покажется неделя с ним
diary = client.get_diary(date)
print(diary)
```