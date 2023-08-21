from utils.conversions import Conversions
from models.compound_key import Compound_key


class Table:
    def __init__(self, package, table_name, columns, pks, mtofks):
        self.package = package.split("src/main/java/")[1].replace("/",".")
        self.compound_key = None
        if len(pks) > 1:
            cpks_columns = [c for c in columns if c.name in pks]
            self.compound_key = Compound_key(self.package,table_name, cpks_columns)
        self.table_name = table_name
        self.columns = columns
        self.pks = pks
        self.mtofks = mtofks

    def camel_case_name(self):
        return Conversions.snake_to_camel(self.table_name)
    
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
        return imports
    
    def join_column_definition(self,fk,table_referenced_column):
        return f"""@JoinColumn(name = "{fk}",  referencedColumnName = "{table_referenced_column}", insertable = false, updatable = false)"""
    
    def add_fks(self):
        fks_res = ""
        many_to_one_tag = "@ManyToOne(fetch = FetchType.LAZY)"
        for t in self.mtofks:
            table_referenced = t[0]
            fks = t[1]
            table_referenced_columns = t[2]
            attribute = f"""private {Conversions.snake_to_camel(table_referenced).capitalize()}MO {Conversions.snake_to_camel(table_referenced)}MO;\n\n"""
            if len(fks) > 1:
                fks_res += f"""    {many_to_one_tag}\n    @JoinColumns(\u007b\n"""
                for i in range(len(fks)):
                    fks_res += "        " + (self.join_column_definition(fks[i],table_referenced_columns[i]))
                    if i < len(fks) - 1:
                        fks_res += ",\n"
                fks_res += f"""    \n    \u007d)\n    {attribute}"""
            elif len(fks) == 1:
                fks_res += f"""    {many_to_one_tag}\n    {self.join_column_definition(fks[0],table_referenced_columns[0])}\n    {attribute}"""
        return fks_res
    
    def __str__(self):
        nl = "\n"
        cpk = f"""\n    @EmbeddedId\n    private {self.camel_case_name().capitalize()}PK {self.camel_case_name()};\n""" if self.compound_key else ""
        cpk_import = f"""import {self.package}{self.camel_case_name()}.pk.{self.camel_case_name().capitalize()}PK;""" if cpk else ""
        return f"""package {self.package}{self.camel_case_name()};

import lombok.*;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
{self.add_extra_imports()}

{cpk_import}

@Entity
@Table(name = "{self.table_name}")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class {self.camel_case_name().capitalize()}MO \u007b
{cpk}
{nl.join([str(column) for column in self.columns])}

{self.add_fks()}
\u007d
"""
