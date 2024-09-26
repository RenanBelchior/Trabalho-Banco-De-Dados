import mysql.connector

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
    print(f"{cursor.rowcount} produto(s) inserido(s).")
    cursor.close()
    connection.close()


def read_products():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM produtos")
    result = cursor.fetchall()
    for row in result:
        print(f"ID: {row[0]} | Produto: {row[1]} | Preço: R$ {row[2]:.2f} | Quantidade: {row[3]}")
    cursor.close()
    connection.close()



def update_product(product_id, nome, preco, quantidade):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "UPDATE produtos SET nome=%s, preco=%s, quantidade=%s WHERE id=%s"
    val = (nome, preco, quantidade, product_id)
    cursor.execute(sql, val)
    connection.commit()
    print(f"{cursor.rowcount} produto(s) atualizado(s).")
    cursor.close()
    connection.close()


def delete_product(product_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "DELETE FROM produtos WHERE id=%s"
    val = (product_id,)
    cursor.execute(sql, val)
    connection.commit()
    print(f"{cursor.rowcount} produto(s) deletado(s).")
    cursor.close()
    connection.close()


def main():
    create_table()

    while True:
        print("\nOpções CRUD para Produtos:")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Atualizar produto")
        print("4. Deletar produto")
        print("5. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))
            create_product(nome, preco, quantidade)
        elif choice == "2":
            read_products()
        elif choice == "3":
            product_id = int(input("ID do produto: "))
            nome = input("Novo nome do produto: ")
            preco = float(input("Novo preço: "))
            quantidade = int(input("Nova quantidade: "))
            update_product(product_id, nome, preco, quantidade)
        elif choice == "4":
            product_id = int(input("ID do produto para deletar: "))
            delete_product(product_id)
        elif choice == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()