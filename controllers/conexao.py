import re
import pyodbc
import oracledb
import os
import logging
from pathlib import Path
from views.interface import exibir_alerta_erro, exibir_alerta_concluido
from models.banco import Banco

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validar_arquivo(script_path):
    if not Path(script_path).exists():
        exibir_alerta_erro(f"Arquivo não encontrado: {script_path}")
        return False
    return True
    
def ler_arquivo(script_path):
    with Path(script_path).open(encoding="utf-8") as file:
        return file.read()
    
def log_erro(mensagem, erro):
    exibir_alerta_erro(f"{mensagem}: {erro}")
    logging.error(f"{mensagem}: {erro}")

    return True

class ConexaoSQLServer:
    def __init__(self):
        self.conexao = None

    def conectar(self, server, database, user, password):
        if not all([server, database, user, password]):
            exibir_alerta_erro("Parâmetros de conexão incompletos.")
            return False
        
        try:
            self.conexao = pyodbc.connect(
                f"DRIVER={{SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={user};"
                f"PWD={password}"
            )
            exibir_alerta_concluido("Conexão SQL Server bem-sucedida!")
            logging.info("Conexão estabelecida com o SQL Server.")
            return True
        except pyodbc.Error as e:
            log_erro("Erro ao conectar ao SQL Server", e)
            return False

    def executar_script_sql(self, script_path, database):
        if not validar_arquivo(script_path):
            return None

        try:
            sql_script = ler_arquivo(script_path)
        except Exception as e:
            log_erro("Erro ao ler o arquivo", e)
            return None

        cursor = self.conexao.cursor()
        self._inicializar_atributos()

        try:
            for comando in sql_script.split(";"):
                self._processar_comando(cursor, comando.strip())
            logging.info("Script SQL executado com sucesso.")
        except pyodbc.Error as e:
            log_erro("Erro ao executar o script", e)
            return None

        return Banco(database, self.versao, self.memoria_min, self.memoria_max, self.datafile, self.logfile, self.tabelas_pesadas, tipo="SQLServer")

    def desconectar(self):
        if self.conexao:
            self.conexao.close()
            logging.info("Conexão com o SQL Server encerrada.")
            
    def _log_erro(self, mensagem, erro):
        exibir_alerta_erro(f"{mensagem}: {erro}")
        logging.error(f"{mensagem}: {erro}")

    def _validar_conexao_e_arquivo(self, script_path):
        if not self.conexao:
            exibir_alerta_erro("Conexão não estabelecida.")
            return False

        if not Path(script_path).exists():
            exibir_alerta_erro(f"Arquivo não encontrado.: {script_path}")
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
            self._processar_memoria(resultados)
        elif "EXEC sp_helpfile" in comando:
            self._processar_armazenamento(resultados)
        elif "TOP 5" in comando:
            self._processar_tabelas_pesadas(resultados)

    def _processar_versao(self, resultados):
        self.versao = " ".join(str(campo) for campo in resultados[0])

    def _processar_memoria(self, resultados):
        for linha in resultados:
            nome = linha[0]
            valor = float(linha[1]) / 1024
            if "min server memory" in nome:
                self.memoria_min = f"{valor} GB"
            elif "max server memory" in nome:
                self.memoria_max = "Ilimitada" if valor > 300 else f"{valor} GB"

    def _processar_armazenamento(self, resultados):
        for linha in resultados:
            uso_arquivo = linha[2].lower()
            tamanho_em_gb = float(re.sub(r'\D', '', linha[4])) / 1_000_000
            if ".mdf" in uso_arquivo:
                self.datafile = f"{round(tamanho_em_gb, 2)} GB"
            elif ".ldf" in uso_arquivo:
                self.logfile = f"{round(tamanho_em_gb, 2)} GB"

    def _processar_tabelas_pesadas(self, resultados):
        for linha_comando in resultados:
            tabela_nome = linha_comando[0]
            qnt_linhas = linha_comando[1]
            total_espaco = linha_comando[2]
            self.tabelas_pesadas[tabela_nome] = (qnt_linhas, total_espaco)

