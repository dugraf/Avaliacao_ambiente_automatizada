class Servidor:
    def __init__(self, hostname, cpu, ano, ram, discos, sistema_operacional):
        self.hostname = hostname
        self.cpu = cpu
        self.ano = ano
        self.ram = ram
        self.discos = discos
        self.sistema_operacional = sistema_operacional

    def __str__(self):
        return (f"Hostname: {self.hostname}\n"
                f"CPU: {self.cpu}\n"
                f"Ano do processador: {self.ano}\n"
                f"RAM: {self.ram}\n"
                f"Discos: {self.discos}\n"
                f"Sistema Operacional: {self.sistema_operacional}")
