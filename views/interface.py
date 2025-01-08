import tkinter as tk
from tkinter import ttk, messagebox

def exibir_alerta_erro(mensagem):
    messagebox.showerror("Erro na Coleta de Dados", mensagem)

def exibir_alerta_concluido(mensagem):
    messagebox.showinfo("Processo concluído", mensagem)