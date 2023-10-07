

# LUIZ FERNANDO GOMES DOS SANTOS
# ANÁLISE E DESENVOLVIMENTO DE SISTEMAS
# Disciplina: Raciocínio Computacional (11100010563_20232_01)

import os
import json

# Função para limpar tela
def limpatela():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

# Funçõo para mostrar menu principal
def menu_principal():
    print("-------------------")
    print("¦  MENU PRINCIPAL ¦")
    print("-------------------")

    print("\n\n 1 - Estudante \n 2 - Professor \n 3 - Disciplina \n 4 - Turma \n 5 - Matrícula \n 9 - Sair \n")

    opcao = input("Escolha uma opção: ")
    return opcao

# Funçõo para mostrar menu de operações, a função precisa de um parâmetro, que seria a escolha da pessoa em "menu_principal"
def menu_operacoes(opcao):
    print("\n")
    if opcao == '1':
        print("------ MENU DE ESTUDANTE ----- \n")
    elif opcao == '2':
        print("------ MENU DE PROFESSORES ----- \n")
    elif opcao == '3':
        print("------ MENU DE DISCIPLINA ----- \n")
    elif opcao == '4':
        print("------ MENU DE TURMA ----- \n")
    elif opcao == '5':
        print("------ MENU DE MATRÍCULA ----- \n")

    print("O que você deseja fazer?\n")
    print(" 1 - Adicionar \n 2 - Listar \n 3 - Excluir \n 4 - Alterar \n 9 - Voltar ao menu principal \n")

    sub_opcao = input("Escolha uma opção: ")

    return sub_opcao

# Função para verificar se arquivo está vazio
def verifica_se_arquivo_esta_vazio(arquivo_json):

    #pegando o nome do arquivo sem a parte ".json"
    nome_sem_extensao = arquivo_json.split('.')[0]

    # verificando se o arquivo existe no caminho especificado
    if not os.path.exists(arquivo_json):
        print(f"Não há registro de {nome_sem_extensao}(s)")
        return True

    # lendo o arquivo, se estiver vazio, é mostrado a mensagem que nenhum registro foi encontrado
    try:
        with open(arquivo_json, 'r') as file:
            dados = json.load(file)
            if len(dados) == 0:
                print(f"Não há registro de {nome_sem_extensao}(s)")
                return True
    except json.decoder.JSONDecodeError:
        #mensagem mostrada se o arquivo estiver ocm json inválido
        print(f"Não há registro de {nome_sem_extensao}(s)")
        return True

    return False

# Função para verificar se já existe id ao adicionar um novo módulo
def verifica_se_id_ja_existe(id,dados):

    for dado in dados:
        if id == dado['id']:
            print("\nEsse id já existe")
            return True

    return False


# ********** ADICIONAR DADOS **********
# função de adicionar dados que precisa de dois parâmetros, arquivo json e campos
def adicionarDados(arquivo_json,campos):

    # Verifica se o arquivo existe ou está vazio
    if not os.path.exists(arquivo_json) or os.path.getsize(arquivo_json) == 0:
        dados = []
    else:
        try:
            # abri o arquivo em forma de escrita
            with open(arquivo_json, 'r', encoding='utf-8') as file:
                dados = json.load(file)
        except FileNotFoundError:
            dados = []
    
    nome_sem_extensao = arquivo_json.split('.')[0]
    

    print(f"Adicione Abaixo os itens para o(a) {nome_sem_extensao}\n")

    
    informacao = []
    dicionario_de_dados = {}

    # loop nos caampos passados por parâmetro
    for i, campo in enumerate(campos):

        # if necessário para forcar o campo "id" ser um número inteiro
        if i == 0:

            try:
                campo = int(input(f"{campo} -> "))

                if verifica_se_id_ja_existe(campo,dados):
                    return 
            
                # adiciona id na lista de informações
                informacao.append(campo)
            except ValueError:
                # caso o usuário digite algo diferente de um número inteiro
                print("\nO id deve ser um valor númerico inteiro")
                return

        else:
            campo = input(f"{campo} -> ")

            #adiciona os outros campos a lista de informações
            informacao.append(campo)

    for i, campo in enumerate(campos):
        # adicionando ao dicionáario de dados as informações em seus respectivos campos
        dicionario_de_dados[campo] = informacao[i]

    dados.append(dicionario_de_dados)

    #abri o arquivo em forma de leitura e adiciona os dados digitados pelo usuário
    with open(arquivo_json,'w', encoding='utf-8') as file:
        json.dump(dados,file,ensure_ascii = False)
    
    print(f"\n{nome_sem_extensao} Adicionado(a)!") 


