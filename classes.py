from datetime import datetime
from dateutil.relativedelta import (
    relativedelta,
)  # Função que calcula direto a idade em anos, meses e dias.
import pandas as pd
import os


class Paciente:
    """
    Classe que modela a entidade paciente dentro de um sistema de gestão hospitalar.
    """

    def __init__(
        self,
        id_paciente: str,
        nome: str,
        cpf: str,
        data_nascimento: str,
        sexo: str,
        peso: float,
        altura: float,
    ) -> None:
        self.id = id_paciente
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.idade = self.calcular_idade(data_nascimento)
        self.sexo = sexo
        self.peso = peso
        self.altura = altura
        self.imc = self.calcular_imc(peso, altura)
        self.consultas = []

    def calcular_imc(self, peso: float, altura: float) -> float:
        if altura <= 0:
            raise ValueError("Altura deve ser maior que zero para calcular o IMC.")
        return round(peso / (altura**2), 2)

    def calcular_idade(self, data_nascimento: str) -> str:
        nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        hoje = datetime.now()
        idade = relativedelta(hoje, nascimento)
        return f"{idade.years} anos, {idade.months} meses e {idade.days} dias"

    def __call__(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "idade": self.idade,
            "sexo": self.sexo,
            "peso": self.peso,
            "altura": self.altura,
            "imc": self.imc,
            "consultas": self.consultas,
        }


class Funcionario:
    """
    Classe que modela a entidade funcionário dentro de um sistema de gestão hospitalar
    """

    def __init__(self, id_funcionario: str, nome: str, cargo: str, n_doc: int, status = 'Ativo') -> None:
        self.id = id_funcionario
        self.nome = nome
        self.cargo = cargo
        self.n_doc = n_doc
        self.status = status
    
    def alterar_status(self, status: str):
        self.status = status

    def __call__(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cargo": self.cargo,
            "n_doc": self.n_doc,
        }


class Radiofarmaco:
    """
    Classe que modela a entidade radiofármaco dentro de um sistema de gestão hospitalar
    """

    def __init__(
        self,
        id_radiofarmaco: str,
        princp_ativo: str,
        concentracao: str,
        data_fabricacao: str,
    ) -> None:
        self.id = id_radiofarmaco
        self.princip_ativo = princp_ativo
        self.concentracao = concentracao
        self.data_fabricacao = data_fabricacao

    def __call__(self):
        return {
            "id": self.id,
            "princip_ativo": self.princip_ativo,
            "concentracao": self.concentracao,
            "data_fabricacao": self.data_fabricacao,
        }

class Exame:
    """
    Classe que modela a entidade exame dentro de um sistema de gestão hospitalar
    """

    def __init__(
        self,
        id_exame: str,
        tipo: str,
        data: str,
        id_paciente: str,
        id_funcionario: str,
        id_consulta: str,
        id_radiofarmaco: str,
    ) -> None:
        self.id = id_exame
        self.tipo = tipo
        self.data = data
        self.id_paciente = id_paciente
        self.id_funcionario = id_funcionario
        self.id_consulta = id_consulta
        self.id_radiofarmaco = id_radiofarmaco

    def __call__(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "data": self.data,
            "id_paciente": self.id_paciente,
            "id_funcionario": self.id_funcionario,
            "id_consulta": self.id_consulta,
            "id_radiofarmaco": self.id_radiofarmaco,
        }

class Consulta:
    """
    Classe que modela a entidade consulta dentro de um sistema de gestão hospitalar
    """

    def __init__(
        self,
        id_consulta: str,
        id_paciente: str,
        data: str,
        id_funcionario: str,
        procedimento: list[str],
    ) -> None:
        self.id_consulta = id_consulta
        self.id_paciente = id_paciente
        self.data = data
        self.id_funcionario = id_funcionario
        self.procedimento = procedimento

    def __call__(self):
        return {
            "id": self.id_consulta,
            "id_paciente": self.id_paciente,
            "data": self.data,
            "id_funcionario": self.id_funcionario,
            "procedimento": self.procedimento,
        }

