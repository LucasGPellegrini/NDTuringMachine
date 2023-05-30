import copy

class DescricaoInstantanea:

    def __init__(self, cabeca_leitura, cadeia, estado, instrucao, passo):
        self.cabeca_leitura = copy.deepcopy(cabeca_leitura)
        self.cadeia = copy.deepcopy(cadeia)
        self.estado = copy.deepcopy(estado)
        self.passo = copy.deepcopy(passo)
        self.instrucao = copy.deepcopy(instrucao)

        estado_prox, acao, direcao = instrucao
        # Aplica a transicao
        self.cadeia[self.cabeca_leitura] = acao
        if direcao == ">":
            self.cabeca_leitura += 1
        elif direcao == "<":
            self.cabeca_leitura -= 1
        self.estado = estado_prox
