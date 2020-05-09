# Discord Bot "TrablCoinMaster"
=====================
## Designed for the discord server "TroubleHome"
-----------------------------------
#### The bot implements the management and storage of "troublecoin" currency.

> Each user has an active "coin" balance and an account to earn all the time.
> Users can make their own coins transfers to each other.
>
> Only the user with the access role can make changes to the account (depositing or withdrawing from the account).

For data storage the "Postgres SQL" database is used.

Название файла  		| Содержание файла
------------------------|----------------------
main.py       			| Основной модуль содержащий инициализацию бота, его комманды и события
sql_fun.py      		| Модуль для работы с базой данных (PostgressSQL)
access_verification   	| Модуль с функциями для проверки доступа к командам бота
