class Banco:
    def __init__(self, nome_database, versao, memoria_min, memoria_max, datafile, logfile, tabelas_pesadas):
        self.nome_database = nome_database
        self.versao = versao
        self.memoria_min = memoria_min
        self.memoria_max = memoria_max
        self.datafile = datafile
        self.logfile = logfile
        self.tabelas_pesadas = tabelas_pesadas

    def __str__(self):
        return (f"Nome da Database: {self.nome_database}\n"
                f"Versão do Banco de Dados: {self.versao}\n"
                f"Memória mínima dedicada ao Banco de Dados: {self.memoria_min}\n"
                f"Memória máxima dedicada ao Banco de Dados: {self.memoria_max}\n"
                f"Tamanho da Base de Dados: {self.datafile}\n"
                f"Tamanho do Arquivo Log: {self.logfile}\n"
                f"Tabelas mais pesadas: {self.tabelas_pesadas}\n")