class Servidor:
    def __init__(self, hostname, cpu, ano, str, nucleos, threads, ram, rede, discos, sistema_operacional):
        self.hostname = hostname
        self.cpu = cpu
        self.ano = ano
        self.str = str
        self.nucleos = nucleos
        self.threads = threads
        self.ram = ram
        self.rede = rede
        self.discos = discos
        self.sistema_operacional = sistema_operacional

    def __str__(self):
        return (f"Hostname: {self.hostname}\n"
                f"CPU: {self.cpu}\n"
                f"Ano do processador: {self.ano}\n"
                f"STR: {self.str}\n"
                f"Núcleos: {self.nucleos}\n"
                f"Threads: {self.threads}\n"
                f"RAM: {self.ram}\n"
                f"Rede: {self.rede}\n"
                f"Discos: {self.discos}\n"
                f"Sistema Operacional: {self.sistema_operacional}")
