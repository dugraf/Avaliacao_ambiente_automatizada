import logging

logging.basicConfig(
    filename='logs/erros.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_erro(mensagem):
    logging.error(mensagem)
