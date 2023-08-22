from utils.conversions import Conversions
from models.compound_key import Compound_key


class Table:
    def __init__(self, package, table_name, columns, pks, mtofks, otmfks):
        self.package = package.split("src/main/java/")[1].replace("/",".")
        self.compound_key = None
        if len(pks) > 1:
            cpks_columns = [c for c in columns if c.name in pks]
            self.compound_key = Compound_key(self.package,table_name, cpks_columns)
        self.table_name = table_name
        self.columns = columns
        self.pks = pks
        self.mtofks = mtofks
        self.otmfks = otmfks

    def camel_case_table_name(self):
        return Conversions.snake_to_camel(self.table_name)
    
    def add_models_imports(self):
        model_imports = ""
        for table in [mto[0] for mto in self.mtofks] + self.otmfks:
            table_snake_case = Conversions.snake_to_camel(table)
            model_imports += f"""import {self.package}{table_snake_case}.{table_snake_case.capitalize()}MO;\n"""
        return model_imports
    
    def add_extra_imports(self):
        imports_dict = {
            "List": "import java.util.List;\n",
            "Timestamp" : "import java.sql.Timestamp;\n",
            "LocalDate": "import java.time.LocalDate;\n"
        }
        imports = ""
        for c in self.columns:
            if c.data_type in imports_dict and imports_dict[c.data_type] not in imports:
                imports += imports_dict.get(c.data_type)
        if "List" not in imports and len(self.otmfks) > 0:
            imports += "import java.util.List;\n"
        return imports
    
    def join_column_definition(self,fk,referenced_column):
        return f"""@JoinColumn(name = "{fk}",  referencedColumnName = "{referenced_column}", insertable = false, updatable = false)"""
    
    def one_to_many_definition(self,referenced_table):
        return f"""private List<{Conversions.snake_to_camel(referenced_table).capitalize()}MO> {Conversions.snake_to_camel(referenced_table)}MO;"""

    def add_many_to_one_definitions(self):
        res = ""
        many_to_one_tag = "@ManyToOne(fetch = FetchType.LAZY)"
        for t in self.mtofks:
            table_referenced = t[0]
            fks = t[1]
            referenced_columns = t[2]
            attribute = f"""private {Conversions.snake_to_camel(table_referenced).capitalize()}MO {Conversions.snake_to_camel(table_referenced)}MO;\n\n"""
            if len(fks) > 1:
                res += f"""    {many_to_one_tag}\n    @JoinColumns(\u007b\n"""
                for i in range(len(fks)):
                    res += "        " + (self.join_column_definition(fks[i],referenced_columns[i]))
                    if i < len(fks) - 1:
                        res += ",\n"
                res += f"""    \n    \u007d)\n    {attribute}"""
            elif len(fks) == 1:
                res += f"""    {many_to_one_tag}\n    {self.join_column_definition(fks[0],referenced_columns[0])}\n    {attribute}"""
        return res
    
    def add_one_to_many_definitions(self):
        res = ""
        one_to_many_tag = f"""    @OneToMany(mappedBy = "{self.camel_case_table_name()}MO", fetch = FetchType.LAZY)"""
        for t in self.otmfks:
            res += f"""{one_to_many_tag}\n    {self.one_to_many_definition(t)}\n\n"""
        return res
    
    def __str__(self):
        nl = "\n"
        cpk = f"""\n    @EmbeddedId\n    private {self.camel_case_table_name().capitalize()}PK {self.camel_case_table_name()};\n""" if self.compound_key else ""
        cpk_import = f"""import {self.package}{self.camel_case_table_name()}.pk.{self.camel_case_table_name().capitalize()}PK;""" if cpk else ""
        return f"""package {self.package}{self.camel_case_table_name()};

{cpk_import}
{self.add_models_imports()}

import lombok.*;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
{self.add_extra_imports()}

@Entity
@Table(name = "{self.table_name}")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class {self.camel_case_table_name().capitalize()}MO \u007b
{cpk}
{nl.join([str(column) for column in self.columns])}

{self.add_many_to_one_definitions()}{self.add_one_to_many_definitions()}
\u007d
"""
