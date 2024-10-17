from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView, TreeViewLabel
import sqlite3

# Configurações do banco de dados
DB_NAME = 'questao1mer.db'

def conectar():
    return sqlite3.connect(DB_NAME)

def executar_query(query, params=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    conn.close()

def consultar_tabela(tabela, filtro=None):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute(f"SELECT * FROM {tabela} WHERE Nome LIKE ?", ('%' + filtro + '%',))
    else:
        cursor.execute(f"SELECT * FROM {tabela}")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def criar_tabelas():
    query_clientes = """
    CREATE TABLE IF NOT EXISTS Tbl_Clientes (
        idTbl_Clientes INTEGER PRIMARY KEY AUTOINCREMENT,
        Numero INTEGER,
        Nome TEXT,
        Endereco TEXT
    )
    """
    executar_query(query_clientes)

class GerenciamentoClientesApp(App):
    def build(self):
        self.title = "Gerenciamento de Clientes"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campos de entrada
        self.numero_input = TextInput(hint_text="Número", multiline=False)
        self.nome_input = TextInput(hint_text="Nome", multiline=False)
        self.endereco_input = TextInput(hint_text="Endereço", multiline=False)
        self.buscar_input = TextInput(hint_text="Buscar por Nome", multiline=False)

        layout.add_widget(self.numero_input)
        layout.add_widget(self.nome_input)
        layout.add_widget(self.endereco_input)
        layout.add_widget(self.buscar_input)

        # Botões
        button_layout = BoxLayout(size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="Incluir", on_press=self.incluir_cliente))
        button_layout.add_widget(Button(text="Alterar", on_press=self.alterar_cliente))
        button_layout.add_widget(Button(text="Excluir", on_press=self.excluir_cliente))
        button_layout.add_widget(Button(text="Buscar", on_press=self.buscar_cliente))

        layout.add_widget(button_layout)

        # Tabela para exibir clientes
        self.tree_view = TreeView(hide_root=True)
        layout.add_widget(self.tree_view)

        # Cria as tabelas no banco de dados
        criar_tabelas()
        self.consultar_clientes()

        return layout

    def incluir_cliente(self, instance):
        numero = self.numero_input.text
        nome = self.nome_input.text
        endereco = self.endereco_input.text
        query = "INSERT INTO Tbl_Clientes (Numero, Nome, Endereco) VALUES (?, ?, ?)"
        executar_query(query, (numero, nome, endereco))
        self.consultar_clientes()

    def alterar_cliente(self, instance):
        selected_item = self.tree_view.selected_node
        if not selected_item:
            return

        cliente_id = selected_item.text.split(":")[0]
        numero = self.numero_input.text
        nome = self.nome_input.text
        endereco = self.endereco_input.text
        query = "UPDATE Tbl_Clientes SET Numero = ?, Nome = ?, Endereco = ? WHERE idTbl_Clientes = ?"
        executar_query(query, (numero, nome, endereco, cliente_id))
        self.consultar_clientes()

    def excluir_cliente(self, instance):
        selected_item = self.tree_view.selected_node
        if not selected_item:
            return

        cliente_id = selected_item.text.split(":")[0]
        query = "DELETE FROM Tbl_Clientes WHERE idTbl_Clientes = ?"
        executar_query(query, (cliente_id,))
        self.consultar_clientes()

    def buscar_cliente(self, instance):
        filtro = self.buscar_input.text
        self.consultar_clientes(filtro)

    def consultar_clientes(self, filtro=None):
        self.tree_view.clear_widgets()
        clientes = consultar_tabela("Tbl_Clientes", filtro)
        for cliente in clientes:
            item = TreeViewLabel(text=f"{cliente[0]}: {cliente[2]} ({cliente[1]})")
            self.tree_view.add_node(item)

if __name__ == "__main__":
    GerenciamentoClientesApp().run()
