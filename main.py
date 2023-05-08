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
            
    # Menu com usuario
    while opt > 7 or opt < 1:
        os.system(CLEAR)
        print("--------------OPCOES--------------")
        print("----------------------------------")
        print("1. MT para Inverter Binario")
        print("2. MT para verificar se uma\n   cadeia pertence a\n   L = {w | w = a^n b a^n}")
        print("3. MT Teste 1")
        print("4. MT Teste 2")
        print("5. MT Teste 3")
        print("6. MT Teste 4")
        print("7. Sair do Programa")
        opt = int(input("Escolha uma opção: "))

    if opt == 7: return
    else:
        cadeia = input("Digite a cadeia: ")

        if opt == 1:
            if cadeia[-1] != dicio_mt['invertebin'].simbolo_vazio : 
                cadeia += dicio_mt['invertebin'].simbolo_vazio

            dicio_mt['invertebin'].processaCadeia(cadeia)
            main()
        elif opt == 2:
            if cadeia[-1] != dicio_mt['anban'].simbolo_vazio : 
                cadeia += dicio_mt['anban'].simbolo_vazio

            dicio_mt['anban'].processaCadeia(cadeia)
            main()
        elif opt == 3:
            if cadeia[-1] != dicio_mt['teste1'].simbolo_vazio : 
                cadeia += dicio_mt['teste1'].simbolo_vazio

            dicio_mt['teste1'].processaCadeia(cadeia)
            main()
        elif opt == 4:
            if cadeia[-1] != dicio_mt['teste2'].simbolo_vazio : 
                cadeia += dicio_mt['teste2'].simbolo_vazio

            dicio_mt['teste2'].processaCadeia(cadeia)
            main()
        elif opt == 5:
            if cadeia[-1] != dicio_mt['teste3'].simbolo_vazio : 
                cadeia += dicio_mt['teste3'].simbolo_vazio

            dicio_mt['teste3'].processaCadeia(cadeia)
            main()
        elif opt == 6:
            if cadeia[-1] != dicio_mt['teste4'].simbolo_vazio : 
                cadeia += dicio_mt['teste4'].simbolo_vazio

            dicio_mt['teste4'].processaCadeia(cadeia)
            main()


if __name__ == "__main__":
    main()

