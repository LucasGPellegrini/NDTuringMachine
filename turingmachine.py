import os
import sys
from time import sleep

# Constante para limpar terminal (Linux ou Windows)
CLEAR = 'clear' if sys.platform.startswith('linux') else 'cls'

# Classe para representar Maquina de Turing
# M = (Q, Σ, Γ, δ, q0, B, F) (SIPSER, 2006)
# O construtor recebe os elementos na ordem:
# M = (Q, Γ, B, Σ, δ, q0, F) + Descrição da Máquina
# para se igualar ao formato presente nos arquivos.
class MaquinaTuring:
    # Pilha de MTs para não determinismo
    # Ao final de um "caminho na arvore de execucao",
    #   a proxima MT da pilha executa o próximo caminho,
    #   se a anterior não aceita a cadeia
    pilha = []

    def __init__(self,
                 estados = None,
                 alfa_fita = None,
                 vazio = " ",
                 sigma = None,
                 transicoes = None, 
                 est_inicial = "", 
                 ests_finais = None,
                 desc = "Maquina de Turing"):

        # Elementos da Maquina
        # Q
        self.estados = estados
        # Σ
        self.alfabeto = sigma
        # Γ
        self.alfa_fita = alfa_fita
        # δ
        self.transicoes = transicoes
        # q0
        self.estado_atual = est_inicial
        # B
        self.simbolo_vazio = vazio
        # F
        self.ests_finais = set(ests_finais)
        
        # Uma descrição da máquina
        self.descricao = desc

        # Elementos de classe (funcionamento)
        self.cabeca_leitura = 0
        self.aceita = False
        self.fim = False
        self.cadeia_inicial = ""
        self.cadeia = ""

    # Realiza um passo do processamento de uma cadeia
    def processa(self):
        # Se consegue ler um caractere da fita
        try:
            caractere = self.cadeia[self.cabeca_leitura]
        # Caso contrário, lê B (uma fita infinita tanto à esquerda,
        # quanto à direita)
        except:
            self.cadeia[self.cabeca_leitura] = self.simbolo_vazio
        
        # Verifica se o símbolo pertence à (Γ U Σ U B)
        if (
            str(caractere) not in self.alfabeto and
            str(caractere) not in self.alfa_fita and
            str(caractere) != self.simbolo_vazio 
        ): 
            print("\n-----ATENCAO-----")
            print(">Cadeia Invalida!\n\n")
            sleep(2)
            self.fim = True
            return

        # Estrutura a possível transição
        transicao = (self.estado_atual, caractere)

        # Caso haja transição, transicione
        if transicao in self.transicoes:
            # Se há mais de uma instrução para a transicao:
            if len(self.transicoes[transicao]) > 1:
                # Empilha os caminhos da árvore
                for instrucao in self.transicoes[transicao][1:]:
                    estado, acao, direcao = instrucao
                    # Cria nova MT para a pilha
                    mt = MaquinaTuring(
                        self.estados,
                        self.alfa_fita,
                        self.simbolo_vazio,
                        self.alfabeto,
                        self.transicoes,
                        self.estado_atual,
                        self.ests_finais,
                        self.descricao
                            )
                    mt.cadeia = self.cadeia.copy()
                    mt.cadeia_inicial = self.cadeia_to_string('ini')
                    mt.cabeca_leitura = self.cabeca_leitura

                    # Aplica a transicao
                    mt.cadeia[mt.cabeca_leitura] = acao
                    if direcao == ">":
                        mt.cabeca_leitura += 1
                    elif direcao == "<":
                        mt.cabeca_leitura -= 1
                    mt.estado_atual = estado
                   
                    # as cadeia volta para o formato string para nao conflitar com o método processa
                    mt.cadeia = self.cadeia_to_string()
                    # Empilha
                    self.__push(MaquinaTuring.pilha, mt)

            # Executa o primeiro caminho/instrucao
            estado, acao, direcao = self.transicoes[transicao][0]
            self.cadeia[self.cabeca_leitura] = acao
              
            if direcao == ">":
                self.cabeca_leitura += 1
            elif direcao == "<":
                self.cabeca_leitura -= 1
            # Se não, não percorre a cadeia (direcao == "*")
                
            self.estado_atual = estado
        # Quando não há transição, vê se aceita (aceitação por
        # estado final)
        else:
            if self.estado_atual in self.ests_finais:
                self.aceita = True
                # Se aceita, apaga a pilha de caminhos
                MaquinaTuring.pilha = []
            self.fim = True

    # Processa uma cadeia inteira
    def processaCadeia(self, cadeia):
        self.cadeia_inicial = dict(enumerate(cadeia))
        self.cadeia = dict(enumerate(cadeia))

        # Prepara os dados que serao escritos no arquivo
        conteudo_arqv = self.__setuplaToString()
        passo_a_passo = ""
        
        # Processamento
        while not self.fim:
            os.system(CLEAR)
            try:
                caractere = self.cadeia[self.cabeca_leitura]
            except:
                self.cadeia[self.cabeca_leitura] = self.simbolo_vazio

            transicao = (self.estado_atual, caractere)

            # Impressao
            cabeca_pos = " " * self.cabeca_leitura
            cabeca_pos += "^"
            self.printa()
            print(f"Cabeca de Leitura => {cabeca_pos}")
            print(f"Estado Atual      => {self.estado_atual}")
            print(f"Transicao         => ")
            passo_a_passo += "Cadeia processada => " + self.cadeia_to_string() + "\n"
            passo_a_passo += "Cabeca de Leitura => " + cabeca_pos + "\n"
            passo_a_passo += "Estado Atual      => " + self.estado_atual + "\n"
            if transicao in self.transicoes:
                print('\u03B4' + f"{transicao} = {self.transicoes[transicao]}")
                passo_a_passo += '\u03B4'+ str(transicao) + " = " + str(self.transicoes[transicao]) + "\n\n"
            else: 
                print(f"Nao ha funcao de transicao definida para {transicao}!")
                passo_a_passo += "Nao ha funcao de transicao definida para "+ str(transicao) + "\n\n"
            self.processa()
            sleep(2)

        conteudo_arqv += "Cadeia processada => " + self.cadeia_to_string()
        self.printa()
        print("*****************")
        if self.aceita:
            print("  Cadeia Aceita !")
            print("*****************")
            sleep(3)
            conteudo_arqv += "\n\n"
            conteudo_arqv += "CADEIA ACEITA!"
        else:
            print("Cadeia Rejeitada!")
            print("*****************")
            sleep(3)
            conteudo_arqv += "\n\n"
            conteudo_arqv += "CADEIA REJEITADA!"

            # Se há algum caminho do não-determinismo, execute-o
            if len(MaquinaTuring.pilha) >= 1:
                mt = MaquinaTuring.pilha.pop()
                mt.processaCadeia(mt.cadeia)


        # Parte de salvar no arquivo comentada por enqanto
        #self.__salva_no_arqv(conteudo_arqv, passo_a_passo)


    def printa(self):
        print(f"{'=-'*(len(self.descricao)//2)}")
        print(self.descricao)
        print(f"{'=-'*(len(self.descricao)//2)}\n")
        print(f"Cadeia inicial    => {self.cadeia_to_string('ini')}")
        print(f"Cadeia processada => {self.cadeia_to_string()}")

    def cadeia_to_string(self, cadeia=""):
        if cadeia == "ini":
            string = ""
            for caractere in self.cadeia_inicial.values():
                string += str(caractere)
            return string
        else:
            string = ""
            for caractere in self.cadeia.values():
                string += str(caractere)
            return string
    
    def verifica_maquina(self):
        for estado, lista_transicao in self.transicoes.items():
            est_atual, simbolo = estado
            for (est_proxm, si_novo, direcao) in lista_transicao:
                if (
                    str(est_atual) not in self.estados or
                    str(est_proxm) not in self.estados or

                    str(simbolo) not in self.alfa_fita or
                    str(si_novo) not in self.alfa_fita
                ):
                    return False

        return True

    def __setuplaToString(self):
        setupla = ""
        setupla += "Estados: " + str(self.estados) + "\n"
        setupla += "Alfabeto da Fita: " + str(self.alfa_fita) + "\n"
        setupla += "Simbolo Vazio: '" + str(self.simbolo_vazio) + "'\n"
        setupla += "Alfabeto (" + '\u03A3' + "): " + str(self.alfabeto) + "\n"
        setupla += "Estado inicial: " + str(self.estado_atual) + "\n"
        setupla += "Estados Finais: " + str(self.ests_finais) + "\n"
        setupla += "Transicoes (" + '\u03B4' + "): " + str(self.transicoes) + "\n"
        setupla += "-----------------------------------------------\n"
        setupla += "Cadeia inicial    => " + str(self.cadeia_to_string('ini')) + "\n"
        
        return setupla

    def __salva_no_arqv(self, cabecalho, passos):
        string = ""
        string += cabecalho
        string += "------------PASSO-A-PASSO------------\n"
        string += passos

        nome = ''
        for char in list(self.cadeia_inicial.values())[:-1]:
            nome += char
        diretorio = "execucoes"
        path = os.path.join(diretorio, nome)
        with open(path, 'w', encoding='utf-8') as arqv:
            arqv.write(string)

    
    def __push(self, pilha, x):
        pilha.insert(0, x)
