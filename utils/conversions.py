import re

class Conversions:
    
    def snake_to_camel(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    def convert_type (sql_type):
        sql_type_to_java = {
            'int': 'Integer',
            'bigint': 'Long',
            'smallint': 'Short',
            'numeric': 'Float',
            'decimal': 'Float',
            'real': 'Float',
            'double precision': 'Double',
            'char': 'String',
            'varchar': 'String',
            'character': 'String',
            'text': 'String',
            'bool': 'Boolean',
            'boolean': 'Boolean',
            'date': 'LocalDate',
            'time': 'LocalDateTime',
            'timestamp': 'LocalDateTime',
            'interval': 'Duration',
            'uuid': 'UUID',
        }

        sql_type = re.match(r'^\s*([a-zA-Z]+)', sql_type).group(1)

        if sql_type.lower() in sql_type_to_java:
            return sql_type_to_java[sql_type.lower()]
        else:
            return None  # Tipo de SQL no reconocido