class BancoDados:
    """
    Classe que modela o banco de dados utilizando dataframes e salvando em .csv
    """

    def __init__(self, nome: str, vazio:bool = False) -> None:
        self.nome = nome
        self.df: pd.DataFrame = pd.DataFrame()
        if not os.path.exists("data"):
            os.makedirs("data")
        self.caminho_arquivo = "data/" + self.nome + ".csv"
        if os.path.exists(self.caminho_arquivo) and not vazio:
            self.atualizar_banco()

    def adicionar_coluna(self, nome_coluna: str, valor_coluna: str):
        """
        Adiciona uma coluna ao dataframe, contanto que a coluna não exista.
        Caso exista, retorna False
        """
        if nome_coluna in self.df.columns:
            print("Erro: A coluna já existe.")
            return False
        else:
            self.df[nome_coluna] = valor_coluna
        return self.df

    def adicionar_linha(self, linha: dict) -> pd.DataFrame:
        """
        Adiciona uma linha ao dataframe, contanto que a linha esteja no formato do dataframe.
        Caso não esteja, retorna False
        """
        
        if self.buscar("id", linha["id"], "index") is not False:
            print("Erro: A linha já existe.")
            return False

        linha = pd.DataFrame([linha])
        if self.df.empty:
            self.df = linha
        elif all(self.df.columns == linha.keys()):
            self.df = pd.concat([self.df, linha], ignore_index=True)
        else:
            print("As colunas do DataFrame não correspondem às chaves fornecidas.")
            return False
        return self.df

    def adicionar_linhas(self, linhas: list[dict]) -> pd.DataFrame:
        """
        Adiciona várias linhas ao dataframe, contanto que as linhas estejam no formato do dataframe.
        Caso não estejam, retorna False
        """

        for linha in linhas:
           self.adicionar_linha(linha)
        
        return self.df

    def remover_linha(self, linha: dict) -> pd.DataFrame:
        """
        Remove uma linha do dataframe, contanto que a linha esteja no formato do dataframe.
        Caso não esteja, retorna False
        """

        if self.buscar("id", linha["id"], "index") is False:
            print("Erro: A linha não existe.")
            return False
        
        self.df = self.df.drop(self.df[self.df["id"] == linha["id"]].index)
        return self.df

    def salvar(self):
        """
        Salva o dataframe em um arquico .csv.
        """

        self.df.to_csv(self.caminho_arquivo, index=False)

    def atualizar_banco(self) -> pd.DataFrame:
        """
        Carrega um arquivo .csv em um dataframe.

        """

        self.df = pd.read_csv(self.caminho_arquivo)
   

        return self.df

    def carregar_dados(
        self, caminho_dados: str = None, dados: dict = None
    ) -> pd.DataFrame:
        """
        Carrega dados de um arquivo .csv ou de um dicionário em um dataframe.

        """
        if caminho_dados is not None:
            self.df = pd.read_csv(caminho_dados)
        elif dados is not None:
            self.df = pd.DataFrame(dados)
        else:
            print("Erro: Nenhum dado fornecido para carregar.")

        
        return self.df


    def buscar(self, coluna: str, valor: str, mode: str = 'full') -> pd.DataFrame:
        """
        Busca um valor em uma coluna do dataframe.

        mode: 
         - 'full' -> devolve a linha toda 
         - 'index' -> devolve o indice da linha contendo o valor
        """
             
        if mode == "full":
            return self.df[self.df[coluna] == valor]
        elif mode == "index":
            return  self.df[self.df[coluna] == valor].index[0]
        else:
            print("Erro: Modo inválido.")
            return False

    
    def atualizar_linha(self,linha_nova:dict):
        """
        Atualiza uma linha do dataframe.
        """
        
        


    def __call__(self):
        return self.df


