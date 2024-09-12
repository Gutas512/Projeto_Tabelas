import tkinter as tk
from tkinter import messagebox

from banco import Banco


class TelaLogin:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Tela de Login")

        self.fonte = ("Verdana", "10")

        # Configuração do formulário
        self.container = tk.Frame(master)
        self.container["padx"] = 20
        self.container["pady"] = 20
        self.container.pack()

        self.lblusuario = tk.Label(self.container, text="Usuário:", font=self.fonte)
        self.lblusuario.pack(pady=5)

        self.txtusuario = tk.Entry(self.container, font=self.fonte)
        self.txtusuario.pack(pady=5)

        self.lblsenha = tk.Label(self.container, text="Senha:", font=self.fonte)
        self.lblsenha.pack(pady=5)

        self.txtsenha = tk.Entry(self.container, show="*", font=self.fonte)
        self.txtsenha.pack(pady=5)

        self.btnlogin = tk.Button(self.container, text="Entrar", font=self.fonte, command=self.login)
        self.btnlogin.pack(pady=10)

    def login(self):
        usuario = self.txtusuario.get()
        senha = self.txtsenha.get()

        if self.validar_login(usuario, senha):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            # Aqui você pode adicionar o código para abrir a próxima tela ou funcionalidade
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def validar_login(self, usuario, senha):
        # Verifica se o usuário e a senha são válidos
        banco = Banco()  # Certifique-se de ter a classe Banco configurada corretamente
        try:
            c = banco.conexao.cursor()
            c.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
            linha = c.fetchone()
            c.close()
            return linha is not None
        except Exception as e:
            print(f"Erro ao validar login: {e}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaLogin(root)
    root.mainloop()
