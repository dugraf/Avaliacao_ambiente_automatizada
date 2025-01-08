import tkinter as tk
from tkinter import messagebox
from controllers.coleta_dados import coletar_dados_locais
from controllers.exportacao import exportar_para_html

def iniciar_coleta():
    servidor = coletar_dados_locais()
    messagebox.showinfo("Dados Coletados", str(servidor))
    exportar_para_html(servidor)
    exit()

def iniciar_gui():
    root = tk.Tk()
    root.title("Avaliação de Servidores CIGAM")
    root.geometry("400x300")

    label = tk.Label(root, text="Avaliação de Servidor Local", font=("Arial", 14))
    label.pack(pady=10)

    btn_coletar = tk.Button(root, text="Coletar Dados", command=iniciar_coleta)
    btn_coletar.pack(pady=20)

    root.mainloop()
