#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "docker" --dbname "docker" <<-EOSQL
    CREATE TABLE rules (
      id char(255) UNIQUE NOT NULL,
      unit INT CHECK (unit >= 0),
      logic INT CHECK (logic >= 0),
      temph NUMERIC,
      templ NUMERIC
    );

    CREATE TABLE units (
      id INT UNIQUE NOT NULL,
      unit TEXT
    );

    INSERT INTO units (id, unit) VALUES (0, 'celsius');
    INSERT INTO units (id, unit) VALUES (1, 'farenheit');
EOSQL
