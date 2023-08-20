from utils.conversions import Conversions
from models.compound_key import Compound_key


class Table:
    def __init__(self, package, table_name, columns, pks, compound_key=None):
        self.package = package.split("src/main/java/")[1].replace("/",".")
        if len(pks) > 1:
            cpks_columns = [c for c in columns if c.name in pks]
            compound_key = Compound_key(self.package,table_name, cpks_columns)
        self.table_name = table_name
        self.columns = columns
        self.pks = pks
        self.compound_key = compound_key

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
    def __str__(self):
        nl = "\n"
        cpk = f"""{nl}    @EmbeddedId{nl}    private {self.camel_case_name().capitalize()}PK {self.camel_case_name()};{nl}""" if self.compound_key else ""
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
public class {self.camel_case_name().capitalize()}MO {{
{cpk}
{nl.join([str(column) for column in self.columns])}
}}
"""
