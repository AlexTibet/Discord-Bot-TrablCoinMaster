# Discord Bot "TrablCoinMaster"
=====================
## Designed for the discord server "TroubleHome"
-----------------------------------
#### The bot implements the management and storage of "troublecoin" currency.

> Each user has an active "coin" balance and an account to earn all the time.
>
> Users can make their own coins transfers to each other.
>
> Only the user with the access role can make changes to the account (depositing or withdrawing from the account).
>
> Users can won or lost coins in casino (chances settings and descriptions in config.py)
>
For data storage the "Postgres SQL" database is used.

File name  		        | File content
------------------------|----------------------
main.py       			| The main module containing the initialization of the bot, its commands and events
sql_fun.py      		| Module to work with the database (PostgresQL)
access_verification   	| Module with functions for checking access to bot commands
