from utils.conversions import Conversions

class Compound_key:
    def __init__(self, package, table_name, columns):
        self.package = package
        self.table_name = table_name
        self.columns = columns

    def camel_case_name(self):
        return Conversions.snake_to_camel(self.table_name)

    def __str__(self):
        nl = '\n'
        return f"""package {self.package}{self.camel_case_name()}.pk;

import lombok.*;
import javax.persistence.*;
import java.io.Serializable;

@Embeddable
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {self.camel_case_name().capitalize()}PK implements Serializable {{
{nl+nl.join([str(column) for column in self.columns])}
}}
"""