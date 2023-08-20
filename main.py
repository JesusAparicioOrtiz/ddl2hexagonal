import os
from models.table import Table
from models.column import Column
from utils.conversions import Conversions

def create_models(db_models_dir, table_definitions):
    for table_name, columns, pks in table_definitions:
        table = Table(db_models_dir,table_name,columns,pks)
        table_camel_case_name = table.camel_case_name()
        if len(pks) > 1:
            if not os.path.exists(f'{db_models_dir}{table_camel_case_name}/pk'):
                os.makedirs(f'{db_models_dir}{table_camel_case_name}/pk')
            with open(f'{db_models_dir}{table_camel_case_name}/pk/{table_camel_case_name.capitalize()}PK.java', 'w') as f:
                f.write(str(table.compound_key))
        if not os.path.exists(f'{db_models_dir}{table_camel_case_name}'):
            os.makedirs(f'{db_models_dir}{table_camel_case_name}')
        with open(f'{db_models_dir}{table_camel_case_name}/{table_camel_case_name.capitalize()}MO.java', 'w') as f:
            f.write(str(table))

def parse_sql_schema(schema):
    statements = schema.split(';')
    table_definitions = []

    for statement in statements:
        if "CREATE TABLE" in statement:
            lines = statement.strip().split('\n')
            table_name = lines[0].split()[2]
            columns = []
            pks = []
            for line in lines[1:]:
                if line.strip() == "(":
                    pass
                elif line.strip() == ")":
                    break
                elif "CONSTRAINT" in line and "PRIMARY KEY" in line:
                    pks = line.split("PRIMARY KEY (")[1].split(")")[0].split(",")
                    for c in columns:
                        if len(pks) == 1:
                            if c.name in pks : c.pk = True
                        else:
                            if c.name in pks : c.compound_pk = True
                elif not "CONSTRAINT"in line:
                    lineParts = line.split()
                    columns.append(Column(lineParts[0].replace('"', ''),Conversions.convert_type(lineParts[1]),lineParts[2] == "NOT"))

            table_definitions.append((table_name, columns, pks))

    return table_definitions

def main():
    ddl_path = input("Enter absolute path to ddl: ")
    db_models_path = input("Enter absolute path to project db models: ")

    if db_models_path[-1] != "/":
        db_models_path += "/"

    with open('../prueba.txt', 'r') as f:
        schema = f.read()

    table_definitions = parse_sql_schema(schema)

    if not os.path.exists(db_models_path):
        os.makedirs(db_models_path)

    create_models(db_models_path, table_definitions)

    print("Java entities created!")

if __name__ == "__main__":
    main()
