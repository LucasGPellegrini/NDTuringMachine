import pickle
import os
import ast
from turingmachine import MaquinaTuring

dicio_mt = {}
diretorio = "maquinas"
for arquivo in os.listdir(diretorio):
    nome = arquivo[:-3]
    
    path = os.path.join(diretorio, arquivo)
    f = open(path, "r")
    
    estados = f.readline().replace('\n', '')
    estados = ast.literal_eval(estados)

    alfa_fita = f.readline().replace('\n', '')
    alfa_fita = ast.literal_eval(alfa_fita)

    vazio = f.readline().replace('\n', '')
    vazio = ast.literal_eval(vazio)

    sigma = f.readline().replace('\n', '')
    sigma = ast.literal_eval(sigma)

    delta = ""
    delta += f.readline()
    while delta[-2] != '}':
        delta += f.readline()
    delta = delta.replace('\n', '')
    delta = ast.literal_eval(delta)

    inicial = f.readline().replace('\n', '')
    
    finais = f.readline().replace('\n', '')
    finais = ast.literal_eval(finais)

    desc = f.readline().replace('\n', '')

    f.close()

    maquina = MaquinaTuring(
            estados, 
            alfa_fita, 
            vazio, 
            sigma, 
            delta, 
            inicial,
            finais,
            desc
            )
    if maquina.verifica_maquina():
        dicio_mt.update({nome:maquina})
    else:
        print(f"Maquina '{nome}' invalida!!!")

#escrita serializada das maquinas de turing
diretorio = "maquinas_bin"
for nome, mt in dicio_mt.items():
    nome_arqv = nome + ".pkl"
    path = os.path.join(diretorio, nome_arqv)
    
    with open(path, 'wb') as mt_arq:
        pickle.dump(mt, mt_arq)
