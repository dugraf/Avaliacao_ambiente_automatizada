import os
from time import sleep
from tkinter import messagebox
import webbrowser
from collections import defaultdict

TEMPO_SLEEP = 1

def exportar_para_html(obj, janela):
    
    if hasattr(obj, 'discos'):
        # Ler o template HTML
        with open('assets/template_servidor.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()
            
        # Dados dos discos
        discos_html = "".join(
            f"<li><strong>{nome}</strong>: {info}</li>"
            for nome, info in obj.discos.items()
        )

        # Dicionário com os dados a serem inseridos no template
        dados = defaultdict(str, {
            'hostname': obj.hostname,
            'cpu': obj.cpu,
            'ano': obj.ano,
            'str': obj.str,
            'nucleos': obj.nucleos,
            'threads': obj.threads,
            'ram': obj.ram,
            'rede': obj.rede,
            'discos': discos_html,
            'sistema_operacional': obj.sistema_operacional
        })
        # Gerar o HTML final, preenchendo as variáveis
        html_content = template.format_map(dados)
        with open('assets/relatorio_servidor.html', 'w', encoding='utf-8') as output_file:
            output_file.write(html_content)
        
        exportacao_sucesso(janela)
        webbrowser.open('file://' + os.path.realpath('assets/relatorio_servidor.html'))
        
    elif hasattr(obj, 'tipo') and obj.tipo == "SQLServer":
        # Ler o template HTML específico para SQLServer
        with open('assets/template_banco.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()
            
        tabelas_html = "".join(
            f"<tr><td>{nome}</td><td>{info[0]}</td><td>{info[1]}</td></tr>"
            for nome, info in obj.tabelas_pesadas.items()
        )
        
        tabelas_html = tabela(tabelas_html)
        
        dados = defaultdict(str, {
            'banco' : 'SQL SERVER',
            'nome_database_ou_user' : 'Database',
            'database': obj.nome_database,
            'versao': obj.versao,
            'memoria_info_1': obj.memoria_min,
            'memoria_info_2': obj.memoria_max,
            'datafile': obj.datafile,
            'logfile': obj.logfile,
            'tabelas_pesadas': tabelas_html,
            'tamanho_log': 'Tamanho do log:',
            'memoria_1': 'Memória mínima dedicada ao banco:',
            'memoria_2': 'Memória máxima dedicada ao banco:'
        })
        
        html_content = template.format_map(dados)
        with open('assets/relatorio_banco.html', 'w', encoding='utf-8') as output_file:
            output_file.write(html_content)
        
        exportacao_sucesso(janela)
        webbrowser.open('file://' + os.path.realpath('assets/relatorio_banco.html'))
    
    elif hasattr(obj, 'tipo') and obj.tipo == "Oracle":
        # Ler o template HTML específico para Oracle
        with open('assets/template_banco.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()
        
        tabelas_html = "".join(
            f"<tr><td>{nome}</td><td>{info[0]}</td><td>{info[1]}</td></tr>"
            for nome, info in obj.tabelas_pesadas.items()
        )
        
        tabelas_html = tabela(tabelas_html)
        
        dados = defaultdict(str, {
            'banco' : 'Oracle',
            'nome_database_ou_user' : 'Usuário',
            'database': obj.usuario,
            'versao': obj.versao,
            'memoria_info_1': obj.sga,
            'memoria_info_2': obj.pga,
            'datafile': obj.armazenamento,
            'tabelas_pesadas': tabelas_html,
            'memoria_1': 'SGA:',
            'memoria_2': 'PGA:'
        })
        
        html_content = template.format_map(dados)
        with open('assets/relatorio_banco.html', 'w', encoding='utf-8') as output_file:
            output_file.write(html_content)
       
        exportacao_sucesso(janela)
        webbrowser.open('file://' + os.path.realpath('assets/relatorio_banco.html'))
    else:
        messagebox.showerror("Erro", "Objeto não reconhecido ou inválido.")
        
def exportacao_sucesso(janela):
    janela.after(0, lambda: messagebox.showinfo("Sucesso", "Dados coletados e exportados com sucesso!"))
    sleep(TEMPO_SLEEP)

def tabela(tabela):
    return f"""
        <table border="1" style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr>
                    <th>Nome da Tabela</th>
                    <th>Quantidade de Linhas</th>
                    <th>Espaço Total (GB)</th>
                </tr>
            </thead>
            <tbody>
                {tabela}
            </tbody>
        </table>
        """