# ********** LISTAR DADOS **********
# função de listar dados que precisa de dois parâmetros, arquivo json e campos
def listarDados(arquivo_json,campos):


    if verifica_se_arquivo_esta_vazio(arquivo_json):
        return

    
    with open(arquivo_json, 'r', encoding='utf-8') as file:
        dados = json.load(file)
        
    # loop nos dados do arquivo json    
    for i,dado in enumerate(dados):
        #loop nos campos especificados por parâmetro
        for i in range(len(campos)):
            # separa os campos com "|"
            print(f" {campos[i]}: {dado[campos[i]]}", end=' | ')

        print("\n")
        print("----------------------------------------------------------\n")


# ********** EXCLUIR DADOS **********
# função de excluir dados que precisa de um parâmetro, arquivo json.
# é necessário colocar um segundo parâmetro por mais que ele não seja usado, a falta dele ocasionaria um erro
def excluirDados(arquivo_json,campos):
    if verifica_se_arquivo_esta_vazio(arquivo_json):
        return

    with open(arquivo_json, 'r') as file:
        dados = json.load(file)
    
    nome_sem_extensao = arquivo_json.split('.')[0]

    try:
        id = int(input(f"Digite o id do(a) {nome_sem_extensao} que deseja excluir: "))
    except ValueError:
        print("\nO id deve ser um valor númerico inteiro")
        return
    
    encontrado = False

    # loop nos dados do arquivo, se existir o mesmo id digitado, é excluido os dados desse id
    for dado in dados:
        if dado['id'] == id:
            encontrado = True
            dados.remove(dado)

    # se o id digitado não for enconrado, retorna a mensagem
    if not encontrado:
        print("\nId não encontrado")
        return

    with open(arquivo_json, 'w') as file:
        json.dump(dados,file)
    
    print(f"\n {nome_sem_extensao} Removido(a)!!")


# ********** ALTERAR DADOS **********
# função de alterar dados que precisa de dois parâmetros, arquivo json e campos
def alterarDados(arquivo_json,campos):
    if verifica_se_arquivo_esta_vazio(arquivo_json):
        return
    
    with open(arquivo_json, 'r') as file:
        dados = json.load(file)
    
    nome_sem_extensao = arquivo_json.split('.')[0]

    try:
        id = int(input(f"Digite o id do(a) {nome_sem_extensao} que deseja alterar: "))
    except ValueError:
        print("\nO id deve ser um valor númerico inteiro")
        return

    encontrado = False

    for dado in dados:
        if dado['id'] == id:
            encontrado = True
            print("\nId encontrado! Digite abaixo os novos dados\n")
            for i,campo in enumerate(campos):
                # garente que o id não será alterado
                if i == 0:
                    continue
                else:
                    # alterando os campos
                    dado[campo] = input(f"{campo} -> ")
            
    if not encontrado:
        print("\nId não encontrado")
        return

    with open(arquivo_json, 'w', encoding='utf-8') as file:
        json.dump(dados,file,ensure_ascii = False)
    
    print(f"\n{nome_sem_extensao} Alterado(a)!!")


