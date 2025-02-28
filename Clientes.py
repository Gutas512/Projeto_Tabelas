import tkinter as tk
from tkinter import ttk
from tkinter import *
from banco import Banco
from usuario import Clientes, Cidades


def fetch_data_clients():
    banco = Banco()
    try:
        c = banco.conexao.cursor()
        c.execute("SELECT * FROM clientes")
        rows = c.fetchall()  # Buscando todos os resultados
        c.close()
        return rows
    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")
        return []


def fetch_data_cities():
    banco = Banco()
    try:
        c = banco.conexao.cursor()
        c.execute("SELECT idcidade, nomecid FROM cidades")
        rows = c.fetchall()  # Buscando todos os resultados
        c.close()
        return rows
    except Exception as e:
        print(f"Erro ao buscar cidades: {e}")
        return []


def populate_treeview(treeview, data):
    for row in data:
        treeview.insert("", "end", values=row)


def update_treeview(treeview):
    treeview.delete(*treeview.get_children())  # Limpa todos os dados existentes
    data = fetch_data_clients()  # Busca os dados atualizados
    populate_treeview(treeview, data)  # Reinsere os dados


def populate_combobox_cidades(combobox):
    cidades = fetch_data_cities()
    combobox["values"] = [cidade[1] for cidade in cidades]  # Apenas os nomes das cidades


def get_city_id_by_name(city_name):
    cidades = fetch_data_cities()
    for cid in cidades:
        if cid[1] == city_name:
            return cid[0]
    return None


