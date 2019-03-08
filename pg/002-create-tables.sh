#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "docker" --dbname "docker" <<-EOSQL
    CREATE TABLE rules (
      id char(255) UNIQUE NOT NULL,
      scale INT CHECK (scale >= 0),
      logic INT CHECK (logic >= 0)
    );

    CREATE TABLE scale (
      id INT UNIQUE NOT NULL,
      unit TEXT
    );

    INSERT INTO scale (id, unit) VALUES (1, 'celsius');
    INSERT INTO scale (id, unit) VALUES (2, 'farenheit');
EOSQL
