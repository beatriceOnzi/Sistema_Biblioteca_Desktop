# turma.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import messagebox
from setup_autocomplete import complete_text

def print_tabela(cabecalhos, dados):
    larguras = [
        max(len(str(cabecalho)), max((len(str(linha[i])) for linha in dados), default=0))
        for i, cabecalho in enumerate(cabecalhos)
    ]
    linha_cab = " | ".join(cabecalhos[i].ljust(larguras[i]) for i in range(len(cabecalhos)))
    print(linha_cab)
    print("-" * len(linha_cab))
    for linha in dados:
        print(" | ".join(str(linha[i]).ljust(larguras[i]) for i in range(len(linha))))

def truncar_texto(texto, limite):
    if not texto:
        return ""
    return texto if len(texto) <= limite else texto[:limite - 3] + "..."

class TurmaWindow:
    def __init__(self, parent, turma, database):
        self.parent = parent
        self.turma = turma
        self.db = database

        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gerenciamento - {turma}")
        self.window.update_idletasks()
        largura = self.window.winfo_screenwidth()
        altura = self.window.winfo_screenheight()
        self.window.geometry(f"{largura}x{altura-100}+0+0")
        self.window.configure(bg="#f0f0f0")
        self.scrollbar_width = 16
        self.col_widths = [112, 150, 200, 112]

        # Centralizar janela
        self.window.transient(parent)
        self.window.grab_set()

        self.create_widgets()
        self.carregar_dados()

    def create_widgets(self):
        # Título
        title_frame = tk.Frame(self.window, bg="#f0f0f0")
        title_frame.pack(pady=10)

        title_label = tk.Label(
            title_frame,
            text=f"Gerenciamento de Empréstimos - {self.turma}",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack()

        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # grid com 3 colunas: tabela | separador | tabela
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        primeira_tabela_container = tk.Frame(main_frame, bg="#f0f0f0")
        primeira_tabela_container.grid(row=0, column=0, sticky="nsew")

        separator = tk.Frame(main_frame, bg="#bdc3c7", width=2)
        separator.grid(row=0, column=1, sticky="ns", padx=10)

        segunda_tabela_container = tk.Frame(main_frame, bg="#f0f0f0")
        segunda_tabela_container.grid(row=0, column=2, sticky="nsew")

        # CRIAR AS TABELAS
        self.create_primeira_tabela(primeira_tabela_container)
        self.create_segunda_tabela(segunda_tabela_container)

        # Frame para botões
        buttons_frame = tk.Frame(self.window, bg="#f0f0f0")
        buttons_frame.pack(pady=15, fill="x", padx=20)

        # Botão Salvar
        salvar_btn = tk.Button(
            buttons_frame,
            text="Salvar",
            font=("Arial", 14, "bold"),
            width=10,
            height=1,
            bg="#27ae60",
            fg="white",
            relief="raised",
            bd=3,
            command=self.salvar_dados
        )
        salvar_btn.pack(side="left", padx=10)

        # Botão Avançar Semana
        avancar_btn = tk.Button(
            buttons_frame,
            text="Avançar Semana",
            font=("Arial", 12, "bold"),
            width=14,
            height=1,
            bg="#1f18a9",
            fg="white",
            relief="raised",
            bd=3,
            command=self.avancar_semana_btn
        )
        avancar_btn.pack(side="left", padx=10)


    def create_primeira_tabela(self, parent):
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            frame,
            text="Empréstimos Anteriores",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))

        table_frame = tk.Frame(frame, bg="white", relief="solid", bd=1)
        table_frame.pack(fill="both", expand=True)

        headers = ["Data Empréstimo", "Aluno", "Livro", "Data Devolução"]

        header_frame = tk.Frame(table_frame, bg="#34495e")
        header_frame.pack(fill="x")

        for i, texto in enumerate(headers):
            label = tk.Label(
                header_frame,
                text=texto,
                font=("Arial", 10, "bold"),
                bg="#34495e",
                fg="white",
                relief="solid",
                bd=1,
                anchor="w"
            )
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            header_frame.grid_columnconfigure(i, minsize=self.col_widths[i])

        data_frame = tk.Frame(table_frame)
        data_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(data_frame, bg="white")
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=canvas.yview)

        self.scrollable_frame1 = tk.Frame(canvas, bg="white")

        for i in range(4):
            self.scrollable_frame1.grid_columnconfigure(i, minsize=self.col_widths[i])

        self.scrollable_frame1.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame1, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.primeira_tabela_frame = self.scrollable_frame1


    def create_segunda_tabela(self, parent):
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            frame,
            text="Empréstimos Atuais",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))

        table_frame = tk.Frame(frame, bg="white", relief="solid", bd=1)
        table_frame.pack(fill="both", expand=True)

        headers = ["Data", "Aluno", "Livro", "Data Devolução"]

        # ---------------- CABEÇALHO ----------------
        header_frame = tk.Frame(table_frame, bg="#34495e")
        header_frame.pack(fill="x")

        for i, texto in enumerate(headers):
            label = tk.Label(
                header_frame,
                text=texto,
                font=("Arial", 10, "bold"),
                bg="#34495e",
                fg="white",
                relief="solid",
                bd=1,
                anchor="w"
            )
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            header_frame.grid_columnconfigure(
                i,
                minsize=self.col_widths[i],
                weight=1
            )

        scrollbar_width = 16
        header_frame.grid_columnconfigure(len(headers), minsize=scrollbar_width)

        spacer = tk.Frame(header_frame, bg="#34495e")
        spacer.grid(row=0, column=len(headers), sticky="ns")

        # ---------------- DADOS ----------------
        data_frame = tk.Frame(table_frame)
        data_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(data_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=canvas.yview)

        self.scrollable_frame2 = tk.Frame(canvas, bg="white")

        for i in range(len(headers)):
            self.scrollable_frame2.grid_columnconfigure(
                i,
                minsize=self.col_widths[i],
                weight=1
            )

        self.scrollable_frame2.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=self.scrollable_frame2,
            anchor="nw"
        )

        # 👉 força o frame interno a ter a mesma largura do canvas
        def resize_frame(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_frame)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.segunda_tabela_frame = self.scrollable_frame2

    def carregar_dados(self):
        self.carregar_primeira_tabela()
        self.carregar_segunda_tabela()

    def carregar_primeira_tabela(self):
        for widget in self.primeira_tabela_frame.winfo_children():
            widget.destroy()

        semana_atual = self.db.get_semana_atual_turma(self.turma)
        semana_anterior = semana_atual - 1

        if semana_anterior > 0:
            emprestimos_anteriores = self.db.get_emprestimos_por_semana_turma(self.turma, semana_anterior)
        else:
            emprestimos_anteriores = []

        alunos = self.db.get_alunos_por_turma(self.turma)

        # dicionário correto
        emprestimos_dict = {}
        for emp in emprestimos_anteriores:
            data_emp, nome_aluno, nome_livro, data_dev_prevista, data_dev_real = emp
            emprestimos_dict[nome_aluno] = {
                "data_emp": data_emp,
                "livro": nome_livro,
                "dev_prev": data_dev_prevista,
                "dev_real": data_dev_real
            }

        for i, (aluno_id, nome_aluno) in enumerate(alunos):
            if nome_aluno in emprestimos_dict:
                info = emprestimos_dict[nome_aluno]
                self.create_primeira_linha(
                    i,
                    info["data_emp"],
                    nome_aluno,
                    info["livro"],
                    info["dev_prev"],
                    aluno_id,
                    info["dev_real"]
                )
            else:
                self.create_primeira_linha(
                    i,
                    "",
                    nome_aluno,
                    "",
                    "",
                    aluno_id,
                    ""
                )

    def create_primeira_linha(self, row, data_emp, nome_aluno, nome_livro, data_dev_prev, aluno_id=None, data_dev_real=None):
        bg_dev = "#e8a3a9" if nome_livro and not data_dev_real else "white"

        labels = [
            data_emp or "",
            nome_aluno,
            truncar_texto(nome_livro, 38),
            data_dev_real or ""
        ]

        for col, texto in enumerate(labels):
            bg = bg_dev if col == 3 else "white"
            label = tk.Label(
                self.primeira_tabela_frame,
                text=texto,
                font=("Arial", 9),
                bg=bg,
                relief="solid",
                bd=1,
                anchor="w"
            )
            label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        self.primeira_tabela_frame.grid_rowconfigure(row, weight=1)


    def carregar_segunda_tabela(self):
        for widget in self.segunda_tabela_frame.winfo_children():
            widget.destroy()

        emprestimos_atuais = self.db.get_emprestimos_semana_atual(self.turma)
        alunos = self.db.get_alunos_por_turma(self.turma)
        livros = self.db.get_todos_livros()

        self.livros_disponiveis = livros
        self.entries_segunda_tabela = []

        emprestimos_dict = {}
        for emp in emprestimos_atuais:
            data_emp, nome_aluno, nome_livro, data_dev_prev = emp
            emprestimos_dict[nome_aluno] = (data_emp, nome_livro, data_dev_prev)

        for i, (aluno_id, nome_aluno) in enumerate(alunos):
            if nome_aluno in emprestimos_dict:
                data_emp, nome_livro, data_dev_prev = emprestimos_dict[nome_aluno]
                self.create_segunda_linha(i, data_emp, nome_aluno, nome_livro, data_dev_prev, aluno_id)
            else:
                # ✅ Data do sistema (data atual)
                hoje = datetime.now().strftime("%d/%m/%Y")
                data_sistema = datetime.now()

                # Data de devolução (uma semana depois)
                uma_semana_depois = (data_sistema + timedelta(days=7)).strftime("%d/%m/%Y")

                self.create_segunda_linha(i, hoje, nome_aluno, "", uma_semana_depois, aluno_id)

    def create_segunda_linha(self, row, data_emp, nome_aluno, nome_livro, data_dev_prev, aluno_id):
        valores = [data_emp, nome_aluno]

        for col, texto in enumerate(valores):
            label = tk.Label(
                self.segunda_tabela_frame,
                text=texto,
                font=("Arial", 9),
                bg="white",
                relief="solid",
                bd=1,
                anchor="w"
            )
            label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        livro_var = tk.StringVar(value=truncar_texto(nome_livro, 38))
        livro_entry = tk.Entry(
            self.segunda_tabela_frame,
            textvariable=livro_var,
            font=("Arial", 9)
        )
        livro_entry.grid(row=row, column=2, sticky="nsew", padx=1, pady=1)
        complete_text(self, livro_entry, livro_var)

        data_label = tk.Label(
            self.segunda_tabela_frame,
            text=data_dev_prev,
            font=("Arial", 9),
            bg="white",
            relief="solid",
            bd=1,
            anchor="w"
        )
        data_label.grid(row=row, column=3, sticky="nsew", padx=1, pady=1)

        self.entries_segunda_tabela.append({
            'aluno_id': aluno_id,
            'nome_aluno': nome_aluno,
            'livro_var': livro_var,
            'data_emp': data_emp,
            'data_dev': data_dev_prev
        })

        self.segunda_tabela_frame.grid_rowconfigure(row, weight=1)


    def salvar_dados(self):
        data_sistema_dt = self.db.get_data_atual_sistema()
        data_devolucao_real = data_sistema_dt.strftime("%d/%m/%Y")

        semana_atual = self.db.get_semana_atual_turma(self.turma)
        semana_anterior = semana_atual - 1

        emprestimos_salvos = 0

        for entry_data in self.entries_segunda_tabela:
            inseriu = False  # GARANTE que sempre exista

            livro_nome = entry_data['livro_var'].get().strip()
            aluno_id = entry_data['aluno_id']

            if not livro_nome or livro_nome == "..." or len(livro_nome) < 2:
                continue

            # 1️⃣ GARANTIR QUE O LIVRO EXISTA
            livro_id = self.db.get_livro_id(livro_nome)

            if not livro_id:
                criado = self.db.inserir_livro(livro_nome)
                if not criado:
                    messagebox.showwarning(
                        "Livro não encontrado",
                        f"O livro '{livro_nome}' não pôde ser criado no sistema."
                    )
                    continue

                livro_id = self.db.get_livro_id(livro_nome)
                if not livro_id:
                    messagebox.showwarning(
                        "Livro não encontrado",
                        f"O livro '{livro_nome}' não foi encontrado após a criação."
                    )
                    continue

            # 2️⃣ VERIFICAR EMPRÉSTIMO DA SEMANA ATUAL
            existe_emprestimo = self.db.verificar_emprestimo_existente(
                aluno_id,
                semana_atual
            )

            if existe_emprestimo:
                # existe empréstimo → atualizar (edição ou troca)
                self.db.atualizar_emprestimo(
                    aluno_id,
                    livro_id,
                    entry_data['data_emp'],
                    entry_data['data_dev'],
                    semana_atual
                )

            else:
                # não existe empréstimo → inserir novo
                inseriu = self.db.inserir_emprestimo(
                    aluno_id,
                    livro_id,
                    entry_data['data_emp'],
                    entry_data['data_dev'],
                    semana_atual
                )

            # 3️⃣ DEVOLUÇÃO REAL (SÓ SE A SEMANA AVANÇOU E INSERIU NOVO)
            if inseriu and semana_anterior > 0:
                linhas_afetadas = self.db.atualizar_devolucao_real(
                    aluno_id,
                    semana_anterior,
                    data_devolucao_real
                )
                if linhas_afetadas > 0:
                    emprestimos_salvos += 1

        # 4️⃣ FECHAR JANELA SE ALGO FOI SALVO
            self.window.destroy()


    def avancar_semana_btn(self):
        ok = False
        try:
            ok = self.db.finalizar_e_avancar_semana(self.turma)
        except Exception as e:
            print("Erro ao finalizar e avançar semana:", e)
            ok = False

        if ok:
            messagebox.showinfo("Avançar Semana", f"Semana avançada com sucesso para a turma {self.turma}. As devoluções foram registradas.")
            self.carregar_dados()
        else:
            messagebox.showerror("Avançar Semana", "Falha ao avançar a semana. Verifique logs.")

    def calcular_larguras_colunas(self, dados, headers):
        larguras = []
        for i, header in enumerate(headers):
            largura_cabecalho = len(header["text"])
            largura_dados = max((len(str(linha[i])) for linha in dados), default=0)
            larguras.append(max(largura_cabecalho, largura_dados))
        return larguras
