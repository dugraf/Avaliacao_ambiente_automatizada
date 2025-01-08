import os
import webbrowser
from views.interface import exibir_alerta_concluido

def exportar_para_html(servidor):
    with open('assets/template.html', 'r') as template_file:
        template = template_file.read()
    
    discos_html = "".join(
        f"<li><strong>{nome}</strong>: {info}</li>"
        for nome, info in servidor.discos.items()
    )
    
    html_content = template.format(
        hostname=servidor.hostname,
        cpu=servidor.cpu,
        ano = servidor.ano,
        ram=servidor.ram,
        discos=discos_html,
        sistema_operacional=servidor.sistema_operacional
    )
    
    with open('assets/relatorio_servidor.html', 'w') as output_file:
        output_file.write(html_content)
    
    exibir_alerta_concluido("✅ Relatório gerado: relatorio_servidor.html")
    webbrowser.open('file://' + os.path.realpath('assets/relatorio_servidor.html'))