import os
import sys
import copy
#import random
from time import sleep
from DescricaoInstantanea import DescricaoInstantanea

# Constante para limpar terminal (Linux ou Windows)
CLEAR = 'clear' if sys.platform.startswith('linux') else 'cls'

# Classe para representar Maquina de Turing
# M = (Q, Σ, Γ, δ, q0, B, F) (SIPSER, 2006)
# O construtor recebe os elementos na ordem:
# M = (Q, Γ, B, Σ, δ, q0, F) + Descrição da Máquina
# para se igualar ao formato presente nos arquivos.
class MaquinaTuring:

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

        # Variavel para auxilio da persistencia das execuções
        self.passo_a_passo = ""
        self.brancos = 0

        # Elemento do Não-Determinismo (pilha de DescricaoInstantanea)
        self.pilha = []

    # Realiza um passo do processamento de uma cadeia
    def processa(self):
        # Se consegue ler um caractere da fita
        try:
            caractere = self.cadeia[self.cabeca_leitura]
        # Caso contrário, lê B (uma fita infinita tanto à esquerda,
        # quanto à direita)
        except:
            self.cadeia[self.cabeca_leitura] = self.simbolo_vazio
            caractere = self.simbolo_vazio
        
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
                # -------------------------------------------------
                # Seleciona uma das transicoes aleatoriamente
                # tran = random.choice(self.transicoes[transicao])
                # outras_transicoes = [x for x in self.transicoes[transicao] if x!=tran]
                # -------------------------------------------------

                # Empilha os caminhos da árvore
                for instrucao in self.transicoes[transicao][1:]:
                    # Guarda a Descricao instantanea
                    instante = DescricaoInstantanea(
                            self.cabeca_leitura, self.cadeia, 
                            self.estado_atual, instrucao, self.passo_a_passo)
                    # Empilha
                    self.__push(self.pilha, instante)

            # Executa o primeiro caminho/instrucao
            estado, acao, direcao = self.transicoes[transicao][0]
            self.cadeia[self.cabeca_leitura] = acao

            # Marca qual transição foi tomada
            self.passo_a_passo += "Transicao Tomada: "
            self.passo_a_passo += '\u03B4' + " : " + f'({estado}, {acao}, {direcao})' + "\n"
              
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
                self.pilha = []
            self.fim = True

    # Processa uma cadeia inteira
    def processaCadeia(self, cadeia, nd = False):
        # Se é o processamento de um novo ramo do nao determinismo, precisa resetar a variavel fim
        if nd:
            self.fim = False
        else: 
            self.cadeia_inicial = dict(enumerate(cadeia))
            self.passo_a_passo = ""
            self.brancos = 0
        self.cadeia = dict(enumerate(cadeia))

        # Prepara os dados que serao escritos no arquivo
        conteudo_arqv = self.__setuplaToString()
        
        # Processamento
        while not self.fim:
            os.system(CLEAR)
            try:
                caractere = self.cadeia[self.cabeca_leitura]
            except:
                self.cadeia[self.cabeca_leitura] = self.simbolo_vazio
                caractere = self.simbolo_vazio

            transicao = (self.estado_atual, caractere)

            # Impressao
            self.printa()
            cabeca_pos = " " * (self.cabeca_leitura + self.brancos)
            cabeca_pos += "^"
            print(f"Cabeca de Leitura => {cabeca_pos[2:]}")
            print(f"Estado Atual      => {self.estado_atual}")
            print(f"Transicao         => ")
            self.passo_a_passo += "\nCadeia processada => " + self.cadeia_to_string() + "\n"
            self.passo_a_passo += "Cabeca de Leitura => " + cabeca_pos[self.brancos:] + "\n"
            self.passo_a_passo += "Estado Atual      => " + self.estado_atual + "\n"
            if transicao in self.transicoes:
                print('\u03B4' + f"{transicao} = {self.transicoes[transicao]}")
                self.passo_a_passo += '\u03B4'+ str(transicao) + " = " + str(self.transicoes[transicao]) + "\n"
            else: 
                print(f"Nao ha funcao de transicao definida para {transicao}!")
                self.passo_a_passo += "Nao ha funcao de transicao definida para "+ str(transicao) + "\n"
            self.processa()
            sleep(0.8)

        print("*****************")
        if self.aceita:
            conteudo_arqv += "Cadeia processada => " + self.cadeia_to_string()
            print("  Cadeia Aceita !")
            print("*****************")
            conteudo_arqv += "\n\n"
            conteudo_arqv += "CADEIA ACEITA!\n"
            sleep(1.2)
            self.__salva_no_arqv(conteudo_arqv, self.passo_a_passo)
        else:
            print("Ramo do nao-determinismo Rejeitado!")
            print("*****************")
            sleep(1.2)
            # Se não ha mais ramos do não-determinismo
            # Então pode armazenar no arquivo que a cadeia foi rejeitada!
            if len(self.pilha) == 0:
                conteudo_arqv += "Cadeia processada => " + self.cadeia_to_string()
                conteudo_arqv += "\n\n"
                conteudo_arqv += "CADEIA REJEITADA!\n"
                self.__salva_no_arqv(conteudo_arqv, self.passo_a_passo)

            # Se há algum caminho do não-determinismo, execute-o
            if len(self.pilha) >= 1:
                di = self.pilha.pop()
                self.__recuperaInstancia(di)

    def printa(self):
        # Conta a quantidade de símbolos brancos que há efetivamente na cadeia
        # (pra ficar bonitinho na hora de printar)
        vazios_cadeia = 0
        for s in reversed(self.cadeia_to_string()):
            if s == self.simbolo_vazio:
                vazios_cadeia += 1
            else:
                break
        print(f"{'=-'*(len(self.descricao)//2)}")
        print(self.descricao)
        print(f"{'=-'*(len(self.descricao)//2)}\n")
        if len(self.cadeia_to_string()) < 20:
            self.brancos = (20-len(self.cadeia_to_string()))//2
        print(f"Cadeia inicial  => {self.brancos*self.simbolo_vazio}{self.cadeia_to_string('ini')}{(self.brancos-1)*self.simbolo_vazio}")
        print(f"Fita processada => {self.brancos*self.simbolo_vazio}{self.cadeia_to_string()}{(self.brancos-vazios_cadeia)*self.simbolo_vazio}")

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
        string += "------------PASSO-A-PASSO------------"
        string += passos

        nome = ''
        for char in list(self.cadeia_inicial.values()):
            nome += char
        diretorio = "execucoes"
        path = os.path.join(diretorio, nome)
        with open(path, 'w', encoding='utf-8') as arqv:
            arqv.write(string)

    
    def __push(self, pilha, x):
        pilha.insert(0, x)

    def __recuperaInstancia(self, descricaoInstantanea):
        self.cadeia = copy.deepcopy(descricaoInstantanea.cadeia)
        self.cabeca_leitura = copy.deepcopy(descricaoInstantanea.cabeca_leitura)
        self.estado_atual = copy.deepcopy(descricaoInstantanea.estado)
        self.passo_a_passo = copy.deepcopy(descricaoInstantanea.passo)

        # Marca qual transição foi tomada
        estado, acao, direcao = descricaoInstantanea.instrucao
        self.passo_a_passo += "Transicao Tomada: "
        self.passo_a_passo += '\u03B4' + " : " + f'({estado}, {acao}, {direcao})' + "\n"

        self.processaCadeia(self.cadeia_to_string(), True)
