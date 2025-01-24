import os
from tkinter import messagebox
import webbrowser
from collections import defaultdict

def exportar_para_html(obj):
    
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
            
        webbrowser.open('file://' + os.path.realpath('assets/relatorio_servidor.html'))
        
    elif hasattr(obj, 'datafile'):
        # Ler o template HTML
        with open('assets/template_banco.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()
            
        # Geração de uma tabela para tabelas pesadas
        tabelas_html = "".join(
            f"<tr><td>{nome}</td><td>{info[0]}</td><td>{info[1]}</td></tr>"
            for nome, info in obj.tabelas_pesadas.items()
        )
        
        tabelas_html = f"""
        <table border="1" style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr>
                    <th>Nome da Tabela</th>
                    <th>Quantidade de Linhas</th>
                    <th>Espaço Total (MB)</th>
                </tr>
            </thead>
            <tbody>
                {tabelas_html}
            </tbody>
        </table>
        """
        
        dados = defaultdict(str, {
            'nome_database': obj.nome_database,
            'versao': obj.versao,
            'memoria_min': obj.memoria_min,
            'memoria_max': obj.memoria_max,
            'datafile': obj.datafile,
            'logfile': obj.logfile,
            'tabelas_pesadas': tabelas_html
        })
        
        # Gerar o HTML final, preenchendo as variáveis
        html_content = template.format_map(dados)
        with open('assets/relatorio_banco.html', 'w', encoding='utf-8') as output_file:
            output_file.write(html_content)
            
        webbrowser.open('file://' + os.path.realpath('assets/relatorio_banco.html'))
