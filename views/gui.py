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
        style.configure("TLabel", foreground="black", background="#CFCFCF", font=("Arial", 12, "bold"))
        style.configure("TButton", foreground="white", background="#FFA500", font=("Arial", 10, "bold"), padding=10)
        style.map("TButton", background=[("active", "#FF7F00")])

    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1, uniform="equal")
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        ttk.Label(self.root, text="Avaliação de Servidor Local").grid(row=0, column=0, pady=5)
        ttk.Button(self.root, text="Coletar Dados", cursor="hand2", command=self.iniciar_coleta).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(self.root, text="Conectar ao Banco de Dados", cursor="hand2", command=self.conectar_banco).grid(row=2, column=0, padx=10, pady=5)

    def iniciar_coleta(self):
        def tarefa_coleta():
            try:
                servidor = coletar_dados_locais()
                exportar_para_html(servidor, janela=self.root)

            except Exception as e:
                 self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {str(e)}"))
        
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
        self.btn_avaliar_oracle_database = None
        self.btn_avaliar_sql_server = None
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.window, text="Escolha o Banco de Dados").pack(pady=10)
        ttk.Button(self.window, text="Conectar no SQL Server", cursor="hand2", command=self.conectar_sql_server).pack(pady=10)
        ttk.Button(self.window, text="Conectar no Oracle", cursor="hand2", command=self.conectar_oracle).pack(pady=10)

    def conectar_sql_server(self):
        self.sqlGUI()
        
    def sqlGUI(self):
        window_sql = tk.Toplevel(self.parent)
        window_sql.title("Sql Server")
        window_sql.geometry("400x400")
        window_sql.configure(bg="#CFCFCF")
        window_sql.grab_set()
               
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
                    self.btn_avaliar_sql_server = ttk.Button(
                        frame_sql, text="Avaliar Banco SQL Server", cursor="hand2", command=lambda: on_avaliar_sql_server()
                    )
                    self.btn_avaliar_sql_server.grid(row=5, columnspan=2, pady=10)
                elif validar_conexao is False:
                    self.btn_avaliar_sql_server.grid_forget()
                    
                def on_avaliar_sql_server():
                    self.btn_avaliar_sql_server.destroy()
                    try:
                        banco = conexao.executar_script_sql("controllers/scripts/sql_server.sql", database=database)
                        exportar_para_html(banco, janela=self.window)

                    except Exception as e:
                        self.window.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {str(e)}"))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("Erro", f"Erro ao conectar ao SQL Server: {str(e)}"))

        ttk.Button(frame_sql, text="Conectar", cursor="hand2", command=conectar).grid(row=4, column=0, columnspan=2, pady=10)

    def conectar_oracle(self):
        self.oracleGUI()
        
    def oracleGUI(self):
        window_sql = tk.Toplevel(self.parent)
        window_sql.title("Oracle Database")
        window_sql.geometry("400x350")
        window_sql.configure(bg="#CFCFCF")
        window_sql.grab_set()
               
        frame_sql = ttk.LabelFrame(window_sql, text="Conexão Oracle Database", padding=10)
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
            
            conexao = ConexaoOracle()
            validar_conexao = conexao.conectar(usuario, senha, host, porta, servico, role)
            self.conexoes["oracle_database"] = conexao
            if validar_conexao is True:
                self.btn_avaliar_oracle_database = ttk.Button(
                    frame_sql, text="Avaliar Banco Oracle Database", cursor="hand2", command=lambda: on_avaliar_oracle_database()
                )
                self.btn_avaliar_oracle_database.grid(row=6, columnspan=2, pady=10)
            elif validar_conexao is False:
                self.btn_avaliar_oracle_database.grid_forget()
                
            def on_avaliar_oracle_database():
                self.btn_avaliar_oracle_database.destroy()
                try:
                    banco = conexao.executar_script_oracle("controllers/scripts/oracle.sql", usuario)
                    exportar_para_html(banco, janela=self.window)
                    
                except Exception as e:
                        self.window.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {str(e)}"))


        ttk.Button(frame_sql, text="Conectar", cursor="hand2", command=conectar).grid(row=5, column=0, columnspan=2, pady=10)