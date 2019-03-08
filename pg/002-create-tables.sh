#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "docker" --dbname "docker" <<-EOSQL
    CREATE TABLE "rules" (
      id char UNIQUE,
        scale INT CHECK (scale >= 0),
        logic INT CHECK (logic >= 0)
    );

    CREATE TABLE "scale" (
      "id" INT,
      "unit" TEXT
    );

    INSERT INTO scale (id, unit) VALUES (1, 'celsius');
    INSERT INTO scale (id, unit) VALUES (1, 'farenheit');
EOSQL
