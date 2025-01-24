import tkinter as tk
from tkinter import ttk, messagebox
from concurrent.futures import ThreadPoolExecutor
from controllers.coleta_dados import coletar_dados_locais
from controllers.exportacao import exportar_para_html
from controllers.conexao import ConexaoSQLServer, ConexaoOracle

class AvaliacaoGUI:
    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.root = tk.Tk()
        self.root.title("Avaliação de Servidores - CIGAM")
        self.root.geometry("400x300")
        self.root.configure(bg="#CFCFCF")
        self.conexoes = {}

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", foreground="black", background="#CFCFCF", font=("Arial", 14, "bold"))
        style.configure("TButton", foreground="white", background="#FFA500", font=("Arial", 10, "bold"), padding=10)
        style.map("TButton", background=[("active", "#FF7F00")])

    def create_widgets(self):
        ttk.Label(self.root, text="Avaliação de Servidor Local").pack(pady=20)
        ttk.Button(self.root, text="Coletar Dados", command=self.iniciar_coleta).pack(pady=10)
        ttk.Button(self.root, text="Conectar ao Banco de Dados", command=self.conectar_banco).pack(pady=10)

    def iniciar_coleta(self):
        def tarefa_coleta():
            try:
                servidor = coletar_dados_locais()
                exportar_para_html(servidor)
                messagebox.showinfo("Sucesso", "Dados coletados e exportados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro durante a coleta de dados: {str(e)}")
        
        self.executor.submit(tarefa_coleta)

    def conectar_banco(self):
        BancoConexaoGUI(self.root, self.conexoes)

    def run(self):
        self.root.mainloop()

class BancoConexaoGUI:
    def __init__(self, parent, conexoes):
        self.parent = parent
        self.conexoes = conexoes
        self.window = tk.Toplevel(self.parent)
        self.window.title("Conectar ao Banco de Dados")
        self.window.geometry("300x300")
        self.window.configure(bg="#CFCFCF")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.window, text="Escolha o Banco de Dados").pack(pady=10)
        ttk.Button(self.window, text="Conectar no SQL Server", command=self.conectar_sql_server).pack(pady=10)
        ttk.Button(self.window, text="Conectar no Oracle", command=self.conectar_oracle).pack(pady=10)

    def conectar_sql_server(self):
        self.sqlGUI()
        
    def sqlGUI(self):
        window_sql = tk.Toplevel(self.parent)
        window_sql.title("Sql Server")
        window_sql.geometry("400x400")
        window_sql.configure(bg="#CFCFCF")
               
        frame_sql = ttk.LabelFrame(window_sql, text="Conexão SQL Server", padding=10)
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
                if validar_conexao is True:
                    btn_avaliar_sql_server = ttk.Button(
                        frame_sql, text="Avaliar Banco SQL Server", command=lambda: on_avaliar_sql_server()
                    )
                    btn_avaliar_sql_server.grid(row=5, columnspan=2, pady=10)
                def on_avaliar_sql_server():
                    try:
                        banco = conexao.executar_script_sql("controllers/scripts/sql_server.sql", database=database)
                        exportar_para_html(banco)
                        messagebox.showinfo("Sucesso", "Dados coletados e exportados com sucesso!")
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro durante a coleta de dados: {str(e)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao conectar ao SQL Server: {str(e)}")

        ttk.Button(frame_sql, text="Conectar", command=conectar).grid(row=4, column=0, columnspan=2, pady=10)

    def conectar_oracle(self):
        conexao = ConexaoOracle()
        conexao.conectar("user", "pass", "dsn")
        self.conexoes["oracle"] = conexao