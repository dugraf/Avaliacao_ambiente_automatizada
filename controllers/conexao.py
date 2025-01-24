import re
import pyodbc
import cx_Oracle
import logging
from pathlib import Path
from views.interface import exibir_alerta_erro, exibir_alerta_concluido
from models.banco import Banco

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MENSAGEM_CONEXAO_BEM_SUCEDIDA_SQL = "Conexão SQL Server bem-sucedida!"
MENSAGEM_CONEXAO_BEM_SUCEDIDA_ORACLE = "Conexão Oracle bem-sucedida!"
ERRO_CONEXAO_SQL = "Erro ao conectar ao SQL Server"
ERRO_CONEXAO_ORACLE = "Erro ao conectar ao Oracle"
ERRO_LEITURA_ARQUIVO = "Erro ao ler o arquivo"
ERRO_EXECUCAO_SCRIPT = "Erro ao executar o script"
ALERTA_PARAMETROS_INCOMPLETOS = "Parâmetros de conexão incompletos."
ALERTA_ARQUIVO_NAO_ENCONTRADO = "Arquivo não encontrado."
ALERTA_CONEXAO_NAO_ESTABELECIDA = "Conexão não estabelecida."

class ConexaoSQLServer:
    def __init__(self):
        self.conexao = None

    def conectar(self, server, database, user, password):
        if not all([server, database, user, password]):
            exibir_alerta_erro(ALERTA_PARAMETROS_INCOMPLETOS)
            return False
        
        try:
            self.conexao = pyodbc.connect(
                f"DRIVER={{SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={user};"
                f"PWD={password}"
            )
            exibir_alerta_concluido(MENSAGEM_CONEXAO_BEM_SUCEDIDA_SQL)
            logging.info("Conexão estabelecida com o SQL Server.")
            return True
        except pyodbc.Error as e:
            self._log_erro(ERRO_CONEXAO_SQL, e)
            return False

    def executar_script_sql(self, script_path, database):
        if not self._validar_conexao_e_arquivo(script_path):
            return None

        try:
            sql_script = self._ler_arquivo(script_path)
        except Exception as e:
            self._log_erro(ERRO_LEITURA_ARQUIVO, e)
            return None

        cursor = self.conexao.cursor()
        self._inicializar_atributos()

        try:
            for comando in sql_script.split(";"):
                self._processar_comando(cursor, comando.strip())
            logging.info("Script SQL executado com sucesso.")
        except pyodbc.Error as e:
            self._log_erro(ERRO_EXECUCAO_SCRIPT, e)
            return None

        return Banco(database, self.versao, self.memoria_min, self.memoria_max, self.datafile, self.logfile, self.tabelas_pesadas)

    def desconectar(self):
        if self.conexao:
            self.conexao.close()
            logging.info("Conexão com o SQL Server encerrada.")
            
    def _log_erro(self, mensagem, erro):
        exibir_alerta_erro(f"{mensagem}: {erro}")
        logging.error(f"{mensagem}: {erro}")

    def _validar_conexao_e_arquivo(self, script_path):
        if not self.conexao:
            exibir_alerta_erro(ALERTA_CONEXAO_NAO_ESTABELECIDA)
            return False

        if not Path(script_path).exists():
            exibir_alerta_erro(f"{ALERTA_ARQUIVO_NAO_ENCONTRADO}: {script_path}")
            return False

        return True

    def _ler_arquivo(self, script_path):
        with Path(script_path).open(encoding="utf-8") as file:
            return file.read()

    def _inicializar_atributos(self):
        self.versao = None
        self.memoria_min = None
        self.memoria_max = None
        self.datafile = None
        self.logfile = None
        self.tabelas_pesadas = {}

    def _processar_comando(self, cursor, comando):
        if not comando:
            return

        cursor.execute(comando)
        resultados = cursor.fetchall()

        if "@@VERSION" in comando:
            self._processar_versao(resultados)
        elif "sys.configurations" in comando:
            self._processar_configuracoes(resultados)
        elif "EXEC sp_helpfile" in comando:
            self._processar_arquivos(resultados)
        elif "TOP 5" in comando:
            self._processar_tabelas_pesadas(resultados)

    def _processar_versao(self, resultados):
        self.versao = " ".join(str(campo) for campo in resultados[0])

    def _processar_configuracoes(self, resultados):
        for linha in resultados:
            nome = linha[0]
            valor = linha[1]
            if "min server memory" in nome:
                self.memoria_min = f"{valor / 1024} GB"
            elif "max server memory" in nome:
                self.memoria_max = f"{valor / 1024} GB"

    def _processar_arquivos(self, resultados):
        for linha in resultados:
            uso_arquivo = linha[0].lower()
            tamanho_em_mb = float(re.sub(r'\D', '', linha[4])) / 1_000_000
            if "data" in uso_arquivo:
                self.datafile = f"{round(tamanho_em_mb, 2)} GB"
            elif "log" in uso_arquivo:
                self.logfile = f"{round(tamanho_em_mb, 2)} GB"

    def _processar_tabelas_pesadas(self, resultados):
        for linha_comando in resultados:
            tabela_nome = linha_comando[0]
            qnt_linhas = linha_comando[1]
            total_espaco = linha_comando[2]
            self.tabelas_pesadas[tabela_nome] = (qnt_linhas, total_espaco)

class ConexaoOracle:
    def __init__(self):
        self.conexao = None

    def conectar(self, user, password, dsn):
        try:
            self.conexao = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            exibir_alerta_concluido(MENSAGEM_CONEXAO_BEM_SUCEDIDA_ORACLE)
            logging.info("Conexão estabelecida com o Oracle.")
        except cx_Oracle.DatabaseError as e:
            exibir_alerta_erro(f"{ERRO_CONEXAO_ORACLE}: {e}")
            logging.error(f"{ERRO_CONEXAO_ORACLE}: {e}")
