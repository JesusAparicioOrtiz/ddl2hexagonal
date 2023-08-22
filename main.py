import os
from models.table import Table
from models.column import Column
from utils.conversions import Conversions

def create_models(db_models_dir, table_definitions):
    for table_name, columns, pks, mtofks, otmfks in table_definitions:
        table = Table(db_models_dir, table_name, columns, pks, mtofks, otmfks)
        table_camel_case_name = table.camel_case_table_name()
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
    otmfks = {}
    for statement in statements:
        statement = statement.lower()
        if "create table" in statement:
            lines = statement.strip().split('\n')
            table_name = lines[0].split()[2]
            columns, pks, mtofks = [], [], []
            for line in lines[1:]:
                if line.strip() == "(":
                    pass
                elif line.strip() == ")":
                    break
                elif "constraint" in line:
                    if "primary key" in line:
                        pks = line.split("primary key (")[1].split(")")[0].split(",")
                        for c in columns:
                            if len(pks) == 1:
                                if c.name in pks : c.pk = True
                            else:
                                if c.name in pks : c.compound_pk = True
                    elif "foreign key"in line:
                        referenced_table = line.split("references ")[1].split()[0]
                        fk = line.split("foreign key (")[1].split(")")[0].split(",")
                        referenced_column = line.split("references ")[1].split("(")[1].split(")")[0].split(",")
                        mtofks.append((referenced_table,fk,referenced_column))
                        if referenced_table not in otmfks:
                            otmfks[referenced_table] = []
                        if table_name not in otmfks[referenced_table]:
                            otmfks[referenced_table].append(table_name)
                elif not "constraint"in line:
                    lineParts = line.split()
                    columns.append(Column(lineParts[0].replace('"', ''),Conversions.convert_type(lineParts[1]),"not null" in line))
            table_definitions.append((table_name, columns, pks, mtofks))

    for idx, (table_name, columns, pks, mtofks) in enumerate(table_definitions):
        table_definition_with_otfmfks = (table_name, columns, pks, mtofks, otmfks.get(table_name, []))
        table_definitions[idx] = table_definition_with_otfmfks

    return table_definitions

def main():
    ddl_path = input("Enter absolute path to ddl: ")
    db_models_path = input("Enter absolute path to project db models: ")

    if db_models_path[-1] != "/":
        db_models_path += "/"

    with open(ddl_path, 'r') as f:
        schema = f.read()

    table_definitions = parse_sql_schema(schema)

    if not os.path.exists(db_models_path):
        os.makedirs(db_models_path)

    create_models(db_models_path, table_definitions)

    print("Java entities created!")

if __name__ == "__main__":
    main()
