import tkinter as tk
from tkinter import ttk, messagebox
from concurrent.futures import ThreadPoolExecutor
from controllers.coleta_dados import coletar_dados_locais
from controllers.exportacao import exportar_resultados
from controllers.conexao import ConexaoSQLServer, ConexaoOracle
from views.questionario import Questionnaire

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

class AvaliacaoGUI:
    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.root = tk.Tk()
        self.configure_styles()
        self.current_window = self.root
        self.root.resizable(False, False)
        self.login()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", foreground="black", background="#F0F0F0", font=("Arial", 12, "bold"))
        style.configure("TButton", foreground="white", background="#FFA500", font=("Arial", 10, "bold"), padding=10)
        style.map("TButton", background=[("active", "#FF7F00")])

    def login(self):
        self.root.title("Login")
        self.root.configure(bg="#F0F0F0")
        center_window(self.root, 260, 200)

        ttk.Label(self.root, text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.usuario = ttk.Entry(self.root)
        self.usuario.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.root, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.senha = ttk.Entry(self.root, show="*")
        self.senha.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.error_label = ttk.Label(self.root, text="", foreground="red", background="#F0F0F0", font=("Arial", 10))
        self.error_label.grid(row=3, column=0, columnspan=2)

        ttk.Button(self.root, text="Entrar", cursor="hand2", command=self.validar_credenciais).grid(row=4, column=1, padx=10, pady=10)

    def validar_credenciais(self):
        usuario = self.usuario.get()
        senha = self.senha.get()

        if usuario == "infracigam" and senha == "@zyba.@":
            self.root.withdraw()
            self.create_widgets()
        else:
            self.error_label.config(text="Usuário ou senha inválidos!")

    def create_widgets(self):
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Avaliação de Servidores - CIGAM")
        self.main_window.geometry("400x300")
        self.main_window.configure(bg="#CFCFCF")
        self.main_window.resizable(False, False)
        self.main_window.grid_columnconfigure(0, weight=1, uniform="equal")
        self.main_window.grid_rowconfigure(0, weight=0)
        self.main_window.grid_rowconfigure(1, weight=1)
        self.main_window.grid_rowconfigure(2, weight=1)
        self.main_window.grid_rowconfigure(3, weight=1)
        center_window(self.main_window, 400, 300)
        self.current_window = self.main_window

        ttk.Label(self.main_window, text="AVALIADOR DE AMBIENTE").grid(row=0, column=0, pady=5)
        ttk.Button(self.main_window, text="INICIAR AVALIAÇÃO", cursor="hand2", command=self.iniciar_avalicao).grid(row=2, column=0, padx=10, pady=5)

        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def iniciar_avalicao(self):
        self.main_window.withdraw()
        Questionnaire(self)

    def on_close(self):
        self.executor.shutdown(wait=True)
        if hasattr(self, 'main_window'):
            self.main_window.destroy()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

class AvaliacaoServidor:
    def __init__(self, app):
        self.app = app
        self.tarefa_coleta()

    def tarefa_coleta(self):
        try:
            servidor = coletar_dados_locais()
            exportar_resultados(servidor, janela=self.app.current_window)
        except Exception as e:
            erro = str(e)
            self.app.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {erro}"))

class BancoConexaoGUI:
    def __init__(self, app, conexoes, dados_questionario=None):
        self.app = app
        self.conexoes = conexoes
        self.dados_questionario = dados_questionario  # Recebe os dados do questionário
        self.window = tk.Toplevel(self.app.root)
        self.window.title("Conectar ao Banco de Dados")
        self.window.geometry("300x300")
        self.window.configure(bg="#CFCFCF")
        self.window.resizable(False, False)
        center_window(self.window, 300, 300)
        self.app.current_window = self.window
        self.btn_avaliar_oracle_database = None
        self.btn_avaliar_sql_server = None
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.window, text="Escolha o Banco de Dados").pack(pady=10)
        ttk.Button(self.window, text="Conectar no SQL Server", cursor="hand2", command=self.conectar_sql_server).pack(pady=10)
        ttk.Button(self.window, text="Conectar no Oracle", cursor="hand2", command=self.conectar_oracle).pack(pady=10)

    def conectar_sql_server(self):
        self.window.withdraw()
        self.sqlGUI()

    def sqlGUI(self):
        self.sql_window = tk.Toplevel(self.app.root)
        self.sql_window.title("SQL Server")
        self.sql_window.geometry("400x400")
        self.sql_window.configure(bg="#CFCFCF")
        self.sql_window.resizable(False, False)
        center_window(self.sql_window, 400, 400)
        self.sql_window.grab_set()
        self.app.current_window = self.sql_window

        frame_sql = ttk.LabelFrame(self.sql_window, text="Conexão SQL Server", padding=10)
        frame_sql.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_sql, text="Servidor SQL Server:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_server = ttk.Entry(frame_sql)
        entry_server.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_sql, text="Banco de Dados:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_database = ttk.Entry(frame_sql)
        entry_database.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_sql, text="Usuário:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_user = ttk.Entry(frame_sql)
        entry_user.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_sql, text="Senha:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_password = ttk.Entry(frame_sql, show="*")
        entry_password.grid(row=3, column=1, padx=5, pady=5)

        def conectar():
            servidor = entry_server.get()
            database = entry_database.get()
            usuario = entry_user.get()
            senha = entry_password.get()
            try:
                conexao = ConexaoSQLServer()
                validar_conexao = conexao.conectar(servidor, database, usuario, senha)
                self.conexoes["sql_server"] = conexao
                if validar_conexao:
                    self.btn_avaliar_sql_server = ttk.Button(
                        frame_sql, text="Avaliar Banco SQL Server", cursor="hand2", command=lambda: self.on_avaliar_sql_server(conexao, database)
                    )
                    self.btn_avaliar_sql_server.grid(row=5, columnspan=2, pady=10)
            except Exception as e:
                erro = str(e)
                self.app.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao conectar ao SQL Server: {erro}"))

        ttk.Button(frame_sql, text="Conectar", cursor="hand2", command=conectar).grid(row=4, column=0, columnspan=2, pady=10)

    def on_avaliar_sql_server(self, conexao, database):
        self.btn_avaliar_sql_server.destroy()
        loading_window = tk.Toplevel(self.app.root)
        loading_window.title("Carregando")
        loading_window.geometry("300x100")
        loading_window.configure(bg="#CFCFCF")
        loading_window.resizable(False, False)
        loading_window.attributes("-topmost", True)  # Fica na frente
        center_window(loading_window, 300, 100)
        ttk.Label(loading_window, text="A avaliação está sendo realizada...", font=("Arial", 12)).pack(pady=20)
        self.app.current_window = loading_window

        self.app.executor.submit(self.finalizar_avaliacao_sql, loading_window, conexao, database)

    def finalizar_avaliacao_sql(self, loading_window, conexao, database):
        try:
            banco = conexao.executar_script_sql("controllers/scripts/sql_server.sql", database=database)
            servidor = coletar_dados_locais()
            loading_window.destroy()
            self.sql_window.destroy()
            self.app.current_window = self.app.root
            exportar_resultados((banco, servidor), janela=self.app.current_window, dados_questionario=self.dados_questionario)
        except Exception as e:
            erro = str(e)
            loading_window.destroy()
            self.app.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {erro}"))

    def conectar_oracle(self):
        self.window.withdraw()
        self.oracleGUI()

    def oracleGUI(self):
        self.oracle_window = tk.Toplevel(self.app.root)
        self.oracle_window.title("Oracle Database")
        self.oracle_window.geometry("400x350")
        self.oracle_window.configure(bg="#CFCFCF")
        self.oracle_window.resizable(False, False)
        center_window(self.oracle_window, 400, 350)
        self.oracle_window.grab_set()
        self.app.current_window = self.oracle_window

        frame_sql = ttk.LabelFrame(self.oracle_window, text="Conexão Oracle Database", padding=10)
        frame_sql.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_sql, text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_user = ttk.Entry(frame_sql)
        entry_user.grid(row=1, column=1, padx=5, pady=5)

        login_options = ["Default", "SYSDBA"]
        role_combobox = ttk.Combobox(frame_sql, values=login_options, width=10)
        role_combobox.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(frame_sql, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_password = ttk.Entry(frame_sql, show="*")
        entry_password.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_sql, text="Host:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_host = ttk.Entry(frame_sql)
        entry_host.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_sql, text="Porta:").grid(row=3, column=3, padx=5, pady=5, sticky="w")
        entry_porta = ttk.Entry(frame_sql, width=6)
        entry_porta.grid(row=3, column=4, padx=4, pady=5)

        ttk.Label(frame_sql, text="Serviço:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        entry_servico = ttk.Entry(frame_sql)
        entry_servico.grid(row=4, column=1, padx=5, pady=5)

        def conectar():
            usuario = entry_user.get()
            senha = entry_password.get()
            host = entry_host.get()
            porta = entry_porta.get()
            servico = entry_servico.get()
            role = role_combobox.get()

            try:
                conexao = ConexaoOracle()
                validar_conexao = conexao.conectar(usuario, senha, host, porta, servico, role)
                self.conexoes["oracle_database"] = conexao
                if validar_conexao:
                    self.btn_avaliar_oracle_database = ttk.Button(
                        frame_sql, text="Avaliar Banco Oracle Database", cursor="hand2", command=lambda: self.on_avaliar_oracle_database(conexao, usuario)
                    )
                    self.btn_avaliar_oracle_database.grid(row=6, columnspan=2, pady=10)
            except Exception as e:
                erro = str(e)
                self.app.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao conectar ao Oracle: {erro}"))

        ttk.Button(frame_sql, text="Conectar", cursor="hand2", command=conectar).grid(row=5, column=0, columnspan=2, pady=10)

    def on_avaliar_oracle_database(self, conexao, usuario):
        self.btn_avaliar_oracle_database.destroy()
        loading_window = tk.Toplevel(self.app.root)
        loading_window.title("Carregando")
        loading_window.geometry("300x100")
        loading_window.configure(bg="#CFCFCF")
        loading_window.resizable(False, False)
        loading_window.attributes("-topmost", True)  # Fica na frente
        center_window(loading_window, 300, 100)
        ttk.Label(loading_window, text="A avaliação está sendo realizada...", font=("Arial", 12)).pack(pady=20)
        self.app.current_window = loading_window

        self.app.executor.submit(self.finalizar_avaliacao_oracle, loading_window, conexao, usuario)

    def finalizar_avaliacao_oracle(self, loading_window, conexao, usuario):
        try:
            banco = conexao.executar_script_oracle("controllers/scripts/oracle.sql", usuario)
            servidor = coletar_dados_locais()
            loading_window.destroy()
            self.oracle_window.destroy()
            self.app.current_window = self.app.root
            exportar_resultados((banco, servidor), janela=self.app.current_window, dados_questionario=self.dados_questionario)
        except Exception as e:
            erro = str(e)
            loading_window.destroy()
            self.app.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {erro}"))