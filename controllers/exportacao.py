import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
from controllers.gerar_documento import gerar_documento

def exportar_resultados(obj, janela, dados_questionario=None):
    if isinstance(obj, tuple) and len(obj) == 2:
        banco, servidor = obj
        if hasattr(banco, 'tipo') and banco.tipo == "SQLServer":
            ResultadosGUI(janela, tipo="SQLServer", banco=banco, servidor=servidor, dados_questionario=dados_questionario)
        elif hasattr(banco, 'tipo') and banco.tipo == "Oracle":
            ResultadosGUI(janela, tipo="Oracle", banco=banco, servidor=servidor, dados_questionario=dados_questionario)
    elif hasattr(obj, 'discos'):
        ResultadosGUI(janela, tipo="Servidor", servidor=obj, dados_questionario=dados_questionario)
    else:
        messagebox.showerror("Erro", "Objeto não reconhecido ou inválido.")

class ResultadosGUI:
    def __init__(self, parent, tipo, banco=None, servidor=None, dados_questionario=None):
        self.parent = parent
        self.tipo = tipo
        self.banco = banco
        self.servidor = servidor
        self.dados_questionario = dados_questionario
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Resultados - {self.tipo}")
        self.window.state('zoomed')
        self.window.resizable(True, True)
        self.window.configure(bg="#f4f4f9")
        self.configure_styles()
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("MainTitle.TLabel", font=("Arial", 20, "bold"), foreground="#4CAF50", background="#f4f4f9")
        style.configure("SectionTitle.TLabel", font=("Arial", 16, "bold"), foreground="#555", background="#fff")
        style.configure("Data.TLabel", font=("Arial", 14), foreground="#333", background="#fff", padding=5)
        style.configure("ListItem.TLabel", font=("Arial", 14), foreground="#333", background="#f9fafc", padding=8)
        style.configure("Doc.TButton", font=("Arial", 12, "bold"), foreground="white", background="#4CAF50", padding=10)
        style.map("Doc.TButton", background=[("active", "#45a049")])
        style.configure("Custom.Treeview", font=("Arial", 11), rowheight=25, background="#f9f9f9", foreground="#333")
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"), background="#f2f2f2", foreground="#333")
        style.map("Custom.Treeview", background=[("selected", "#f1f1f1")])

    def create_widgets(self):
        container = tk.Frame(self.window, bg="#fff", bd=2, relief="flat")
        container.pack(pady=30, padx=30, fill="both", expand=True)
        container.configure(highlightbackground="#ddd", highlightthickness=1, highlightcolor="#ddd")

        title = "Avaliação de Ambiente: " + ("Servidor" if not self.banco else self.tipo)
        ttk.Label(container, text=title, style="MainTitle.TLabel").pack(pady=(0, 20))

        content_frame = tk.Frame(container, bg="#fff")
        content_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(content_frame, bg="#fff", bd=2, relief="flat")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.Frame(content_frame, bg="#fff", bd=2, relief="flat")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        if self.servidor:
            self.exibir_dados_servidor(left_frame)

        if self.banco:
            self.exibir_dados_banco(right_frame)

        button_frame = tk.Frame(container, bg="#fff")
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Gerar Documento", cursor="hand2", style="Doc.TButton", command=self.gerar_documento).pack()

        footer = tk.Frame(self.window, bg="#f4f4f9")
        footer.pack(side="bottom", fill="x", pady=(0, 10))
        
        # Substitui o Label por uma imagem
        # logo_image = tk.PhotoImage(file="assets/cigam-logo.png").subsample(2, 2)  # Reduz pela metade (tamanho médio)
        # logo_label = tk.Label(footer, image=logo_image, bg="#f4f4f9")
        # logo_label.image = logo_image  # Mantém referência para evitar garbage collection
        # logo_label.pack(side="right", padx=10)

    def exibir_dados_servidor(self, frame):
        ttk.Label(frame, text="Informações Gerais - Servidor Atual", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 10))
        labels = [
            ("Hostname:", self.servidor.hostname),
            ("Sistema Operacional:", self.servidor.sistema_operacional),
            ("Processador:", self.servidor.cpu),
            ("Ano do Processador:", self.servidor.ano),
            ("STR do Processador:", self.servidor.str),
            ("Núcleos:", self.servidor.nucleos),
            ("Threads:", self.servidor.threads),
            ("RAM:", self.servidor.ram),
            ("Rede:", self.servidor.rede),
        ]
        for titulo, valor in labels:
            row_frame = tk.Frame(frame, bg="#fff")
            row_frame.pack(fill="x", pady=2)
            ttk.Label(row_frame, text=f"{titulo}", style="Data.TLabel", width=25, anchor="w").pack(side="left")
            ttk.Label(row_frame, text=str(valor), style="Data.TLabel").pack(side="left")

        ttk.Label(frame, text="Discos", style="SectionTitle.TLabel").pack(anchor="w", pady=(20, 10))
        for nome, info in self.servidor.discos.items():
            ttk.Label(frame, text=f"{nome} - {info}", style="ListItem.TLabel").pack(fill="x", pady=2)

    def exibir_dados_banco(self, frame):
        title = f"Database: {self.banco.nome_database}" if self.tipo == "SQLServer" else f"Usuário: {self.banco.usuario}"
        ttk.Label(frame, text=title, style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 10))
        
        if self.tipo == "SQLServer":
            labels = [
                ("Versão:", self.banco.versao),
                ("Memória mínima dedicada ao banco:", self.banco.memoria_min),
                ("Memória máxima dedicada ao banco:", self.banco.memoria_max),
                ("Tamanho da base:", self.banco.datafile),
                ("Tamanho do log:", self.banco.logfile),
            ]
        else:  # Oracle
            labels = [
                ("Versão:", self.banco.versao),
                ("SGA:", self.banco.sga),
                ("PGA:", self.banco.pga),
                ("Armazenamento:", self.banco.armazenamento),
            ]
        
        for titulo, valor in labels:
            row_frame = tk.Frame(frame, bg="#fff")
            row_frame.pack(fill="x", pady=2)
            ttk.Label(row_frame, text=f"{titulo}", style="Data.TLabel", width=35, anchor="w").pack(side="left")
            ttk.Label(row_frame, text=str(valor), style="Data.TLabel").pack(side="left")

        ttk.Label(frame, text="TOP 5 - Tabelas mais pesadas", style="SectionTitle.TLabel").pack(anchor="w", pady=(20, 10))
        tree = ttk.Treeview(frame, columns=("Nome", "Linhas", "Espaço"), show="headings", height=5, style="Custom.Treeview")
        tree.heading("Nome", text="Nome da Tabela")
        tree.heading("Linhas", text="Quantidade de Linhas")
        tree.heading("Espaço", text="Espaço Total (GB)")
        tree.column("Nome", width=150, anchor="w")
        tree.column("Linhas", width=150, anchor="center")
        tree.column("Espaço", width=150, anchor="center")
        tree.pack(fill="x", pady=5)
        for nome, (linhas, espaco) in self.banco.tabelas_pesadas.items():
            linhas_formatadas = "{:,}".format(linhas).replace(",", ".")
            tree.insert("", "end", values=(nome, linhas_formatadas, espaco))

    def gerar_documento(self):
        try:
            gerar_documento(self.servidor, self.banco, self.tipo, self.dados_questionario)
            messagebox.showinfo("Sucesso", "Documento gerado com sucesso como 'relatorio_ambiente.docx'!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar documento: {str(e)}")

    def on_close(self):
        self.window.destroy()
        self.parent.destroy()