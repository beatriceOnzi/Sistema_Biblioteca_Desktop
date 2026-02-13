import tkinter as tk
from tkinter import ttk, messagebox

class CadastroWindow:
    def __init__(self, parent, database):
        self.parent = parent
        self.db = database

        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Cadastrar Alunos e Livros")
        largura = self.window.winfo_screenwidth()
        altura = self.window.winfo_screenheight()
        self.window.geometry(f"{largura}x{altura-100}+0+0")
        self.window.configure(bg="#f0f0f0")

        self.window.transient(parent)
        self.window.grab_set()

        self.create_widgets()

    def create_widgets(self):
        # Título principal
        title_frame = tk.Frame(self.window, bg="#f0f0f0")
        title_frame.pack(pady=20)

        title_label = tk.Label(
            title_frame,
            text="Cadastro de Alunos e Livros",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack()

        # Notebook para abas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Aba de cadastro de alunos
        self.create_aluno_tab(notebook)

        # Aba de cadastro de livros
        self.create_livro_tab(notebook)

        # Aba de passagem de ano
        self.create_year_passes(notebook)

        # Aba de histórico (nova)
        self.create_historico_tab(notebook)

        #Aba do manual
        self.create_manual(notebook)

        # Frame para botão fechar
        buttons_frame = tk.Frame(self.window, bg="#f0f0f0")
        buttons_frame.pack(pady=20)

        # Botão Fechar
        fechar_btn = tk.Button(
            buttons_frame,
            text="Fechar",
            font=("Arial", 12, "bold"),
            width=15,
            height=2,
            bg="#e74c3c",
            fg="white",
            relief="raised",
            bd=3,
            command=self.window.destroy
        )
        fechar_btn.pack()

    def create_aluno_tab(self, notebook):
        aluno_frame = tk.Frame(notebook, bg="#f0f0f0")
        notebook.add(aluno_frame, text="Cadastrar Aluno")

        # ===== FRAME PRINCIPAL =====
        main_frame = tk.Frame(aluno_frame, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # ===== BLOCO ESQUERDO =====
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        left_frame.columnconfigure(1, weight=1)

        tk.Label(
            left_frame,
            text="Cadastrar Novo Aluno",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        tk.Label(
            left_frame,
            text="Nome do Aluno:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        self.nome_aluno_var = tk.StringVar()
        tk.Entry(
            left_frame,
            textvariable=self.nome_aluno_var,
            font=("Arial", 12)
        ).grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(
            left_frame,
            text="Turma:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        self.turma_var = tk.StringVar()
        ttk.Combobox(
            left_frame,
            textvariable=self.turma_var,
            state="readonly",
            values=[f"{i}º Ano" for i in range(1, 10)]
        ).grid(row=2, column=1, sticky="ew", pady=5)

        tk.Button(
            left_frame,
            text="Cadastrar Aluno",
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            width=22,
            command=self.cadastrar_aluno
        ).grid(row=3, column=0, columnspan=2, pady=(25, 5))

        tk.Button(
            left_frame,
            text="Excluir Aluno",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            width=22,
            command=self.excluir_aluno
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # ===== BLOCO DIREITO =====
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(
            right_frame,
            text="Alunos Cadastrados",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=26,
            fieldbackground="white"
        )

        # Tabela
        self.alunos_tree = ttk.Treeview(
            right_frame,
            columns=("Nome", "Turma"),
            show="headings",
            height=10
        )

        self.alunos_tree.heading("Nome", text="Nome")
        self.alunos_tree.heading("Turma", text="Turma")

        self.alunos_tree.column("Nome", width=220)
        self.alunos_tree.column("Turma", width=90, anchor="center")

        self.alunos_tree.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            right_frame,
            orient="vertical",
            command=self.alunos_tree.yview
        )
        self.alunos_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        self.alunos_tree.tag_configure(
            "selecionado",
            background="#d6eaff"
        )

        # Seleção da linha
        def ao_selecionar_linha(event):
            selecionados = self.alunos_tree.selection()
            if not selecionados:
                return

            item = selecionados[0]

            # limpa destaque visual anterior
            for i in self.alunos_tree.get_children():
                self.alunos_tree.item(i, tags=())

            # aplica destaque
            self.alunos_tree.item(item, tags=("selecionado",))

            # pega os valores corretos
            nome, turma = self.alunos_tree.item(item, "values")

            self.nome_aluno_var.set(nome)
            self.turma_var.set(turma)


        self.alunos_tree.bind("<<TreeviewSelect>>", ao_selecionar_linha)

        self.carregar_alunos()


    def create_livro_tab(self, notebook):
        """Cria a aba para cadastro de livros"""
        livro_frame = tk.Frame(notebook, bg="#f0f0f0")
        notebook.add(livro_frame, text="Cadastrar Livro")

        # Título
        title_label = tk.Label(
            livro_frame,
            text="Cadastrar Novo Livro",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=20)

        # Frame para formulário
        form_frame = tk.Frame(livro_frame, bg="#f0f0f0")
        form_frame.pack(pady=20)

        # Nome do livro
        nome_label = tk.Label(
            form_frame,
            text="Nome do Livro:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        nome_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.nome_livro_var = tk.StringVar()
        nome_entry = tk.Entry(
            form_frame,
            textvariable=self.nome_livro_var,
            font=("Arial", 12),
            width=50
        )
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        # Frame para botões
        btn_frame = tk.Frame(form_frame, bg="#f0f0f0")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)

        # Botão para cadastrar livro
        cadastrar_livro_btn = tk.Button(
            btn_frame,
            text="Cadastrar Livro",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            bg="#3498db",
            fg="white",
            relief="raised",
            bd=3,
            command=self.cadastrar_livro
        )
        cadastrar_livro_btn.pack(side="left", padx=10)

        # Botão para excluir livro
        excluir_livro_btn = tk.Button(
            btn_frame,
            text="Excluir Livro",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            bg="#e74c3c",
            fg="white",
            relief="raised",
            bd=3,
            command=self.excluir_livro
        )
        excluir_livro_btn.pack(side="left", padx=10)

        # Lista de livros cadastrados
        lista_frame = tk.Frame(livro_frame, bg="#f0f0f0")
        lista_frame.pack(fill="both", expand=True, padx=20, pady=10)

        lista_label = tk.Label(
            lista_frame,
            text="Livros Cadastrados:",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        lista_label.pack(anchor="w")

        # Listbox para mostrar livros
        listbox_frame = tk.Frame(lista_frame)
        listbox_frame.pack(fill="both", expand=True)

        self.livros_listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 11),
            height=25
        )

        # Scrollbar para a lista
        scrollbar_livros = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.livros_listbox.yview)
        self.livros_listbox.configure(yscrollcommand=scrollbar_livros.set)

        self.livros_listbox.pack(side="left", fill="both", expand=True)
        scrollbar_livros.pack(side="right", fill="y")

        self.carregar_livros()

    def create_year_passes(self, notebook):
        """Cria a aba para passagem de ano"""
        year_frame = tk.Frame(notebook, bg="#f0f0f0")
        notebook.add(year_frame, text="Passagem de Ano")

        # Título
        title_label = tk.Label(
            year_frame,
            text="Passagem do Ano Escolar",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=20)

        # Instrução da passagem de ano
        instructions_label = tk.Label(
            year_frame,
            text="Clique no botão abaixo para avançar todos os alunos para o próximo ano.",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        instructions_label.pack(pady=10)

        # Botão para avançar ano
        avancar_ano_btn = tk.Button(
            year_frame,
            text="Avançar Ano Escolar",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            bg="#2980b9",
            fg="white",
            relief="raised",
            bd=3,
            command=self.avancar_ano_escolar
        )
        avancar_ano_btn.pack(pady=20)

    def create_historico_tab(self, notebook):
        #Aba 'Histórico' com todos os empréstimos
        historico_frame = tk.Frame(notebook, bg="#f0f0f0")
        notebook.add(historico_frame, text="Histórico")

        title_label = tk.Label(
            historico_frame,
            text="Histórico de Empréstimos",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)

        # Frame da tabela
        main_frame = tk.Frame(historico_frame, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Estilo
        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=28,
            bordercolor="#d0d0d0",
            relief="flat"
        )
        style.map("Treeview", background=[("selected", "white")], foreground=[("selected", "black")])

        # Colunas
        cols = ("id", "turma", "aluno", "livro", "data_emprestimo", "data_devolucao_real", "situacao")
        self.historico_tree = ttk.Treeview(main_frame, columns=cols, show="headings", height=20)

        headings = {
            "turma": "Turma",
            "aluno": "Aluno",
            "livro": "Livro",
            "data_emprestimo": "Data de Empréstimo",
            "data_devolucao_real": "Data de Devolução",
            "situacao": "Situação"
        }

        for col in cols:
            if col == "id":
                self.historico_tree.heading(col, text="")
                self.historico_tree.column(col, width=1, stretch=False)
                continue

            if col == "turma":
                width = 25
            elif col == "aluno" or col == "livro":
                width = 220
            elif col == "situacao":
                width = 110
                self.historico_tree.column(col, anchor="center")
            elif col == "data_emprestimo" or col == "data_devolucao_real":
                width = 90
            else:
                width = 140

            self.historico_tree.heading(col, text=headings[col])
            self.historico_tree.column(col, width=width, anchor="w")

        # dicionário para guardar os Labels que vamos sobrepor (chave = item_id)
        self._situacao_labels = {}

        # Scrollbar: usamos _on_treeview_scroll para garantir reposicionamento dos labels ao rolar
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self._on_treeview_scroll)
        self.historico_tree.configure(yscrollcommand=vsb.set)

        self.historico_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Alterar situação ao clicar na célula
        self.historico_tree.bind("<Button-1>", self.clicar_historico)
        
        # Frame dos botões
        btns_frame = tk.Frame(historico_frame, bg="#f0f0f0")
        btns_frame.pack(fill="x", pady=8)

        atualizar_btn = tk.Button(
            btns_frame,
            text="Atualizar",
            font=("Arial", 12, "bold"),
            width=12,
            bg="#2980b9",
            fg="white",
            command=self.carregar_historico
        )
        atualizar_btn.pack(side="left", padx=6)

        # Tags para simular botões (não usadas para a célula, mas mantidas se necessário)
        self.historico_tree.tag_configure("pendente", background="#ffcccc", foreground="black", font=("Arial", 10, "bold"))
        self.historico_tree.tag_configure("devolvido", background="#ccffcc", foreground="black", font=("Arial", 10, "bold"))

        # Carrega os dados iniciais
        self.carregar_historico()

        # bindings para reposicionar labels quando necessário
        self.historico_tree.bind("<Configure>", lambda e: self._reposicionar_labels_situacao())
        self.historico_tree.bind("<Motion>", lambda e: self._reposicionar_labels_situacao())
        
        # mousewheel bindings — atualizam posicao dos labels ao rolar com roda do mouse
        self.historico_tree.bind_all("<MouseWheel>", lambda e: self._reposicionar_labels_situacao())
        self.historico_tree.bind_all("<Button-4>", lambda e: self._reposicionar_labels_situacao())
        self.historico_tree.bind_all("<Button-5>", lambda e: self._reposicionar_labels_situacao())

    def _on_treeview_scroll(self, *args):
        # Função que substitui o comando do scrollbar e reposiciona os labels.
        try:
            self.historico_tree.yview(*args)
        except Exception:
            pass
        self._reposicionar_labels_situacao()

    def _reposicionar_labels_situacao(self):
        # Atualiza a posição (place) de todos os labels de situação conforme bbox do Treeview.
        for item_id, lbl in list(self._situacao_labels.items()):
            try:
                bbox = self.historico_tree.bbox(item_id, column="situacao")
            except Exception:
                bbox = ()
            if not bbox:
                try:
                    lbl.place_forget()
                except Exception:
                    pass
                continue

            x, y, width, height = bbox
            try:
                lbl.place(in_=self.historico_tree, x=x+1, y=y+1, width=width-2, height=height-2)
            except Exception:
                pass

    def _limpar_labels_situacao(self):
        # Remove todos os labels antigos.
        for lbl in list(self._situacao_labels.values()):
            try:
                lbl.destroy()
            except Exception:
                pass
        self._situacao_labels.clear()

    def carregar_historico(self):
        # Carrega todos os empréstimos no Treeview com cor apenas na célula da situação
        for item in self.historico_tree.get_children():
            self.historico_tree.delete(item)
        self._limpar_labels_situacao()

        try:
            rows = self.db.get_all_emprestimos_detalhados()

            for i, r in enumerate(rows):
                situacao_real = "pendente" if (r.get("data_devolucao_real") in (None, "")) else "devolvido"
                texto_botao = f"{situacao_real.upper()}"

                tag_linha = "linha_par" if i % 2 == 0 else "linha_impar"

                item_id = self.historico_tree.insert(
                    "",
                    "end",
                    values=(
                        r.get("id"),
                        r.get("turma") or "",
                        r.get("aluno") or "",
                        r.get("livro") or "",
                        r.get("data_emprestimo") or "",
                        r.get("data_devolucao_real") or "",
                        ""
                    ),
                    tags=(tag_linha,)
                )

                cor = "#ffcccc" if situacao_real == "pendente" else "#89bfe3"
                lbl = tk.Label( 
                    self.historico_tree,
                    text=texto_botao,
                    bg=cor,
                    fg="black",
                    font=("Arial", 10, "bold"),
                    bd=1,
                    relief="solid",
                    padx=4,
                    pady=2
                )
                lbl.bind('<Button-1>', lambda e, item_id=item_id: self._trocar_situacao(item_id))

                self._situacao_labels[item_id] = lbl

            # estilos das linhas alternadas
            self.historico_tree.tag_configure("linha_par", background="#ffffff")
            self.historico_tree.tag_configure("linha_impar", background="#f5f5f5")

            # depois de inserir tudo, reposicionar os labels (alguns estarão visíveis)
            self._reposicionar_labels_situacao()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {e}")

    
    def _trocar_situacao(self, item_id):
        valores = self.historico_tree.item(item_id, "values")
        emprestimo_id = valores[0]
        try:
            self.db.toggle_emprestimo_situacao(int(emprestimo_id))
            self.carregar_historico()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alternar situação: {e}")

    def clicar_historico(self, event):
            self.historico_tree.selection_remove(self.historico_tree.selection())

            item = self.historico_tree.identify_row(event.y)
            col = self.historico_tree.identify_column(event.x)

            if col != "#7":
                return

            if not item:
                return

            valores = self.historico_tree.item(item, "values")
            emprestimo_id = valores[0]

            try:
                self.db.toggle_emprestimo_situacao(int(emprestimo_id))
                self.carregar_historico()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao alternar situação: {e}")


    def create_manual(self, notebook):
        '''Cria a aba do manual de instruções com scrollbar'''
        import tkinter as tk

        manual_frame = tk.Frame(notebook, bg="#f0f0f0")
        notebook.add(manual_frame, text="Manual de Instruções")

        # Título
        title_label = tk.Label(
            manual_frame,
            text="Manual de Instruções",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=20)

        # Frame para texto + scrollbar
        text_frame = tk.Frame(manual_frame, bg="#f0f0f0")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        # Campo de texto com scrollbar
        text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=("Arial", 11),
            padx=10,
            pady=10,
            yscrollcommand=scrollbar.set,
            bg="#ffffff",
            relief="groove",
            height=20
        )
        text_widget.pack(fill="both", expand=True)

        scrollbar.config(command=text_widget.yview)

        # Texto do manual
        manual_text = (
            "Manual – Fluxo de Uso para Professores\n\n"
            "• Consultar Alunos e Turmas\n"
            "Ao abrir o sistema, selecione uma das turmas listadas na tela principal\n\n"

            "• Tabelas de Empréstimo\n"
            "- Empréstimos Atuais: empréstimos em curso.\n"
            "- Empréstimos Anteriores: registros anteriores.\n\n"

            "• Registrar Empréstimos\n"
            "1) Abra uma turma.\n"
            "2) Selecione o aluno.\n"
            "3) Escreva o livro.\n"
            "4) Confirme o registro clicando em salvar.\n"
            "O empréstimo aparecerá na tabela da Semana Atual.\n\n"

            "• Avançar Semana\n"
            "Clique no botão Avancar para dar início à novos empréstimos\n\n"

            "• Registrar Devoluções\n"
            "A data de devolução será salva após ser designado um novo livro ao aluno\n\n"

            "• Passagem de Ano Escolar\n"
            "- Use 'Avançar Ano Escolar' no fim do ano letivo.\n"
            "- Todos os alunos avançam de série automaticamente.\n"
            "- Alunos do 9º ano são removidos da tabela, mas permanecem no histórico.\n\n"

            "• Histórico\n"
            "- Na aba histórico está todos os registros de empréstimos.\n"
            "- Para alterar a situação de um empréstimo, clique na célula.\n"
            
            "• Outras Informações\n"
            "- Não mova a pasta Sistema Biblioteca\n"
            "- Caso indentificado algum problema ou dúvida, por favor entre em contato com o telefone (54) 9351-3835"
        )

        # Inserir texto no widget
        text_widget.insert("1.0", manual_text)
        text_widget.config(state="disabled")

        return text_widget

    def avancar_ano_escolar(self):
        # Avança todos os alunos para o próximo ano
        confirm = messagebox.askyesno("Confirmar Passagem de Ano", "Tem certeza que deseja avançar todos os alunos para o próximo ano?")
        if confirm:
            sucesso = self.db.avancar_ano()
            if sucesso:
                messagebox.showinfo("Sucesso", "Todos os alunos foram avançados para o próximo ano com sucesso!")
                self.carregar_alunos()
            else:
                messagebox.showerror("Erro", "Erro ao avançar o ano escolar.")


    def cadastrar_aluno(self):
        """Cadastra um novo aluno"""
        nome = self.nome_aluno_var.get().strip()
        turma = self.turma_var.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Por favor, digite o nome do aluno.")
            return

        if not turma:
            messagebox.showerror("Erro", "Por favor, selecione uma turma.")
            return

        # Inserir no banco
        sucesso = self.db.inserir_aluno(nome, turma)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado com sucesso!")
            self.nome_aluno_var.set("")
            self.turma_var.set("")
            self.carregar_alunos()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar aluno.")

    def excluir_aluno(self):
        """Exclui um aluno selecionado"""
        selected_item = self.alunos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um aluno para excluir.")
            return

        aluno = self.alunos_tree.item(selected_item)['values'][0]
        turma = self.alunos_tree.item(selected_item)['values'][1]

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o aluno '{aluno}' da turma '{turma}'?")
        if confirm:
            sucesso = self.db.excluir_aluno(aluno, turma)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Aluno '{aluno}' excluído com sucesso!")
                self.carregar_alunos()
            else:
                messagebox.showerror("Erro", "Erro ao excluir aluno.")

    def cadastrar_livro(self):
        """Cadastra um novo livro"""
        nome = self.nome_livro_var.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Por favor, digite o nome do livro.")
            return

        # Inserir no banco
        sucesso = self.db.inserir_livro(nome)

        if sucesso:
            self.nome_livro_var.set("")
            self.carregar_livros()
        else:
            messagebox.showerror("Erro", "Livro já existe ou erro ao cadastrar.")

    def excluir_livro(self):
        """Exclui um livro selecionado"""
        selected_item = self.livros_listbox.curselection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro para excluir.")
            return

        livro = self.livros_listbox.get(selected_item)

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o livro '{livro}'?")
        if confirm:
            sucesso = self.db.excluir_livro(livro)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Livro '{livro}' excluído com sucesso!")
                self.carregar_livros()
            else:
                messagebox.showerror("Erro", "Erro ao excluir livro.")

    def carregar_alunos(self):
        """Carrega a lista de alunos cadastrados"""
        # Limpar treeview
        for item in self.alunos_tree.get_children():
            self.alunos_tree.delete(item)

        # Buscar todos os alunos
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT nome, turma FROM alunos ORDER BY turma, nome")
            alunos = cursor.fetchall()

            for nome, turma in alunos:
                self.alunos_tree.insert("", "end", values=(nome, turma))

            conn.close()
        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")

    def carregar_livros(self):
        """Carrega a lista de livros cadastrados"""
        # Limpar listbox
        self.livros_listbox.delete(0, tk.END)

        # Buscar todos os livros
        livros = self.db.get_todos_livros()

        for livro in livros:
            self.livros_listbox.insert(tk.END, livro)