from utils.conversions import Conversions

class Column:
    def __init__(self, name, data_type, not_null, pk=None, compound_pk=None):
        self.name = name
        self.data_type = data_type
        self.not_null = not_null
        self.pk = pk
        self.compound_pk = compound_pk

    def set_as_pk(self):
        self.pk = True

    def __str__(self):
        nl = "\n"
        res = ""
        if not self.compound_pk:
            if self.pk :
                res += f"    @Id{nl}"
            if self.not_null:
                res += f"    @NotNull{nl}"
        return res + f'    @Column(name = "{self.name}"){nl}    private {self.data_type} {Conversions.snake_to_camel(self.name)};{nl}'
