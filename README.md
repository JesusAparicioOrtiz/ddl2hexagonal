# ddl2hexagonal

https://github.com/JesusAparicioOrtiz/ddl2hexagonal

## 📖 Introduction

Script to create entities and mappers in java for a hexagonal architecture based on a given DDL

## 🤖 Requirements

- Python 3.9.6 or higher, you can download it from the following link (https://www.python.org/downloads/)

## 🚀 Start up

Run the script by running ```python main.py```
After that, the script will ask for two values:
* ```DDL path```: Path where the DDL to convert is located
* ```Project DB models path```: Path of the project where the DB models are going to be created

## DDL valid structure example

```
CREATE TABLE table_name (
    table_id         int4    NOT NULL,
    second_table_id  int8    NOT NULL,
    executor         varchar NULL,
    name             varchar NULL,
    is_favourite     bool    NULL,
    CONSTRAINT table_name_pk PRIMARY KEY (table_id, second_table_id),
    CONSTRAINT table_name_fk foreign key (second_table_id) references second_table (second_table_id)
);
```
## ⚙ Troublehooting

Here are some tips in case you have any errors during the execution of the script:
* Try to define columns and constraints in a single line each one, without taking up more than one line