class Application:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Sistema de Gestão de Clientes")

        # Configuração do formulário
        self.fonte = ("Verdana", "8")
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
        self.container7.pack()

        self.container8 = Frame(master)
        self.container8["pady"] = 10
        self.container8.pack(fill=tk.BOTH, expand=True)

        self.titulo = Label(self.container1, text="Informe os dados do cliente:")
        self.titulo["font"] = ("Calibri", "9", "bold")
        self.titulo.pack()

        self.lblidcliente = Label(self.container2, text="ID Cliente:", font=self.fonte, width=10)
        self.lblidcliente.pack(side=LEFT)

        self.txtidcliente = Entry(self.container2)
        self.txtidcliente["width"] = 10
        self.txtidcliente["font"] = self.fonte
        self.txtidcliente.pack(side=LEFT)

        self.btnBuscar = Button(self.container2, text="Buscar", font=self.fonte, width=10)
        self.btnBuscar["command"] = self.buscarCliente
        self.btnBuscar.pack(side=RIGHT)

        self.lblnomecli = Label(self.container3, text="Nome:", font=self.fonte, width=10)
        self.lblnomecli.pack(side=LEFT)

        self.txtnomecli = Entry(self.container3)
        self.txtnomecli["width"] = 25
        self.txtnomecli["font"] = self.fonte
        self.txtnomecli.pack(side=LEFT)

        self.lblcpf = Label(self.container4, text="CPF:", font=self.fonte, width=10)
        self.lblcpf.pack(side=LEFT)

        self.txtcpf = Entry(self.container4)
        self.txtcpf["width"] = 25
        self.txtcpf["font"] = self.fonte
        self.txtcpf.pack(side=LEFT)

        self.lbldata_nascimento = Label(self.container5, text="Nascimento:", font=self.fonte, width=15)
        self.lbldata_nascimento.pack(side=LEFT)

        self.txtdata_nascimento = Entry(self.container5)
        self.txtdata_nascimento["width"] = 25
        self.txtdata_nascimento["font"] = self.fonte
        self.txtdata_nascimento.pack(side=LEFT)

        self.lblgenero = Label(self.container6, text="Gênero:", font=self.fonte, width=10)
        self.lblgenero.pack(side=LEFT)

        self.combogenero = ttk.Combobox(self.container6, values=["Masculino", "Feminino"], font=self.fonte, width=23)
        self.combogenero.pack(side=LEFT)
        self.combogenero.current(0)  # Define a opção padrão como "Masculino"

        self.lblcidade = Label(self.container7, text="Cidade:", font=self.fonte, width=10)
        self.lblcidade.pack(side=LEFT)

        self.combocidade = ttk.Combobox(self.container7, values=[], font=self.fonte, width=23)
        self.combocidade.pack(side=LEFT)

        self.bntInsert = Button(self.container7, text="Inserir", font=self.fonte, width=12)
        self.bntInsert["command"] = self.inserirCliente
        self.bntInsert.pack(side=LEFT)

        self.bntAlterar = Button(self.container7, text="Alterar", font=self.fonte, width=12)
        self.bntAlterar["command"] = self.alterarCliente
        self.bntAlterar.pack(side=LEFT)

        self.bntExcluir = Button(self.container7, text="Excluir", font=self.fonte, width=12)
        self.bntExcluir["command"] = self.excluirCliente
        self.bntExcluir.pack(side=LEFT)

        self.lblmsg = Label(self.container7, text="")
        self.lblmsg["font"] = ("Verdana", "9", "italic")
        self.lblmsg.pack()

        # Configuração da Treeview (Tabela)
        self.columns = ("ID", "Nome", "CPF", "Data de nascimento", "Gênero", "Cidade")
        self.treeview = ttk.Treeview(self.container8, columns=self.columns, show='headings')
        for col in self.columns:
            self.treeview.heading(col, text=col)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Preencher a Treeview e a Combobox com dados do banco ao iniciar
        self.update_treeview()
        populate_combobox_cidades(self.combocidade)

    def update_treeview(self):
        update_treeview(self.treeview)  # Atualiza a Treeview com os dados mais recentes

    def inserirCliente(self):
        cliente = Clientes()
        cliente.nomecli = self.txtnomecli.get()
        cliente.cpf = self.txtcpf.get()
        cliente.data_nascimento = self.txtdata_nascimento.get()
        cliente.genero = self.combogenero.get()

        # Obtém o ID da cidade selecionada
        cidade_selecionada = self.combocidade.get()
        cidade_id = get_city_id_by_name(cidade_selecionada)
        cliente.idcidade = cidade_id

        self.lblmsg["text"] = cliente.insertCliente()

        self.txtidcliente.delete(0, END)
        self.txtnomecli.delete(0, END)
        self.txtcpf.delete(0, END)
        self.txtdata_nascimento.delete(0, END)
        self.combogenero.set('')
        self.combocidade.set('')  # Reseta a combobox para o valor padrão

        self.update_treeview()  # Atualiza a Treeview após inserir

    def alterarCliente(self):
        cliente = Clientes()
        cliente.idcliente = self.txtidcliente.get()
        cliente.nomecli = self.txtnomecli.get()
        cliente.cpf = self.txtcpf.get()
        cliente.data_nascimento = self.txtdata_nascimento.get()
        cliente.genero = self.combogenero.get()

        # Obtém o ID da cidade selecionada
        cidade_selecionada = self.combocidade.get()
        cidade_id = get_city_id_by_name(cidade_selecionada)
        cliente.idcidade = cidade_id

        self.lblmsg["text"] = cliente.updateCliente()

        self.txtidcliente.delete(0, END)
        self.txtnomecli.delete(0, END)
        self.txtcpf.delete(0, END)
        self.txtdata_nascimento.delete(0, END)
        self.combogenero.set('')
        self.combocidade.set('')  # Reseta a combobox para o valor padrão

        self.update_treeview()  # Atualiza a Treeview após alterar

    def excluirCliente(self):
        cliente = Clientes()
        cliente.idcliente = self.txtidcliente.get()

        self.lblmsg["text"] = cliente.deleteCliente()

        self.txtidcliente.delete(0, END)
        self.txtnomecli.delete(0, END)
        self.txtcpf.delete(0, END)
        self.txtdata_nascimento.delete(0, END)
        self.combogenero.set('')
        self.combocidade.set('')  # Reseta a combobox para o valor padrão

        self.update_treeview()  # Atualiza a Treeview após excluir

    def buscarCliente(self):
        cliente = Clientes()
        idcliente = self.txtidcliente.get()

        self.lblmsg["text"] = cliente.selectCliente(idcliente)

        # Preencher os campos com os dados do cliente encontrado
        self.txtidcliente.delete(0, END)
        self.txtidcliente.insert(INSERT, cliente.idcliente)
        self.txtnomecli.delete(0, END)
        self.txtnomecli.insert(INSERT, cliente.nomecli)
        self.txtcpf.delete(0, END)
        self.txtcpf.insert(INSERT, cliente.cpf)
        self.txtdata_nascimento.delete(0, END)
        self.txtdata_nascimento.insert(INSERT, cliente.data_nascimento)
        self.combogenero.set(cliente.genero)

        # Selecionar a cidade na combobox
        cidade_id = cliente.idcidade
        cidades = fetch_data_cities()
        for cid in cidades:
            if cid[0] == cidade_id:
                self.combocidade.set(cid[1])
                break

    def on_city_selected(self, event):
        # Implementar o que acontece quando uma cidade é selecionada (se necessário)
        pass


if __name__ == '__main__':
    root = Tk()
    Application(root)
    root.mainloop()