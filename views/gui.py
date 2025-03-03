import tkinter as tk
from tkinter import ttk, messagebox
from concurrent.futures import ThreadPoolExecutor
from controllers.coleta_dados import coletar_dados_locais
from controllers.exportacao import exportar_para_html
from controllers.conexao import ConexaoSQLServer, ConexaoOracle

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
        self.conexoes = {}
        self.configure_styles()
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

        # Mensagem de erro abaixo do campo de senha
        self.error_label = ttk.Label(self.root, text="", foreground="red", background="#F0F0F0", font=("Arial", 10))
        self.error_label.grid(row=3, column=0, columnspan=2)

        # Botão de login
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
        self.main_window.grid_columnconfigure(0, weight=1, uniform="equal")
        self.main_window.grid_rowconfigure(0, weight=0)
        self.main_window.grid_rowconfigure(1, weight=1)
        self.main_window.grid_rowconfigure(2, weight=1)
        self.main_window.grid_rowconfigure(3, weight=1)
        center_window(self.main_window, 400, 300)

        ttk.Label(self.main_window, text="Avaliação de Servidor Local").grid(row=0, column=0, pady=5)
        ttk.Button(self.main_window, text="Coletar Dados", cursor="hand2", command=self.iniciar_coleta).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(self.main_window, text="Conectar ao Banco de Dados", cursor="hand2", command=self.conectar_banco).grid(row=2, column=0, padx=10, pady=5)
        
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.main_window.mainloop()

    def iniciar_coleta(self):
        AvaliacaoServidor(self.main_window)

    def conectar_banco(self):
        center_window(self.main_window, 400, 300)
        BancoConexaoGUI(self.main_window, self.conexoes)
        
    def on_close(self):
        self.executor.shutdown(wait=True)
        self.main_window.quit()
        self.main_window.destroy()
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        
class AvaliacaoServidor:
    def __init__(self, parent):
        self.parent = parent
        self.tarefa_coleta()
        
    def tarefa_coleta(self):
        try:
            servidor = coletar_dados_locais()
            exportar_para_html(servidor, janela=self.parent)

        except Exception as e:
            self.parent.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a coleta de dados: {str(e)}"))
        
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