"""
    A função executarComando é a principal do código, ela é responsável por executar a ação desejada pelo usuário.
    Ela utiliza um dicionário chamado possibilidades para mapear as combinações de opções e sub_opções para as ações a serem executadas
    A função retornada é baseada no valor das variáveis opção e sub_opção, por exemplo se a função retornada for 'listarEstudante',
    neste caso o valor de opção é 1 e o valor de sub_opção é 2. A função também retorna um texto explicando ao usuário em qual menu ele está.

    Foi adicionado a função mais duas chaves, arquivo: que seria o arquivo json para fazer as operações e campos, que também são usados
    nas operações. Como a função de excluir dados não precisa de campos, não é passado nenhum para ela
"""
def executarComando(opcao, sub_opcao):
    chave = (opcao, sub_opcao)  #tupla 
    possibilidades = {
        ('1', '1'): {'texto': 'ADICIONAR ESTUDANTE', 'função': adicionarDados, 'arquivo': 'estudante.json', 'campos': ['id','nome','cpf']},
        ('1', '2'): {'texto': 'LISTAR ESTUDANTE', 'função': listarDados,'arquivo': 'estudante.json', 'campos': ['id','nome','cpf']},
        ('1', '3'): {'texto': 'EXCLUIR ESTUDANTE', 'função': excluirDados,'arquivo': 'estudante.json', 'campos': ''},
        ('1', '4'): {'texto': 'ALTERAR ESTUDANTE', 'função': alterarDados,'arquivo': 'estudante.json', 'campos': ['id','nome','cpf']},

        ('2', '1'): {'texto': 'ADICIONAR PROFESSOR', 'função': adicionarDados, 'arquivo': 'professor.json', 'campos': ['id','nome','cpf']},
        ('2', '2'): {'texto': 'LISTAR PROFESSOR', 'função': listarDados, 'arquivo': 'professor.json', 'campos': ['id','nome','cpf']},
        ('2', '3'): {'texto': 'EXCLUIR PROFESSOR', 'função': excluirDados, 'arquivo': 'professor.json', 'campos': ''},
        ('2', '4'): {'texto': 'ALTERAR PROFESSOR', 'função': alterarDados, 'arquivo': 'professor.json', 'campos': ['id','nome','cpf']},

        ('3', '1'): {'texto': 'ADICIONAR DISCIPLINA', 'função': adicionarDados, 'arquivo' : 'disciplina.json', 'campos': ['id','nome']},
        ('3', '2'): {'texto': 'LISTAR DISCIPLINAS', 'função': listarDados, 'arquivo' : 'disciplina.json', 'campos': ['id','nome']},
        ('3', '3'): {'texto': 'EXCLUIR DISCIPLINA', 'função': excluirDados, 'arquivo' : 'disciplina.json', 'campos': ''},
        ('3', '4'): {'texto': 'ALTERAR DISCIPLINA', 'função': alterarDados, 'arquivo' : 'disciplina.json', 'campos': ['id','nome']},

        ('4', '1'): {'texto': 'ADICIONAR TURMA', 'função': adicionarDados, 'arquivo' : 'turma.json', 'campos': ['id', 'id.professor', 'id.disciplina']},
        ('4', '2'): {'texto': 'LISTAR TURMAS', 'função': listarDados, 'arquivo' : 'turma.json', 'campos': ['id', 'id.professor', 'id.disciplina']},
        ('4', '3'): {'texto': 'EXCLUIR TURMA', 'função': excluirDados, 'arquivo' : 'turma.json', 'campos': ''},
        ('4', '4'): {'texto': 'ALTERAR TURMA', 'função': alterarDados, 'arquivo' : 'turma.json', 'campos': ['id', 'id.professor', 'id.disciplina']},

        ('5', '1'): {'texto': 'ADICIONAR MATRÍCULA', 'função': adicionarDados, 'arquivo' : 'matricula.json', 'campos': ['id', 'id.turma','id do estudante']},
        ('5', '2'): {'texto': 'LISTAR MATRÍCULAS', 'função': listarDados, 'arquivo' : 'matricula.json', 'campos': ['id', 'id.turma','id do estudante']},
        ('5', '3'): {'texto': 'EXCLUIR MATRÍCULA', 'função': excluirDados, 'arquivo' : 'matricula.json', 'campos': ''},
        ('5', '4'): {'texto': 'ALTERAR MATRÍCULA', 'função': alterarDados, 'arquivo' : 'matricula.json', 'campos': ['id', 'id.turma','id do estudante']},
    }

    if chave in possibilidades:
        texto = possibilidades[chave]['texto']
        print(f'\n>>>>>>>>>>>>>>> {texto} <<<<<<<<<<<<<<<\n')
        return possibilidades[chave]['função'](possibilidades[chave]['arquivo'], possibilidades[chave]['campos'])
    else:
        print("\nOpção inválida")


# ---------- INÍCIO ---------
while True:
    print("\n")

    opcao = menu_principal()

    limpatela()

    if opcao == '9':
        print("\nEncerrando o programa...\n")
        break

    if opcao not in ['1','2','3','4','5']:
        print("\nOpção invalida")

    else:
        while True:

            sub_opcao = menu_operacoes(opcao)

            limpatela()

            if sub_opcao == '9':
                break

            executarComando(opcao,sub_opcao)
        