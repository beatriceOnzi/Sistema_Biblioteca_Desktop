## database.py
import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name="biblioteca.db"):
        self.db_name = db_name
        self.init_database()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def init_database(self):
        conn = self.connect()
        cur = conn.cursor()

        # Tabela de alunos
        cur.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                turma TEXT NOT NULL
            )
        ''')

        # Tabela de livros
        cur.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        ''')

        # Tabela de empréstimos — agora com campo turma
        cur.execute('''
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                livro_id INTEGER,
                data_emprestimo TEXT,
                data_devolucao_prevista TEXT,
                data_devolucao_real TEXT,
                semana TEXT,
                turma TEXT,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id),
                FOREIGN KEY (livro_id) REFERENCES livros (id)
            )
        ''')

        # Tabela config_turma
        cur.execute('''
            CREATE TABLE IF NOT EXISTS config_turma (
                turma TEXT PRIMARY KEY,
                semana_atual INTEGER
            )
        ''')

        conn.commit()
        conn.close()

    # ---------------- helpers de data ----------------
    def _parse_date_flexible(self, s):
        if not s:
            return datetime.now()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                continue
        return datetime.now()

    # ---------------- config por turma ----------------
    def get_semana_atual_turma(self, turma):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT semana_atual FROM config_turma WHERE turma = ?", (turma,))
        row = cur.fetchone()

        if row and row[0] is not None:
            conn.close()
            return row[0]

        # primeira semana da turma
        cur.execute(
            "INSERT OR REPLACE INTO config_turma (turma, semana_atual) VALUES (?, ?)",
            (turma, 1)
        )
        conn.commit()
        conn.close()
        return 1

    def get_semana_anterior_turma(self, turma):
        atual = self.get_semana_atual_turma(turma)
        return atual - 1 if atual > 1 else None


    def get_data_atual_sistema(self):
        hoje = datetime.now().strftime("%d/%m/%Y")
        return self._parse_date_flexible(hoje)

    def _ensure_config_turma_row(self, turma, semana_atual=None, semana_anterior=None):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM config_turma WHERE turma = ?", (turma,))
        if cur.fetchone():
            if semana_atual is not None:
                cur.execute("UPDATE config_turma SET semana_atual = ? WHERE turma = ?", (semana_atual, turma))
            if semana_anterior is not None:
                cur.execute("UPDATE config_turma SET semana_anterior = ? WHERE turma = ?", (semana_anterior, turma))
        else:
            cur.execute("INSERT INTO config_turma (turma, semana_atual, semana_anterior) VALUES (?, ?, ?)",
                        (turma, semana_atual or datetime.now().strftime("%d/%m/%Y"),
                         semana_anterior or (semana_atual or datetime.now().strftime("%d/%m/%Y"))))
        conn.commit()
        conn.close()

    def set_semana_atual_turma(self, turma, data_dt):
        s = data_dt.strftime("%d/%m/%Y")
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO config_turma (turma, semana_atual, semana_anterior)
            VALUES (?, COALESCE((SELECT semana_atual FROM config_turma WHERE turma=?), ?),
                        COALESCE((SELECT semana_anterior FROM config_turma WHERE turma=?), ?))
        """, (turma, turma, s, turma, s))
        cur.execute("UPDATE config_turma SET semana_atual = ? WHERE turma = ?", (s, turma))
        conn.commit()
        conn.close()

    # ---------------- CRUDs mantidos ----------------
    def inserir_aluno(self, nome, turma):
        conn = self.connect()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO alunos (nome, turma) VALUES (?, ?)", (nome, turma))
            conn.commit()
            return True
        except Exception as e:
            print("Erro inserir_aluno:", e)
            return False
        finally:
            conn.close()

    def excluir_aluno(self, nome, turma):
        conn = self.connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM alunos WHERE nome = ? AND turma = ?", (nome, turma))
            conn.commit()
            return True
        except Exception as e:
            print("Erro excluir_aluno:", e)
            return False
        finally:
            conn.close()

    def inserir_livro(self, nome):
        conn = self.connect()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO livros (nome) VALUES (?)", (nome,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print("Erro inserir_livro:", e)
            return False
        finally:
            conn.close()

    def excluir_livro(self, nome):
        conn = self.connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM livros WHERE nome = ?", (nome,))
            conn.commit()
            return True
        except Exception as e:
            print("Erro excluir_livro:", e)
            return False
        finally:
            conn.close()

    def get_alunos_por_turma(self, turma):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM alunos WHERE turma = ? ORDER BY nome", (turma,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_todos_livros(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT nome FROM livros ORDER BY nome")
        rows = [r[0] for r in cur.fetchall()]
        conn.close()
        return rows

    def get_livro_id(self, nome_livro):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT id FROM livros WHERE nome = ?", (nome_livro,))
        r = cur.fetchone()
        conn.close()
        return r[0] if r else None

    # ===============================
    #   INSERIR AGORA COM TURMA !!!
    # ===============================
    def inserir_emprestimo(self, aluno_id, livro_id, data_emprestimo, data_devolucao_prevista, semana):
        conn = self.connect()
        cur = conn.cursor()

        # Pegando turma do aluno
        cur.execute("SELECT turma FROM alunos WHERE id = ?", (aluno_id,))
        turma_row = cur.fetchone()
        turma = turma_row[0] if turma_row else ""

        try:
            cur.execute('''
                INSERT INTO emprestimos (aluno_id, livro_id, data_emprestimo, data_devolucao_prevista, semana, turma)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (aluno_id, livro_id, data_emprestimo, data_devolucao_prevista, semana, turma))
            conn.commit()
            return True
        except Exception as e:
            print("Erro inserir_emprestimo:", e)
            return False
        finally:
            conn.close()

    def atualizar_emprestimo(self, aluno_id, livro_id, data_emprestimo, data_devolucao_prevista, semana):
        conn = self.connect()
        cur = conn.cursor()
        try:
            # Atualiza sem mexer no histórico
            cur.execute('''
                UPDATE emprestimos
                SET livro_id = ?, data_emprestimo = ?, data_devolucao_prevista = ?
                WHERE aluno_id = ? AND semana = ?
            ''', (livro_id, data_emprestimo, data_devolucao_prevista, aluno_id, semana))
            conn.commit()
            return True
        except Exception as e:
            print("Erro atualizar_emprestimo:", e)
            return False
        finally:
            conn.close()

    def verificar_emprestimo_existente(self, aluno_id, semana):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT id FROM emprestimos WHERE aluno_id = ? AND semana = ?", (aluno_id, semana))
        r = cur.fetchone()
        conn.close()
        return r is not None

    def atualizar_devolucao_real(self, aluno_id, semana, data_devolucao):
        if semana is None:
            return 0

        conn = self.connect()
        cur = conn.cursor()
        try:
            # só atualiza se existir empréstimo naquela semana
            cur.execute("""
                UPDATE emprestimos
                SET data_devolucao_real = ?
                WHERE aluno_id = ?
                AND semana = ?
                AND livro_id IS NOT NULL
                AND (data_devolucao_real IS NULL OR data_devolucao_real = '')
            """, (data_devolucao, aluno_id, semana))

            conn.commit()
            return cur.rowcount
        except Exception as e:
            print("Erro atualizar_devolucao_real:", e)
            return 0
        finally:
            conn.close()


    # ---------------- consultas por turma ----------------
    def get_all_emprestimos_detalhados(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.id,
                   COALESCE(e.turma, a.turma),
                   a.nome,
                   l.nome,
                   e.data_emprestimo,
                   e.data_devolucao_real
            FROM emprestimos e
            LEFT JOIN alunos a ON e.aluno_id = a.id
            LEFT JOIN livros l ON e.livro_id = l.id
            ORDER BY 
                date(substr(e.data_emprestimo,7,4) || '-' || substr(e.data_emprestimo,4,2) || '-' || substr(e.data_emprestimo,1,2)) DESC
        """)
        rows = cur.fetchall()
        conn.close()

        result = []
        for r in rows:
            result.append({
                "id": r[0],
                "turma": r[1],
                "aluno": r[2],
                "livro": r[3],
                "data_emprestimo": r[4],
                "data_devolucao_real": r[5]
            })
        return result

    def get_emprestimos_semana_atual(self, turma):
        semana_atual = self.get_semana_atual_turma(turma)
        conn = self.connect()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.data_emprestimo, a.nome, l.nome, e.data_devolucao_prevista
            FROM emprestimos e
            JOIN alunos a ON e.aluno_id = a.id
            JOIN livros l ON e.livro_id = l.id
            WHERE a.turma = ? AND e.semana = ?
            ORDER BY a.nome
        ''', (turma, semana_atual))
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_emprestimos_semana_anterior(self, turma):
        semana_anterior = self.get_semana_anterior_turma(turma)
        conn = self.connect()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.data_emprestimo, a.nome, l.nome, e.data_devolucao_prevista, e.data_devolucao_real
            FROM emprestimos e
            JOIN alunos a ON e.aluno_id = a.id
            JOIN livros l ON e.livro_id = l.id
            WHERE a.turma = ? AND e.semana = ?
            ORDER BY a.nome
        ''', (turma, semana_anterior))
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_historico_emprestimos_por_turma(self, turma):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.semana, e.data_emprestimo, a.nome, l.nome, e.data_devolucao_real
            FROM emprestimos e
            JOIN alunos a ON e.aluno_id = a.id
            JOIN livros l ON e.livro_id = l.id
            WHERE e.turma = ?
            ORDER BY e.semana DESC, a.nome
        ''', (turma,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_semanas_por_turma(self, turma):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute('''
            SELECT DISTINCT e.semana
            FROM emprestimos e
            WHERE e.turma = ?
            ORDER BY e.semana DESC
        ''', (turma,))
        rows = [r[0] for r in cur.fetchall()]
        conn.close()
        return rows

    def get_emprestimos_por_semana_turma(self, turma, semana):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.data_emprestimo, a.nome, l.nome, e.data_devolucao_prevista, e.data_devolucao_real
            FROM emprestimos e
            JOIN alunos a ON e.aluno_id = a.id
            JOIN livros l ON e.livro_id = l.id
            WHERE e.turma = ? AND e.semana = ?
            ORDER BY a.nome
        ''', (turma, semana))
        rows = cur.fetchall()
        conn.close()
        return rows

    # ---------------- histórico ----------------
    def toggle_emprestimo_situacao(self, emprestimo_id):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT data_devolucao_real FROM emprestimos WHERE id = ?", (emprestimo_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            raise ValueError("Empréstimo não encontrado")
        current = row[0]
        if current is None or str(current).strip() == "":
            new_date = datetime.now().strftime("%d/%m/%Y")
            cur.execute("UPDATE emprestimos SET data_devolucao_real = ? WHERE id = ?", (new_date, emprestimo_id))
            conn.commit()
            conn.close()
            return new_date
        else:
            cur.execute("UPDATE emprestimos SET data_devolucao_real = NULL WHERE id = ?", (emprestimo_id,))
            conn.commit()
            conn.close()
            return None

    # ---------------- finalizar e avançar semana por turma ----------------
    def finalizar_e_avancar_semana(self, turma):
        try:
            conn = self.connect()
            cur = conn.cursor()

            # garante semana atual
            cur.execute(
                "SELECT semana_atual FROM config_turma WHERE turma = ?",
                (turma,)
            )
            row = cur.fetchone()

            if row and row[0] is not None:
                semana_atual = int(row[0])
            else:
                semana_atual = 1
                cur.execute(
                    "INSERT OR REPLACE INTO config_turma (turma, semana_atual) VALUES (?, ?)",
                    (turma, semana_atual)
                )
                conn.commit()

            # avança semana (contador)
            nova_semana = semana_atual + 1

            cur.execute(
                "UPDATE config_turma SET semana_atual = ? WHERE turma = ?",
                (nova_semana, turma)
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print("Erro em finalizar_e_avancar_semana:", e)
            try:
                conn.close()
            except:
                pass
            return False

    def avancar_ano(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE alunos
                SET turma = ''
                WHERE turma = '9º Ano'
            """)

            cursor.execute("""
                UPDATE alunos
                SET turma = CASE
                    WHEN turma = '1º Ano' THEN '2º Ano'
                    WHEN turma = '2º Ano' THEN '3º Ano'
                    WHEN turma = '3º Ano' THEN '4º Ano'
                    WHEN turma = '4º Ano' THEN '5º Ano'
                    WHEN turma = '5º Ano' THEN '6º Ano'
                    WHEN turma = '6º Ano' THEN '7º Ano'
                    WHEN turma = '7º Ano' THEN '8º Ano'
                    WHEN turma = '8º Ano' THEN '9º Ano'
                    ELSE turma
                END
            """)
            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Erro ao avançar o ano escolar: {e}")
            return False

        finally:
            conn.close()
