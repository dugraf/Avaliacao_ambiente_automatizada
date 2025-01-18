import tkinter as tk
import threading
from tkinter import messagebox
from controllers.coleta_dados import coletar_dados_locais
from controllers.exportacao import exportar_para_html

def iniciar_coleta():
    def tarefa_coleta():
        try:
            servidor = coletar_dados_locais()
            exportar_para_html(servidor)
            messagebox.showinfo("Sucesso", "Dados coletados e exportados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante a coleta de dados: {str(e)}")

    threading.Thread(target=tarefa_coleta).start()

def iniciar_gui():
    root = tk.Tk()
    root.title("Avaliação de Servidores CIGAM")
    root.geometry("400x300")

    label = tk.Label(root, text="Avaliação de Servidor Local", font=("Arial", 14))
    label.pack(pady=10)

    btn_coletar = tk.Button(root, text="Coletar Dados", command=iniciar_coleta)
    btn_coletar.pack(pady=20)

    root.mainloop()
