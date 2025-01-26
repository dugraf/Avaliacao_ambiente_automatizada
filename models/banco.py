class Banco:
    def __init__(self, 
                 nome_database=None, versao=None, memoria_min=None, memoria_max=None, 
                 datafile=None, logfile=None, tabelas_pesadas=None, 
                 usuario=None, sga=None, pga=None, armazenamento=None, tipo = None):
        self.tipo = tipo
        self.versao = versao
        self.tabelas_pesadas = tabelas_pesadas

        if tipo == "SQLServer":
            self.nome_database = nome_database
            self.memoria_min = memoria_min
            self.memoria_max = memoria_max
            self.datafile = datafile
            self.logfile = logfile
        elif tipo == "Oracle":
            self.usuario = usuario
            self.sga = sga
            self.pga = pga
            self.armazenamento = armazenamento

    def __str__(self):
        if self.tipo == "SQLServer":
            return (f"Nome da Database: {self.nome_database}\n"
                    f"Versão: {self.versao}\n"
                    f"Memória Mínima: {self.memoria_min}\n"
                    f"Memória Máxima: {self.memoria_max}\n"
                    f"Datafile: {self.datafile}\n"
                    f"Logfile: {self.logfile}\n"
                    f"Tabelas Pesadas: {self.tabelas_pesadas}\n")
        elif self.tipo == "Oracle":
            return (f"Usuário: {self.usuario}\n"
                    f"Versão: {self.versao}\n"
                    f"SGA: {self.sga}\n"
                    f"PGA: {self.pga}\n"
                    f"Armazenamento: {self.armazenamento}\n"
                    f"Tabelas Pesadas: {self.tabelas_pesadas}\n")
