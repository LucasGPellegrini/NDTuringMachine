from turingmachine import MaquinaTuring
import os
import sys
import pickle

# Constante para limpar terminal (Linux ou Windows)
CLEAR = 'clear' if sys.platform.startswith('linux') else 'cls'

def main():
    opt = 0
    cadeia = ""

    # Carrega as maquinas de turing
    dicio_mt = {}
    diretorio = "maquinas_bin"
    for arquivo in os.listdir(diretorio):
        nome = arquivo[:-4]
    
        path = os.path.join(diretorio, arquivo)
        with open(path, 'rb') as mt_arq:
            maquina = pickle.load(mt_arq)
            dicio_mt.update({nome:maquina})

    # Testa
    dicio_mt['ex2'].processaCadeia("0101")

if __name__ == "__main__":
    main()
