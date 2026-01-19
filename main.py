import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from turma import TurmaWindow
from cadastro import CadastroWindow

class BibliotecaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Biblioteca")
        largura = self.root.winfo_screenwidth()
        altura = self.root.winfo_screenheight()
        self.root.geometry(f"{largura}x{altura}+0+0")
        self.root.minsize(800, 600)
        self.root.configure(bg="#f0f0f0")

        # Inicializar banco de dados
        self.db = Database()

        self.create_widgets()

    def create_widgets(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(pady=20)

        title_label = tk.Label(
            title_frame,
            text="Sistema de Biblioteca",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack()

        # Imagem logo.png
        try:
            self.logo_img = tk.PhotoImage(file="logo.png")
            logo_label = tk.Label(self.root, image=self.logo_img, bg="#f0f0f0")
            logo_label.pack(pady=5)
        except Exception as e:
            error_label = tk.Label(
                self.root,
                text="(logo.png não encontrado)",
                font=("Arial", 12, "italic"),
                bg="#f0f0f0",
                fg="red"
            )
            error_label.pack()

        # Frame para botões das turmas
        turmas_frame = tk.Frame(self.root, bg="#f0f0f0")
        turmas_frame.pack(pady=10)

        turmas_label = tk.Label(
            turmas_frame,
            text="Selecione uma Turma:",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        turmas_label.pack(pady=(0, 5))

        # Grid de botões das turmas
        buttons_frame = tk.Frame(turmas_frame, bg="#f0f0f0")
        buttons_frame.pack()

        # Criar botões de 1º ao 9º ano em grid 3x3
        for i in range(9):
            row = i // 3
            col = i % 3
            ano = i + 1

            btn = tk.Button(
                buttons_frame,
                text=f"{ano}º Ano",
                font=("Arial", 14, "bold"),
                width=12,
                height=2,
                bg="#1e45ba",
                fg="white",
                relief="raised",
                bd=3,
                command=lambda a=ano: self.abrir_turma(f"{a}º Ano")
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

            def on_enter(e, button=btn):
                button.config(bg="#11349e")

            def on_leave(e, button=btn):
                button.config(bg="#1e45ba")

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Frame para botões de ação
        actions_frame = tk.Frame(self.root, bg="#f0f0f0")
        actions_frame.pack(pady=30)

        # Botão Cadastrar
        cadastrar_btn = tk.Button(
            actions_frame,
            text="Cadastro e Outras Funções",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            bg="#27ae60",
            fg="white",
            relief="raised",
            bd=3,
            command=self.abrir_cadastro
        )
        cadastrar_btn.pack(side="left", padx=10)

        # Efeitos hover para botões de ação
        def on_enter_cadastrar(e):
            cadastrar_btn.config(bg="#219a52")

        def on_leave_cadastrar(e):
            cadastrar_btn.config(bg="#27ae60")

        cadastrar_btn.bind("<Enter>", on_enter_cadastrar)
        cadastrar_btn.bind("<Leave>", on_leave_cadastrar)

    def abrir_turma(self, turma):
        """Abre a janela de gerenciamento da turma"""
        TurmaWindow(self.root, turma, self.db)

    def abrir_cadastro(self):
        """Abre a janela de cadastro"""
        CadastroWindow(self.root, self.db)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BibliotecaApp()
    app.run()
