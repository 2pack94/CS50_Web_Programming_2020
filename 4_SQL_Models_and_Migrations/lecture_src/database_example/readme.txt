open database:
$ sqlite3 flights.sqlite3

list all tables:
sqlite> .tables

enable pretty printing when outputting tables:
sqlite> .headers on
sqlite> .mode columns

import SQL:
sqlite> .read flights.sql

export SQL:
sqlite> .output flights.sql
sqlite> .dump

write database to file:
sqlite> .save flights.sqlite3

exit CLI:
sqlite> .exit
