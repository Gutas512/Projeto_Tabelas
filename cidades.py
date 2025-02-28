import tkinter as tk
from tkinter import ttk, Frame, Label, Entry, Button, END, INSERT
import sqlite3
from usuario import Cidades

class Application:
    def __init__(self, master=None):
        self.fonte = ("Verdana", "8")

        # Containers para o formulário
        self.container1 = Frame(master)
        self.container1["pady"] = 10
        self.container1.pack()

        self.container2 = Frame(master)
        self.container2["padx"] = 20
        self.container2["pady"] = 5
        self.container2.pack()

        self.container3 = Frame(master)
        self.container3["padx"] = 20
        self.container3["pady"] = 5
        self.container3.pack()

        self.container4 = Frame(master)
        self.container4["padx"] = 20
        self.container4["pady"] = 5
        self.container4.pack()

        self.container5 = Frame(master)
        self.container5["padx"] = 20
        self.container5["pady"] = 10
        self.container5.pack()

        self.container6 = Frame(master)
        self.container6["pady"] = 15
        self.container6.pack()

        self.container7 = Frame(master)
        self.container7["pady"] = 15
        self.container7.pack(fill=tk.BOTH, expand=True)

        # Formulário de entrada de dados
        self.titulo = Label(self.container1, text="Informe os dados da cidade:")
        self.titulo["font"] = ("Calibri", "9", "bold")
        self.titulo.pack()

        self.lblidcidade = Label(self.container2, text="idCidade:", font=self.fonte, width=10)
        self.lblidcidade.pack(side=tk.LEFT)

        self.txtidcidade = Entry(self.container2)
        self.txtidcidade["width"] = 10
        self.txtidcidade["font"] = self.fonte
        self.txtidcidade.pack(side=tk.LEFT)

        self.btnBuscar = Button(self.container2, text="Buscar", font=self.fonte, width=10)
        self.btnBuscar["command"] = self.buscarCidade
        self.btnBuscar.pack(side=tk.RIGHT)

        self.lblnomecid = Label(self.container3, text="Nome:", font=self.fonte, width=10)
        self.lblnomecid.pack(side=tk.LEFT)

        self.txtnomecid = Entry(self.container3)
        self.txtnomecid["width"] = 25
        self.txtnomecid["font"] = self.fonte
        self.txtnomecid.pack(side=tk.LEFT)

        self.lblcep = Label(self.container4, text="CEP:", font=self.fonte, width=10)
        self.lblcep.pack(side=tk.LEFT)

        self.txtcep = Entry(self.container4)
        self.txtcep["width"] = 25
        self.txtcep["font"] = self.fonte
        self.txtcep.pack(side=tk.LEFT)

        self.lblUF = Label(self.container5, text="UF:", font=self.fonte, width=10)
        self.lblUF.pack(side=tk.LEFT)

        self.txtUF = Entry(self.container5)
        self.txtUF["width"] = 25
        self.txtUF["font"] = self.fonte
        self.txtUF.pack(side=tk.LEFT)

        self.bntInsert = Button(self.container6, text="Inserir", font=self.fonte, width=12)
        self.bntInsert["command"] = self.inserirCidade
        self.bntInsert.pack(side=tk.LEFT)

        self.bntAlterar = Button(self.container6, text="Alterar", font=self.fonte, width=12)
        self.bntAlterar["command"] = self.alterarCidade
        self.bntAlterar.pack(side=tk.LEFT)

        self.bntExcluir = Button(self.container6, text="Excluir", font=self.fonte, width=12)
        self.bntExcluir["command"] = self.excluirCidade
        self.bntExcluir.pack(side=tk.LEFT)

        self.lblmsg = Label(self.container6, text="")
        self.lblmsg["font"] = ("Verdana", "9", "italic")
        self.lblmsg.pack()

        # Configurando a Treeview para exibir os dados
        self.columns = ("ID", "Nome", "CEP", "UF")
        self.treeview = ttk.Treeview(self.container7, columns=self.columns, show='headings')
        for col in self.columns:
            self.treeview.heading(col, text=col)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Preenchendo a Treeview com dados do banco ao iniciar
        self.update_treeview()

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())  # Limpa todos os dados existentes
        data = self.fetch_data()  # Busca os dados atualizados
        self.populate_treeview(data)  # Reinsere os dados

    def fetch_data(self):
        conn = sqlite3.connect('banco.db')  # Conectando ao banco de dados
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cidades")
        rows = cursor.fetchall()  # Buscando todos os resultados
        conn.close()

        return rows

    def populate_treeview(self, data):
        for row in data:
            self.treeview.insert("", "end", values=row)

    def inserirCidade(self):
        cidade = Cidades()
        cidade.nomecid = self.txtnomecid.get()
        cidade.cep = self.txtcep.get()
        cidade.UF = self.txtUF.get()

        self.lblmsg["text"] = cidade.insertCidade()

        self.txtidcidade.delete(0, END)
        self.txtnomecid.delete(0, END)
        self.txtcep.delete(0, END)
        self.txtUF.delete(0, END)

        self.update_treeview()  # Atualiza a Treeview após inserir

    def alterarCidade(self):
        cidade = Cidades()
        cidade.idcidade = self.txtidcidade.get()
        cidade.nomecid = self.txtnomecid.get()
        cidade.cep = self.txtcep.get()
        cidade.UF = self.txtUF.get()

        self.lblmsg["text"] = cidade.updateCidade()

        self.txtidcidade.delete(0, END)
        self.txtnomecid.delete(0, END)
        self.txtcep.delete(0, END)
        self.txtUF.delete(0, END)

        self.update_treeview()  # Atualiza a Treeview após alterar

    def excluirCidade(self):
        cidade = Cidades()
        cidade.idcidade = self.txtidcidade.get()

        self.lblmsg["text"] = cidade.deleteCidade()

        self.txtidcidade.delete(0, END)
        self.txtnomecid.delete(0, END)
        self.txtcep.delete(0, END)
        self.txtUF.delete(0, END)

        self.update_treeview()  # Atualiza a Treeview após excluir

    def buscarCidade(self):
        cidade = Cidades()
        idcidade = self.txtidcidade.get()

        self.lblmsg["text"] = cidade.selectCidade(idcidade)

        # Preencher os campos com os dados da cidade encontrada
        self.txtidcidade.delete(0, END)
        self.txtidcidade.insert(INSERT, cidade.idcidade)
        self.txtnomecid.delete(0, END)
        self.txtnomecid.insert(INSERT, cidade.nomecid)
        self.txtcep.delete(0, END)
        self.txtcep.insert(INSERT, cidade.cep)
        self.txtUF.delete(0, END)
        self.txtUF.insert(INSERT, cidade.UF)

        self.update_treeview()  # Atualiza a Treeview após buscar


# Configuração da janela principal
root = tk.Tk()
root.attributes('-fullscreen', True)
Application(root)
root.mainloop()