class Sistema:
    def __init__(self) -> None:
        self.pacientes_db = BancoDados("pacientes")
        self.funcionarios_db = BancoDados("funcionarios")
        self.radiofarmacos_db = BancoDados("radiofarmacos")
        self.exames_db = BancoDados("exames")
        self.consultas_db = BancoDados("consultas")
        self.passagens_db = BancoDados("passagens")
        self.divider = "=" * 45

    def shutdown(self):
        self.pacientes_db.salvar()
        self.funcionarios_db.salvar()
        self.consultas_db.salvar()
        self.exames_db.salvar()
        self.radiofarmacos_db.salvar()
        self.passagens_db.salvar()

        print(
            "{div} Banco de Dados salvo! \n {div} \n Desligando o sistema... \n {div}".format(
                div=self.divider
            )
        )

    def menu_principal(self, opcao: int = None):
        os.system("cls" if os.name == "nt" else "clear")  # limpar terminal
        print("Bem vindo ao sistema de gestão hospitalar!")
        print("Escolha uma opção:")
        print("1 - Cadastrar/Agendar")
        print("2 - Modificar")
        print("3 - Consultar")
        print("4 - Excluir")
        print("0 - Sair")

        if opcao is None:
            opcao = input("Selecione sua opção: ")

        if opcao == "1":
            self.menu_cadastrar()
        elif opcao == "2":
            self.menu_modificar()
        elif opcao == "3":
            self.menu_consultar()
        elif opcao == "4":
            self.menu_excluir()
        elif opcao == "0":
            print("Tem certeza que quer desligar o sistema?")
            confirmacao = input("Digite 's' para confirmar: ")
            if confirmacao == "s":
                self.shutdown()
            else:
                self.menu_principal()
        else:
            print("Opção inválida!")
            self.menu_principal()

    def menu_cadastrar(self, opcao: int = None):
        os.system("cls" if os.name == "nt" else "clear")  # limpar terminal
        print("Escolha uma opção para cadastrar ou agendar:")
        print("1 - Paciente")
        print("2 - Funcionário")
        print("3 - Radiofármaco")
        print("4 - Exame")
        print("5 - Consulta")
        print("0 - Voltar")

        if opcao is None:
            opcao = input("Selecione sua opção: ")

        if opcao == "1":
            self.cadastrar_paciente()
        elif opcao == "2":
            self.cadastrar_funcionario()
        elif opcao == "3":
            self.cadastrar_radiofarmaco()
        elif opcao == "4":
            self.cadastrar_exame()
        elif opcao == "5":
            self.agendar_consulta()
        elif opcao == "0":
            self.menu_principal()
        else:
            print("Opção inválida!")
            self.menu_cadastrar()
    
    def menu_modificar(self, opcao: int = None):
        os.system("cls" if os.name == "nt" else "clear")  # limpar terminal
        print("Escolha uma opção para modificar:")
        print("1 - Paciente")
        print("2 - Funcionário")
        print("3 - Radiofármaco")
        print("4 - Exame")
        print("5 - Consulta")
        print("0 - Voltar")

        if opcao is None:
            opcao = input("Selecione sua opção: ")

        if opcao == "1":
            self.modificar_paciente()
        elif opcao == "2":
            self.modificar_funcionario()
        elif opcao == "3":
            self.modificar_radiofarmaco()
        elif opcao == "4":
            self.modificar_exame()
        elif opcao == "5":
            self.modificar_consulta()
        elif opcao == "0":
            self.menu_principal()
        else:
            print("Opção inválida!")
            self.menu_modificar()

    def modificar_paciente(self):
        os.system("cls" if os.name == "nt" else "clear")  # limpar terminal
        id_paciente = input("Digite o ID do paciente: ")
        #buscar paciente
        if paciente is None:
            print("Paciente não encontrado!")
            return
        print("Digite os novos dados do paciente:")
        nome = input("Digite o nome completo do paciente: ")
        cpf = input("Digite o CPF do paciente (apenas números): ")
        data_nascimento = input("Digite a data de nascimento do paciente (DD/MM/AAAA): ")
        sexo = input("Digite o sexo do paciente (M/F): ")
        peso = float(input("Digite o peso do paciente (em kg): "))
        altura = float(input("Digite a altura do paciente (em metros): "))

        paciente = Paciente(
            id_paciente=id_paciente,
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            sexo=sexo,
            peso=peso,
            altura=altura
        )

        # Modificando o paciente no banco de dados
        self.pacientes_db.atualizar_linha(paciente())
        self.pacientes_db.salvar()

        print(f"Paciente {nome} modificado com sucesso!")


    def cadastrar_paciente(self):
        os.system("cls" if os.name == "nt" else "clear")  # limpar terminal
        id_paciente = input("Digite o ID do paciente: ")
        nome = input("Digite o nome completo do paciente: ")
        cpf = input("Digite o CPF do paciente (apenas números): ")
        data_nascimento = input("Digite a data de nascimento do paciente (DD/MM/AAAA): ")
        sexo = input("Digite o sexo do paciente (M/F): ")
        peso = float(input("Digite o peso do paciente (em kg): "))
        altura = float(input("Digite a altura do paciente (em metros): "))

        paciente = Paciente(
            id_paciente=id_paciente,
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            sexo=sexo,
            peso=peso,
            altura=altura
        )

        # Adicionando o paciente ao banco de dados
        self.pacientes_db.adicionar_linha(paciente())
        self.pacientes_db.salvar()

        print(f"Paciente {nome} cadastrado com sucesso!")

    def cadastrar_radiofarmaco(self):
        id_radiofarmaco = input("Digite o ID do radiofármaco: ")
        princp_ativo = input("Digite o princípio ativo do radiofármaco: ")
        concentracao = input("Digite a concentração do radiofármaco: ")
        data_fabricacao = input("Digite a data de fabricação do radiofármaco (DD/MM/AAAA): ")

        radiofarmaco = Radiofarmaco(
            id_radiofarmaco=id_radiofarmaco,
            princp_ativo=princp_ativo,
            concentracao=concentracao,
            data_fabricacao=data_fabricacao
        )

        # Adicionando o radiofármaco ao banco de dados
        self.radiofarmacos_db.adicionar_linha(radiofarmaco())
        self.radiofarmacos_db.salvar()

        print(f"Radiofármaco {id_radiofarmaco} cadastrado com sucesso!")

    def cadastrar_exame(self):
        id_exame = input("Digite o ID do exame: ")
        tipo = input("Digite o tipo do exame: ")
        data = input("Digite a data do exame (DD/MM/AAAA): ")
        id_paciente = input("Digite o ID do paciente: ")
        id_funcionario = input("Digite o ID do funcionário: ")
        id_consulta = input("Digite o ID da consulta: ")
        id_radiofarmaco = input("Digite o ID do radiofármaco: ")

        exame = Exame(
            id_exame=id_exame,
            tipo=tipo,
            data=data,
            id_paciente=id_paciente,
            id_funcionario=id_funcionario,
            id_consulta=id_consulta,
            id_radiofarmaco=id_radiofarmaco
        )

        # Adicionando o exame ao banco de dados
        self.exames_db.adicionar_linha(exame())
        self.exames_db.salvar()

        print(f"Exame {id_exame} cadastrado com sucesso!")

    def agendar_consulta(self):
        id_consulta = input("Digite o ID da consulta: ")
        id_paciente = input("Digite o ID do paciente: ")
        data = input("Digite a data da consulta (DD/MM/AAAA): ")
        id_funcionario = input("Digite o ID do funcionário: ")
        procedimento = input("Digite o procedimento da consulta: ")

        consulta = Consulta(
            id_consulta=id_consulta,
            id_paciente=id_paciente,
            data=data,
            id_funcionario=id_funcionario,
            procedimento=procedimento
        )

        # Adicionando a consulta ao banco de dados
        self.consultas_db.adicionar_linha(consulta.__dict__)
        self.consultas_db.salvar()

        print(f"Consulta {id_consulta} agendada com sucesso!")
    
    
    def cadastrar_funcionario(self):
        os.system("cls" if os.name == "nt" else "clear")  # limpar terminal
        id_funcionario = input("Digite o ID do funcionário: ")
        nome = input("Digite o nome completo do funcionário: ")
        cargo = input("Digite o cargo do funcionário: ")
        n_doc = input("Digite o número do documento do funcionário: ")

        funcionario = Funcionario(
            id_funcionario=id_funcionario,
            nome=nome,
            cargo=cargo,
            n_doc=n_doc,   
        )

        # Adicionando o funcionário ao banco de dados
        self.funcionarios_db.adicionar_linha(funcionario())
        self.funcionarios_db.salvar()

        print(f"Funcionário {nome} cadastrado com sucesso!")