import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="estoque"
    )

def create_table():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            preco DECIMAL(10, 2),
            quantidade INT
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def create_product(nome, preco, quantidade):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)"
    val = (nome, preco, quantidade)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()

def read_products(tree):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM produtos")
    result = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in result:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))
    cursor.close()
    connection.close()

def update_product(product_id, nome, preco, quantidade):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "UPDATE produtos SET nome=%s, preco=%s, quantidade=%s WHERE id=%s"
    val = (nome, preco, quantidade, product_id)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()

def delete_product(product_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "DELETE FROM produtos WHERE id=%s"
    val = (product_id,)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()


def add_product_window():
    def save_product():
        nome = nome_entry.get()
        preco = float(preco_entry.get())
        quantidade = int(quantidade_entry.get())
        create_product(nome, preco, quantidade)
        read_products(product_tree)
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Adicionar Produto")

    tk.Label(add_window, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
    nome_entry = tk.Entry(add_window)
    nome_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Preço:").grid(row=1, column=0, padx=10, pady=5)
    preco_entry = tk.Entry(add_window)
    preco_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5)
    quantidade_entry = tk.Entry(add_window)
    quantidade_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Salvar", command=save_product).grid(row=3, column=0, columnspan=2, pady=10)

def edit_product_window():
    try:
        selected_item = product_tree.selection()[0]
        selected_product = product_tree.item(selected_item)['values']
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um produto para editar.")
        return

    def save_edited_product():
        nome = nome_entry.get()
        preco = float(preco_entry.get())
        quantidade = int(quantidade_entry.get())
        update_product(selected_product[0], nome, preco, quantidade)
        read_products(product_tree)
        edit_window.destroy()

    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Produto")

    tk.Label(edit_window, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
    nome_entry = tk.Entry(edit_window)
    nome_entry.insert(0, selected_product[1])
    nome_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Preço:").grid(row=1, column=0, padx=10, pady=5)
    preco_entry = tk.Entry(edit_window)
    preco_entry.insert(0, selected_product[2])
    preco_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5)
    quantidade_entry = tk.Entry(edit_window)
    quantidade_entry.insert(0, selected_product[3])
    quantidade_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(edit_window, text="Salvar", command=save_edited_product).grid(row=3, column=0, columnspan=2, pady=10)

def delete_selected_product():
    try:
        selected_item = product_tree.selection()[0]
        product_id = product_tree.item(selected_item)['values'][0]
        delete_product(product_id)
        read_products(product_tree)
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um produto para deletar.")


root = tk.Tk()
root.title("Sistema de Estoque")


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)


columns = ("ID", "Nome", "Preço", "Quantidade")
product_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    product_tree.heading(col, text=col)

product_tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)


scroll_y = tk.Scrollbar(root, orient="vertical", command=product_tree.yview)
scroll_y.grid(row=0, column=4, sticky="ns")
product_tree.configure(yscrollcommand=scroll_y.set)


tk.Button(root, text="Adicionar Produto", command=add_product_window).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Editar Produto", command=edit_product_window).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Deletar Produto", command=delete_selected_product).grid(row=1, column=2, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Atualizar Lista", command=lambda: read_products(product_tree)).grid(row=1, column=3, padx=10, pady=5, sticky="ew")


create_table()
read_products(product_tree)
root.mainloop()
