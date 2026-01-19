import tkinter as tk
from tkinter import ttk

def complete_text(self, entry, var):
        # ===== Frame do autocomplete =====
        listbox_frame = tk.Frame(self.window, bg="white", relief="solid", bd=1)

        listbox = tk.Listbox(
            listbox_frame,
            height=8,
            font=("Arial", 9),
            activestyle="none"
        )

        scrollbar = ttk.Scrollbar(
            listbox_frame,
            orient="vertical",
            command=listbox.yview
        )

        listbox.configure(yscrollcommand=scrollbar.set)

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        listbox_frame.place_forget()

        # ===== Atualizar sugestões =====
        def update_list(event=None):
            if event and event.keysym in ['Up', 'Down', 'Return', 'Tab']:
                return

            value = var.get().strip()
            listbox.delete(0, tk.END)

            if not value:
                listbox_frame.place_forget()
                return

            matches = [
                livro for livro in self.livros_disponiveis
                if livro.lower().startswith(value.lower())
            ]

            if not matches:
                listbox_frame.place_forget()
                return

            for match in matches[:50]:  # pode ter muitos livros, mas mostramos com scroll
                listbox.insert(tk.END, match)

            listbox.selection_clear(0, tk.END)
            listbox.selection_set(0)
            listbox.activate(0)

            try:
                entry_x = entry.winfo_rootx() - self.window.winfo_rootx()
                entry_y = entry.winfo_rooty() - self.window.winfo_rooty() + entry.winfo_height()

                max_x = self.window.winfo_width() - 320
                max_y = self.window.winfo_height() - 200

                entry_x = min(entry_x, max_x)
                entry_y = min(entry_y, max_y)

                listbox_frame.place(
                    x=entry_x,
                    y=entry_y,
                    width=min(entry.winfo_width() + 50, 300),
                    height=160
                )
                listbox_frame.lift()
            except:
                listbox_frame.place(x=100, y=100, width=250, height=160)

        # ===== Completar seleção =====
        def complete_from_list(event=None):
            if listbox.curselection():
                selection = listbox.get(listbox.curselection()[0])
                var.set(selection)

            listbox_frame.place_forget()
            entry.icursor(tk.END)
            return 'break'

        # ===== Navegação com teclado =====
        def move_selection(event):
            if not listbox_frame.winfo_ismapped():
                return

            index = listbox.curselection()
            index = index[0] if index else 0

            if event.keysym == 'Down':
                index = min(index + 1, listbox.size() - 1)
            elif event.keysym == 'Up':
                index = max(index - 1, 0)
            else:
                return

            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)
            listbox.activate(index)
            listbox.see(index)
            return 'break'

        # ===== Clique do mouse =====
        def on_listbox_click(event):
            idx = listbox.nearest(event.y)
            if idx >= 0:
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(idx)
                listbox.activate(idx)
                var.set(listbox.get(idx))
                listbox_frame.place_forget()
                entry.focus_set()

        # ===== Esconder quando perde foco =====
        def hide_listbox(event=None):
            self.window.after(150, listbox_frame.place_forget)

        # ===== Bindings =====
        entry.bind('<KeyRelease>', update_list)
        entry.bind('<Return>', complete_from_list)
        entry.bind('<Tab>', complete_from_list)
        entry.bind('<Down>', move_selection)
        entry.bind('<Up>', move_selection)
        entry.bind('<FocusOut>', hide_listbox)

        listbox.bind('<Button-1>', on_listbox_click)
        listbox.bind('<Return>', complete_from_list)
        listbox.bind('<Double-Button-1>', complete_from_list)