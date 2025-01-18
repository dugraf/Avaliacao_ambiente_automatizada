import psutil
import platform
import socket
import cpuinfo
import re
from models.servidor import Servidor
from utils.logger import log_erro
from views.interface import exibir_alerta_erro
from scraper.scraper import Scraper

def coletar_dados_locais():
    try:
        hostname = socket.gethostname()
    except Exception as e:
        hostname = "Erro ao coletar hostname"
        exibir_alerta_erro(f"⚠️ Erro ao coletar hostname: {e}")
        log_erro(f"Erro ao coletar hostname: {e}")
    
    try:
        cpu = cpuinfo.get_cpu_info()['brand_raw']
    except Exception as e:
        cpu = "Erro ao coletar CPU"
        exibir_alerta_erro(f"⚠️ Erro ao coletar CPU: {e}")
        log_erro(f"Erro ao coletar CPU: {e}")
        
    try:       
        scraper = Scraper()
        buscar_ano_cpu = scraper.search(query=cpu, limit=1)[0][0]
        ano = re.search(r"\d{4}", buscar_ano_cpu.get("date")).group()
    except Exception as e:
        ano = "Erro ao coletar ano do processador"
        exibir_alerta_erro(f"⚠️ Erro ao coletar ano do processador: {e}")
        log_erro(f"Erro ao coletar ano do processador: {e}")
        
    try:
        nucleos = cpuinfo.get_cpu_info()['count']
    except Exception as e:
        nucleos = "Erro ao coletar a quantidade de núcleos"
        exibir_alerta_erro(f"⚠️ Erro ao coletar quantidade de núcleos: {e}")
        log_erro(f"Erro ao coletar quantidade de núcleos: {e}")
        
    try:
        threads = psutil.cpu_count(logical=True)
    except Exception as e:
        threads = "Erro ao coletar a quantidade de threads"
        exibir_alerta_erro(f"⚠️ Erro ao coletar quantidade de threads: {e}")
        log_erro(f"Erro ao coletar quantidade de threads: {e}")
    
    try:
        ram = f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
    except Exception as e:
        ram = "Erro ao coletar RAM"
        exibir_alerta_erro(f"⚠️ Erro ao coletar RAM: {e}")
        log_erro(f"Erro ao coletar RAM: {e}")
        
    try:
        rede = "MB" if psutil.net_io_counters().bytes_sent < 1e9 else "GB"
    except Exception as e:
        rede = "Erro ao coletar se a rede é GB ou MB"
        exibir_alerta_erro(f"⚠️ Erro ao coletar se a rede é GB ou MB: {e}")
        log_erro(f"Erro ao coletar se a rede é GB ou MB: {e}")
    
    discos = {}
    try:
        for part in psutil.disk_partitions():
            if 'cdrom' not in part.opts and 'removable' not in part.opts:
                try:
                    total = psutil.disk_usage(part.mountpoint).total / (1024**3)
                    livre = psutil.disk_usage(part.mountpoint).free / (1024**3)
                    discos[part.device] = f"{total:.2f} GB ({livre:.2f} GB livres)"
                except Exception as e:
                    discos[part.device] = "Erro ao coletar informações do disco"
                    exibir_alerta_erro(f"⚠️ Erro ao coletar informações do disco {part.device}: {e}")
                    log_erro(f"Erro ao coletar informações do disco {part.device}: {e}")
    except Exception as e:
        discos = {"Erro": "Erro ao listar discos"}
        exibir_alerta_erro(f"⚠️ Erro ao listar discos: {e}")
        log_erro(f"Erro ao listar discos: {e}")
    
    try:
        sistema_operacional = platform.system() + " " + platform.version()
    except Exception as e:
        sistema_operacional = "Erro ao coletar Sistema Operacional"
        exibir_alerta_erro(f"⚠️ Erro ao coletar Sistema Operacional: {e}")
        log_erro(f"Erro ao coletar Sistema Operacional: {e}")
    
    return Servidor(hostname, cpu, ano, nucleos, threads, ram, rede, discos, sistema_operacional)
