from datetime import datetime
from dateutil.relativedelta import (
    relativedelta,
)  # Função que calcula direto a idade em anos, meses e dias.
import pandas as pd
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta

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

    def __init__(self, id_Funcionario: str, nome: str, cargo: str, n_doc: int) -> None:
        self.id = id_Funcionario
        self.nome = nome
        self.cargo = cargo
        self.n_doc = n_doc


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


class Passagem:
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


class BancoDados:
    """
    Classe que modela o banco de dados utilizando dataframes e salvando em .csv
    """

    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.df: pd.DataFrame = pd.DataFrame()
        if not os.path.exists("data"):
            os.makedirs("data")
        self.caminho_arquivo = "data/" + self.nome + ".csv"

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
        linha = pd.DataFrame([linha])
        if self.df.empty:
            self.df = pd.DataFrame(linha)
        elif self.df.columns == linha.keys:
            self.df = pd.concat([self.df,linha])
        else:
            print("Erro: A linha não corresponde ao formato do dataframe.")
            return False

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

    def __call__(self):
        return self.df