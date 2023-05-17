import copy

class DescricaoInstantanea:

    def __init__(self, cabeca_leitura, cadeia, estado):
        self.cabeca_leitura = copy.deepcopy(cabeca_leitura)
        self.cadeia = copy.deepcopy(cadeia)
        self.estado = copy.deepcopy(estado)