import tkinter as tk
from tkinter import ttk, messagebox
from controllers.coleta_dados import coletar_dados_locais
from controllers.exportacao import exportar_resultados

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

class Questionnaire:
    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Questionário")
        self.conexoes = {}
        self.window.geometry("500x300")
        self.window.configure(bg="#CFCFCF")
        self.window.resizable(False, False)
        center_window(self.window, 500, 300)
        self.app.current_window = self.window
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.window, text="PREENCHA AS INFORMAÇÕES ABAIXO:").grid(pady=10)
        ttk.Label(self.window, text="Ordem de Serviço:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ordem_servico = ttk.Entry(self.window)
        self.ordem_servico.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.window, text="Nome do Técnico:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.nome_tecnico = ttk.Entry(self.window)
        self.nome_tecnico.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.window, text="Nome do Cliente:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.nome_cliente = ttk.Entry(self.window)
        self.nome_cliente.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.window, text="Número de Usuários:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        validate_cmd = self.window.register(self.validar_entrada)
        self.num_usuarios = ttk.Entry(self.window, validate="key", validatecommand=(validate_cmd, "%P"))
        self.num_usuarios.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.window, text="Versão atual:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.versao = ttk.Entry(self.window)
        self.versao.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.window, text="SOBRE ESTE SERVIDOR:").grid(pady=10)
        opcoes = ["Aplicação, Banco e TS", "Aplicação e Banco", "Aplicação e TS", "Aplicação", "Banco"]
        ttk.Label(self.window, text="O que este servidor está hospedando?").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.tipo_servidor = ttk.Combobox(self.window, values=opcoes, state="readonly")
        self.tipo_servidor.grid(row=7, column=1, padx=5, pady=5)

        ttk.Button(self.window, text="FINALIZAR QUESTIONÁRIO", cursor="hand2", command=self.pergunta_banco).grid(row=8, column=0, padx=10, pady=5)

    def validar_entrada(self, P):
        return P == "" or P.isdigit()

    def get_dados_questionario(self):
        """Retorna os dados preenchidos no questionário como dicionário."""
        return {
            "ordem_servico": self.ordem_servico.get(),
            "nome_tecnico": self.nome_tecnico.get(),
            "nome_empresa": self.nome_cliente.get(),
            "numero_usuarios": self.num_usuarios.get(),
            "versao_cigam": self.versao.get(),
            "hospedagem": self.tipo_servidor.get()
        }

    def pergunta_banco(self):
        self.window.withdraw()
        self.pergunta_window = tk.Toplevel(self.app.root)
        self.pergunta_window.geometry("500x100")
        self.pergunta_window.configure(bg="#CFCFCF")
        self.pergunta_window.resizable(False, False)
        center_window(self.pergunta_window, 500, 100)
        self.app.current_window = self.pergunta_window
        ttk.Label(self.pergunta_window, text="Deseja conectar-se ao banco de dados?").grid(pady=10)
        ttk.Button(self.pergunta_window, text="SIM", cursor="hand2", command=self.conectar_banco).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(self.pergunta_window, text="NÃO", cursor="hand2", command=self.iniciar_coleta).grid(row=1, column=1, padx=10, pady=5)

    def iniciar_coleta(self):
        self.dados_questionario = self.get_dados_questionario()
        self.pergunta_window.withdraw()
        loading_window = tk.Toplevel(self.app.root)
        loading_window.title("Carregando")
        loading_window.geometry("300x100")
        loading_window.configure(bg="#CFCFCF")
        loading_window.resizable(False, False)
        center_window(loading_window, 300, 100)
        ttk.Label(loading_window, text="A avaliação está sendo realizada...", font=("Arial", 12)).pack(pady=20)
        self.app.current_window = loading_window
        self.app.executor.submit(self.finalizar_coleta, loading_window)

    def finalizar_coleta(self, loading_window):
        try:
            servidor = coletar_dados_locais()
            loading_window.destroy()
            self.app.current_window = self.app.root
            exportar_resultados(servidor, janela=self.app.current_window, dados_questionario=self.dados_questionario)
        except Exception as e:
            erro = str(e)
            loading_window.destroy()
            self.app.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {erro}"))

    def conectar_banco(self):
        from views.gui import BancoConexaoGUI
        self.dados_questionario = self.get_dados_questionario()
        self.pergunta_window.destroy()
        BancoConexaoGUI(self.app, self.conexoes, self.dados_questionario)