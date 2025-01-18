import os
import webbrowser

def exportar_para_html(servidor):
    with open('assets/template.html', 'r', encoding='utf-8') as template_file:
        template = template_file.read()
    
    discos_html = "".join(
        f"<li><strong>{nome}</strong>: {info}</li>"
        for nome, info in servidor.discos.items()
    )
    
    html_content = template.format(
        hostname=servidor.hostname,
        cpu=servidor.cpu,
        ano = servidor.ano,
        nucleos = servidor.nucleos,
        threads = servidor.threads,
        ram=servidor.ram,
        rede = servidor.rede,
        discos=discos_html,
        sistema_operacional=servidor.sistema_operacional
    )
    
    with open('assets/relatorio_servidor.html', 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)
    
    webbrowser.open('file://' + os.path.realpath('assets/relatorio_servidor.html'))