class ConexaoOracle:
    def __init__(self):
        self.conexao = None

    def conectar(self, user, password, host, port, service, role):
        if not all([user, password, host, port, service]):
            exibir_alerta_erro("Parâmetros de conexão incompletos.")
            return False
        dsn = f"{host}/{service}"
        mode = oracledb.SYSDBA if role == 'SYSDBA' else oracledb.AUTH_MODE_DEFAULT
        try:
            oracle_home = os.getenv("ORACLE_HOME") or os.getenv("PATH")
            if oracle_home:
                for path in oracle_home.split(";"):
                    if "client" in path.lower():
                        oracledb.init_oracle_client(lib_dir=path)
                        break
            self.conexao = oracledb.connect(user=user, password=password, port=port, dsn=dsn, mode=mode)
            exibir_alerta_concluido("Conexão Oracle bem-sucedida!")
            logging.info("Conexão estabelecida com o Oracle.")
            return True
        except oracledb.Error as e:
            exibir_alerta_erro(f"Erro ao conectar ao Oracle: {e}")
            logging.error(f"Erro ao conectar ao Oracle: {e}")
            return False
        
    def executar_script_oracle(self, script_path, user):
        if not validar_arquivo(script_path):
            return None
        try:
            sql_script = ler_arquivo(script_path)
        except Exception as e:
            log_erro("Erro ao ler o arquivo", e)
            return None
        cursor = self.conexao.cursor()
        self._inicializar_atributos()

        try:
            for comando in sql_script.split(";"):
                self._processar_comando(cursor, comando.strip())
            logging.info("Script SQL executado com sucesso.")
        except oracledb.Error as e:
            log_erro("Erro ao executar o script", e)
            return None
        return Banco(usuario=user, versao=self.versao, sga=self.sga, pga=self.pga, armazenamento=self.armazenamento, tabelas_pesadas=self.tabelas_pesadas, tipo="Oracle")

    def desconectar(self):
        if self.conexao:
            self.conexao.close()
            logging.info("Conexão com o Oracle Database encerrada.")

    def _inicializar_atributos(self):
        self.versao = None
        self.sga = None
        self.pga = None
        self.armazenamento = None
        self.tabelas_pesadas = {}

    def _processar_comando(self, cursor, comando):
        if not comando:
            return
        
        cursor.execute(comando)
        resultados = cursor.fetchall()

        if "product_component_version" in comando:
            self._processar_versao(resultados)
        elif "V$PARAMETER" in comando:
            self._processar_memoria(resultados)
        elif "tablespace_name" in comando:
            self._processar_armazenamento(resultados)
        elif "table_name" in comando:
            self._processar_tabelas_pesadas(resultados)

    def _processar_versao(self, resultados):
        for linha in resultados:
            self.versao = linha[0]

    def _processar_memoria(self, resultados):
        for linha in resultados:
            nome = linha[0]
            valor = int(linha[1])
            if "sga_target" in nome:
                self.sga = f"{round(valor / 1_000_000_000, 2)} GB"
            elif "pga_aggregate_target" in nome:
                self.pga = f"{round(valor / 1_000_000_000, 2)} GB"

    def _processar_armazenamento(self, resultados):
        for linha in resultados:
            self.armazenamento = f'{round(float(linha[1]), 2)} GB'

    def _processar_tabelas_pesadas(self, resultados):
        for linha_comando in resultados:
            tabela_nome = linha_comando[0]
            total_espaco = float(linha_comando[1])
            qnt_linhas = linha_comando[2]
            
            total_espaco = 0 if total_espaco < 1 else total_espaco
                
            self.tabelas_pesadas[tabela_nome] = (qnt_linhas, total_espaco)
            