import mysql.connector
from datetime import datetime

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pedro",
    database="financa_estudio"
)
cursor = conexao.cursor()

# ---------------- FUNÇÕES CLIENTES ---------------- #

def cadastrar_cliente(cursor, conexao):
    nome = input("Nome da cliente: ")
    telefone = input("Telefone com DD: ")
    ultima_visita = input("Data da última visita (DD-MM-AAAA): ")

    try:
        visita_convertida = datetime.strptime(ultima_visita, "%d-%m-%Y")
        visita_sql = visita_convertida.strftime("%Y-%m-%d")
    except ValueError:
        print("⚠️ Data inválida! Use o formato DD-MM-AAAA.")
        return

    total_visita = int(input("Número de visitas: "))

    sql = "INSERT INTO tbl_clientes (nome_cliente, tel_cliente, ultima_visita, total_visita) VALUES (%s,%s,%s,%s)"
    valores = (nome, telefone, visita_sql, total_visita)
    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Cliente cadastrado com sucesso!")

def mostrar_clientes(cursor):
    print("\n--- Mostrar Clientes ---")
    print("1 - Listar todos")
    print("2 - Buscar por ID")
    print("3 - Buscar por Nome completo")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        cursor.execute("SELECT * FROM tbl_clientes")
        clientes = cursor.fetchall()
    elif opcao == 2:
        id_cliente = int(input("Digite o ID do cliente: "))
        cursor.execute("SELECT * FROM tbl_clientes WHERE id_cliente=%s", (id_cliente,))
        clientes = cursor.fetchall()
    elif opcao == 3:
        nome = input("Digite o nome completo do cliente: ")
        cursor.execute("SELECT * FROM tbl_clientes WHERE nome_cliente=%s", (nome,))
        clientes = cursor.fetchall()
    else:
        print("⚠️ Opção inválida!")
        return

    if clientes:
        for c in clientes:
            print(f"ID: {c[0]} | Nome: {c[1]} | Telefone: {c[2]} | Última visita: {c[3]} | Total visitas: {c[4]}")
    else:
        print("Nenhum cliente encontrado.")

def excluir_cliente(cursor, conexao):
    print("\n--- Excluir Cliente ---")
    print("1 - Excluir por ID")
    print("2 - Excluir por Nome completo")
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        id_cliente = int(input("Digite o ID do cliente: "))
        cursor.execute("DELETE FROM tbl_clientes WHERE id_cliente=%s", (id_cliente,))
    elif opcao == 2:
        nome = input("Digite o nome completo do cliente: ")
        cursor.execute("DELETE FROM tbl_clientes WHERE nome_cliente=%s", (nome,))
    else:
        print("⚠️ Opção inválida!")
        return

    conexao.commit()
    print("🗑️ Cliente excluído com sucesso!")

def alterar_cliente(cursor, conexao):
    print("\n--- Alterar Cliente ---")
    print("1 - Alterar por ID")
    print("2 - Alterar por Nome completo")
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        id_cliente = int(input("Digite o ID do cliente: "))
        cursor.execute("SELECT * FROM tbl_clientes WHERE id_cliente=%s", (id_cliente,))
    elif opcao == 2:
        nome = input("Digite o nome completo do cliente: ")
        cursor.execute("SELECT * FROM tbl_clientes WHERE nome_cliente=%s", (nome,))
    else:
        print("⚠️ Opção inválida!")
        return

    cliente = cursor.fetchone()
    if not cliente:
        print("⚠️ Cliente não encontrado.")
        return

    print(f"\nCliente atual: ID={cliente[0]}, Nome={cliente[1]}, Telefone={cliente[2]}, Última visita={cliente[3]}, Total visitas={cliente[4]}")

    # Menu de colunas para alterar
    print("\nQual campo deseja alterar?")
    print("1 - Nome")
    print("2 - Telefone")
    print("3 - Última visita")
    print("4 - Total de visitas")
    print("5 - Alterar todos")
    escolha = int(input("Escolha uma opção: "))

    if escolha == 1:
        novo_nome = input("Novo nome: ")
        sql = "UPDATE tbl_clientes SET nome_cliente=%s WHERE id_cliente=%s"
        valores = (novo_nome, cliente[0])

    elif escolha == 2:
        novo_tel = input("Novo telefone: ")
        sql = "UPDATE tbl_clientes SET tel_cliente=%s WHERE id_cliente=%s"
        valores = (novo_tel, cliente[0])

    elif escolha == 3:
        nova_visita = input("Nova data da última visita (DD-MM-AAAA): ")
        try:
            visita_convertida = datetime.strptime(nova_visita, "%d-%m-%Y")
            visita_sql = visita_convertida.strftime("%Y-%m-%d")
        except ValueError:
            print("⚠️ Data inválida! Use o formato DD-MM-AAAA.")
            return
        sql = "UPDATE tbl_clientes SET ultima_visita=%s WHERE id_cliente=%s"
        valores = (visita_sql, cliente[0])

    elif escolha == 4:
        novo_total = int(input("Novo total de visitas: "))
        sql = "UPDATE tbl_clientes SET total_visita=%s WHERE id_cliente=%s"
        valores = (novo_total, cliente[0])

    elif escolha == 5:
        novo_nome = input("Novo nome: ")
        novo_tel = input("Novo telefone: ")
        nova_visita = input("Nova data da última visita (DD-MM-AAAA): ")
        try:
            visita_convertida = datetime.strptime(nova_visita, "%d-%m-%Y")
            visita_sql = visita_convertida.strftime("%Y-%m-%d")
        except ValueError:
            print("⚠️ Data inválida! Use o formato DD-MM-AAAA.")
            return
        novo_total = int(input("Novo total de visitas: "))
        sql = "UPDATE tbl_clientes SET nome_cliente=%s, tel_cliente=%s, ultima_visita=%s, total_visita=%s WHERE id_cliente=%s"
        valores = (novo_nome, novo_tel, visita_sql, novo_total, cliente[0])

    else:
        print("⚠️ Opção inválida!")
        return

    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Cliente atualizado com sucesso!")

def cadastrar_procedimento(cursor, conexao):
    nome = input("Nome do procedimento/produto: ")
    sql = "INSERT INTO tbl_procedimentos_e_produtos (nome_procedimento) VALUES (%s)"
    valores = (nome,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Procedimento/Produto cadastrado com sucesso!")

def mostrar_procedimentos(cursor):
    print("\n--- Mostrar Procedimentos/Produtos ---")
    print("1 - Listar todos")
    print("2 - Buscar por ID")
    print("3 - Buscar por Nome completo")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        cursor.execute("SELECT * FROM tbl_procedimentos_e_produtos")
        registros = cursor.fetchall()
    elif opcao == 2:
        id_proc = int(input("Digite o ID: "))
        cursor.execute("SELECT * FROM tbl_procedimentos_e_produtos WHERE id_procedimento=%s", (id_proc,))
        registros = cursor.fetchall()
    elif opcao == 3:
        nome = input("Digite o nome completo: ")
        cursor.execute("SELECT * FROM tbl_procedimentos_e_produtos WHERE nome_procedimento=%s", (nome,))
        registros = cursor.fetchall()
    else:
        print("⚠️ Opção inválida!")
        return

    if registros:
        for r in registros:
            print(f"ID: {r[0]} | Nome: {r[1]}")
    else:
        print("Nenhum procedimento/produto encontrado.")

def alterar_procedimento(cursor, conexao):
    print("\n--- Alterar Procedimento/Produto ---")
    print("1 - Alterar por ID")
    print("2 - Alterar por Nome completo")
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        id_proc = int(input("Digite o ID: "))
        cursor.execute("SELECT * FROM tbl_procedimentos_e_produtos WHERE id_procedimento=%s", (id_proc,))
    elif opcao == 2:
        nome = input("Digite o nome completo: ")
        cursor.execute("SELECT * FROM tbl_procedimentos_e_produtos WHERE nome_procedimento=%s", (nome,))
    else:
        print("⚠️ Opção inválida!")
        return

    proc = cursor.fetchone()
    if not proc:
        print("⚠️ Procedimento/Produto não encontrado.")
        return

    print(f"Atual: ID={proc[0]}, Nome={proc[1]}")

    novo_nome = input("Novo nome: ")
    sql = "UPDATE tbl_procedimentos_e_produtos SET nome_procedimento=%s WHERE id_procedimento=%s"
    valores = (novo_nome, proc[0])
    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Procedimento/Produto atualizado com sucesso!")

def excluir_procedimento(cursor, conexao):
    print("\n--- Excluir Procedimento/Produto ---")
    print("1 - Excluir por ID")
    print("2 - Excluir por Nome completo")
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        id_proc = int(input("Digite o ID: "))
        cursor.execute("DELETE FROM tbl_procedimentos_e_produtos WHERE id_procedimento=%s", (id_proc,))
    elif opcao == 2:
        nome = input("Digite o nome completo: ")
        cursor.execute("DELETE FROM tbl_procedimentos_e_produtos WHERE nome_procedimento=%s", (nome,))
    else:
        print("⚠️ Opção inválida!")
        return

    conexao.commit()
    print("🗑️ Procedimento/Produto excluído com sucesso!")

def cadastrar_preco(cursor, conexao):
    print("Cadastrar preços dos procedimentos/produtos")
    id_procd = int(input("Id do procedimento/produto: "))
    preco = float(input("Preço do procedimento/produto em R$: "))

    data_inicio = input("Data do início do preço (DD-MM-AAAA): ")
    data_inicio_sql = datetime.strptime(data_inicio, "%d-%m-%Y").strftime("%Y-%m-%d")

    data_fim = input("Data do fim do preço (DD-MM-AAAA): ")
    data_fim_sql = datetime.strptime(data_fim, "%d-%m-%Y").strftime("%Y-%m-%d")

    sql = "INSERT INTO tbl_precos (procedimento_id, preco, data_inicio, data_fim) VALUES (%s,%s,%s,%s)"
    valores = (id_procd, preco, data_inicio_sql, data_fim_sql)
    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Preço cadastrado com sucesso!")

def mostrar_precos(cursor):
    print("\n--- Mostrar Preços ---")
    print("1 - Listar todos")
    print("2 - Buscar por ID do preço")
    print("3 - Buscar por ID do procedimento/produto")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        cursor.execute("SELECT * FROM tbl_precos")
        precos = cursor.fetchall()
    elif opcao == 2:
        id_preco = int(input("Digite o ID do preço: "))
        cursor.execute("SELECT * FROM tbl_precos WHERE id_preco=%s", (id_preco,))
        precos = cursor.fetchall()
    elif opcao == 3:
        id_proc = int(input("Digite o ID do procedimento/produto: "))
        cursor.execute("SELECT * FROM tbl_precos WHERE procedimento_id=%s", (id_proc,))
        precos = cursor.fetchall()
    else:
        print("⚠️ Opção inválida!")
        return

    if precos:
        for p in precos:
            print(f"ID Preço: {p[0]} | Procedimento ID: {p[1]} | Valor: R${p[2]} | Início: {p[3]} | Fim: {p[4]}")
    else:
        print("Nenhum preço encontrado.")

def alterar_preco(cursor, conexao):
    id_preco = int(input("Digite o ID do preço que deseja alterar: "))
    cursor.execute("SELECT * FROM tbl_precos WHERE id_preco=%s", (id_preco,))
    preco = cursor.fetchone()

    if not preco:
        print("⚠️ Preço não encontrado.")
        return

    print(f"Atual: ID={preco[0]}, Procedimento={preco[1]}, Valor={preco[2]}, Início={preco[3]}, Fim={preco[4]}")

    print("\nQual campo deseja alterar?")
    print("1 - Valor")
    print("2 - Data início")
    print("3 - Data fim")
    print("4 - Alterar todos")
    escolha = int(input("Escolha uma opção: "))

    if escolha == 1:
        novo_valor = float(input("Novo valor R$: "))
        sql = "UPDATE tbl_precos SET preco=%s WHERE id_preco=%s"
        valores = (novo_valor, id_preco)

    elif escolha == 2:
        nova_data = input("Nova data início (DD-MM-AAAA): ")
        nova_data_sql = datetime.strptime(nova_data, "%d-%m-%Y").strftime("%Y-%m-%d")
        sql = "UPDATE tbl_precos SET data_inicio=%s WHERE id_preco=%s"
        valores = (nova_data_sql, id_preco)

    elif escolha == 3:
        nova_data = input("Nova data fim (DD-MM-AAAA): ")
        nova_data_sql = datetime.strptime(nova_data, "%d-%m-%Y").strftime("%Y-%m-%d")
        sql = "UPDATE tbl_precos SET data_fim=%s WHERE id_preco=%s"
        valores = (nova_data_sql, id_preco)

    elif escolha == 4:
        novo_valor = float(input("Novo valor R$: "))
        nova_inicio = input("Nova data início (DD-MM-AAAA): ")
        nova_inicio_sql = datetime.strptime(nova_inicio, "%d-%m-%Y").strftime("%Y-%m-%d")
        nova_fim = input("Nova data fim (DD-MM-AAAA): ")
        nova_fim_sql = datetime.strptime(nova_fim, "%d-%m-%Y").strftime("%Y-%m-%d")
        sql = "UPDATE tbl_precos SET preco=%s, data_inicio=%s, data_fim=%s WHERE id_preco=%s"
        valores = (novo_valor, nova_inicio_sql, nova_fim_sql, id_preco)

    else:
        print("⚠️ Opção inválida!")
        return

    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Preço atualizado com sucesso!")

def excluir_preco(cursor, conexao):
    id_preco = int(input("Digite o ID do preço que deseja excluir: "))
    sql = "DELETE FROM tbl_precos WHERE id_preco=%s"
    cursor.execute(sql, (id_preco,))
    conexao.commit()
    print("🗑️ Preço excluído com sucesso!")

def cadastrar_faturamento(cursor, conexao):
    ano = int(input("Ano: "))
    mes = int(input("Mês: "))
    dia = int(input("Dia: "))
    valor_total = float(input("Valor total do faturamento R$: "))

    sql = "INSERT INTO tbl_faturamento (ano, mes, dia, valor_total) VALUES (%s,%s,%s,%s)"
    valores = (ano, mes, dia, valor_total)
    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Faturamento registrado com sucesso!")

def mostrar_faturamento(cursor):
    print("\n--- Mostrar Faturamento ---")
    print("1 - Listar todos")
    print("2 - Buscar por ID")
    print("3 - Buscar por Ano/Mês")

    opcao = int(input("Escolha: "))
    if opcao == 1:
        cursor.execute("SELECT * FROM tbl_faturamento")
    elif opcao == 2:
        id_fat = int(input("ID do faturamento: "))
        cursor.execute("SELECT * FROM tbl_faturamento WHERE id_faturamento=%s", (id_fat,))
    elif opcao == 3:
        ano = int(input("Ano: "))
        mes = int(input("Mês: "))
        cursor.execute("SELECT * FROM tbl_faturamento WHERE ano=%s AND mes=%s", (ano, mes))
    else:
        print("⚠️ Opção inválida!")
        return

    for f in cursor.fetchall():
        print(f"ID={f[0]} | {f[1]}/{f[2]}/{f[3]} | Valor R${f[4]}")

def alterar_faturamento(cursor, conexao):
    id_fat = int(input("Digite o ID do faturamento: "))
    cursor.execute("SELECT * FROM tbl_faturamento WHERE id_faturamento=%s", (id_fat,))
    fat = cursor.fetchone()
    if not fat:
        print("⚠️ Não encontrado.")
        return

    print(f"Atual: {fat}")
    print("1 - Alterar valor | 2 - Alterar data | 3 - Alterar tudo")
    op = int(input("Escolha: "))

    if op == 1:
        novo_valor = float(input("Novo valor R$: "))
        sql = "UPDATE tbl_faturamento SET valor_total=%s WHERE id_faturamento=%s"
        valores = (novo_valor, id_fat)
    elif op == 2:
        ano = int(input("Ano: "))
        mes = int(input("Mês: "))
        dia = int(input("Dia: "))
        sql = "UPDATE tbl_faturamento SET ano=%s, mes=%s, dia=%s WHERE id_faturamento=%s"
        valores = (ano, mes, dia, id_fat)
    elif op == 3:
        ano = int(input("Ano: "))
        mes = int(input("Mês: "))
        dia = int(input("Dia: "))
        novo_valor = float(input("Novo valor R$: "))
        sql = "UPDATE tbl_faturamento SET ano=%s, mes=%s, dia=%s, valor_total=%s WHERE id_faturamento=%s"
        valores = (ano, mes, dia, novo_valor, id_fat)
    else:
        return

    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Alterado com sucesso!")

def excluir_faturamento(cursor, conexao):
    id_fat = int(input("ID do faturamento a excluir: "))
    cursor.execute("DELETE FROM tbl_faturamento WHERE id_faturamento=%s", (id_fat,))
    conexao.commit()
    print("🗑️ Excluído com sucesso!")

def cadastrar_gasto(cursor, conexao):
    print("\n--- Cadastrar Gasto ---")
    categoria = input("Categoria (Aluguel, Produtos, Contas, Lazer, Investimento, Outros): ")
    descricao = input("Descrição do gasto: ")
    valor = float(input("Valor do gasto em R$: "))
    data = input("Data do gasto (DD-MM-AAAA): ")
    data_sql = datetime.strptime(data, "%d-%m-%Y").strftime("%Y-%m-%d")
    forma_pagamento = input("Forma de pagamento (Dinheiro, Cartão Débito, Cartão Crédito, Pix, Boleto): ")

    sql = "INSERT INTO tbl_gastos (categoria, descricao, valor, data_gasto, forma_pagamento) VALUES (%s,%s,%s,%s,%s)"
    valores = (categoria, descricao, valor, data_sql, forma_pagamento)
    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Gasto registrado com sucesso!")

def mostrar_gastos(cursor):
    print("\n--- Mostrar Gastos ---")
    print("1 - Listar todos")
    print("2 - Buscar por ID")
    print("3 - Buscar por Categoria")
    print("4 - Buscar por intervalo de Datas")

    opcao = int(input("Escolha: "))

    if opcao == 1:
        cursor.execute("SELECT * FROM tbl_gastos")
    elif opcao == 2:
        id_gasto = int(input("Digite o ID do gasto: "))
        cursor.execute("SELECT * FROM tbl_gastos WHERE id_gasto=%s", (id_gasto,))
    elif opcao == 3:
        categoria = input("Digite a categoria: ")
        cursor.execute("SELECT * FROM tbl_gastos WHERE categoria=%s", (categoria,))
    elif opcao == 4:
        data_inicio = input("Data inicial (DD-MM-AAAA): ")
        data_fim = input("Data final (DD-MM-AAAA): ")

        try:
            data_inicio_sql = datetime.strptime(data_inicio, "%d-%m-%Y").strftime("%Y-%m-%d")
            data_fim_sql = datetime.strptime(data_fim, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            print("⚠️ Datas inválidas! Use o formato DD-MM-AAAA.")
            return

        sql = "SELECT * FROM tbl_gastos WHERE data_gasto BETWEEN %s AND %s"
        cursor.execute(sql, (data_inicio_sql, data_fim_sql))
    else:
        print("⚠️ Opção inválida!")
        return

    gastos = cursor.fetchall()
    if gastos:
        print("\n--- Resultados ---")
        for g in gastos:
            print(f"ID={g[0]} | Categoria={g[1]} | Descrição={g[2]} | Valor=R${g[3]} | Data={g[4]} | Pagamento={g[5]}")
    else:
        print("Nenhum gasto encontrado.")

def alterar_gasto(cursor, conexao):
    id_gasto = int(input("Digite o ID do gasto que deseja alterar: "))
    cursor.execute("SELECT * FROM tbl_gastos WHERE id_gasto=%s", (id_gasto,))
    gasto = cursor.fetchone()

    if not gasto:
        print("⚠️ Gasto não encontrado.")
        return

    print(f"Atual: {gasto}")
    print("1 - Alterar categoria")
    print("2 - Alterar descrição")
    print("3 - Alterar valor")
    print("4 - Alterar data")
    print("5 - Alterar forma de pagamento")
    print("6 - Alterar tudo")
    escolha = int(input("Escolha: "))

    if escolha == 1:
        nova_categoria = input("Nova categoria: ")
        sql = "UPDATE tbl_gastos SET categoria=%s WHERE id_gasto=%s"
        valores = (nova_categoria, id_gasto)

    elif escolha == 2:
        nova_desc = input("Nova descrição: ")
        sql = "UPDATE tbl_gastos SET descricao=%s WHERE id_gasto=%s"
        valores = (nova_desc, id_gasto)

    elif escolha == 3:
        novo_valor = float(input("Novo valor R$: "))
        sql = "UPDATE tbl_gastos SET valor=%s WHERE id_gasto=%s"
        valores = (novo_valor, id_gasto)

    elif escolha == 4:
        nova_data = input("Nova data (DD-MM-AAAA): ")
        nova_data_sql = datetime.strptime(nova_data, "%d-%m-%Y").strftime("%Y-%m-%d")
        sql = "UPDATE tbl_gastos SET data_gasto=%s WHERE id_gasto=%s"
        valores = (nova_data_sql, id_gasto)

    elif escolha == 5:
        nova_forma = input("Nova forma de pagamento: ")
        sql = "UPDATE tbl_gastos SET forma_pagamento=%s WHERE id_gasto=%s"
        valores = (nova_forma, id_gasto)

    elif escolha == 6:
        nova_categoria = input("Nova categoria: ")
        nova_desc = input("Nova descrição: ")
        novo_valor = float(input("Novo valor R$: "))
        nova_data = input("Nova data (DD-MM-AAAA): ")
        nova_data_sql = datetime.strptime(nova_data, "%d-%m-%Y").strftime("%Y-%m-%d")
        nova_forma = input("Nova forma de pagamento: ")
        sql = "UPDATE tbl_gastos SET categoria=%s, descricao=%s, valor=%s, data_gasto=%s, forma_pagamento=%s WHERE id_gasto=%s"
        valores = (nova_categoria, nova_desc, novo_valor, nova_data_sql, nova_forma, id_gasto)

    else:
        print("⚠️ Opção inválida!")
        return

    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Gasto atualizado com sucesso!")

def excluir_gasto(cursor, conexao):
    id_gasto = int(input("Digite o ID do gasto que deseja excluir: "))
    sql = "DELETE FROM tbl_gastos WHERE id_gasto=%s"
    cursor.execute(sql, (id_gasto,))
    conexao.commit()
    print("🗑️ Gasto excluído com sucesso!")

def cadastrar_lucro(cursor, conexao):
    print("\n--- Cadastrar Lucro Mensal ---")
    ano = int(input("Ano: "))
    mes = int(input("Mês: "))
    faturamento = float(input("Faturamento R$: "))
    despesas = float(input("Despesas R$: "))
    lucro = faturamento - despesas  # cálculo automático

    data_registro = input("Data de registro (DD-MM-AAAA): ")
    data_sql = datetime.strptime(data_registro, "%d-%m-%Y").strftime("%Y-%m-%d")

    sql = "INSERT INTO tbl_lucro_mensal (ano, mes, faturamento, despesas, lucro_liquido, data_registro) VALUES (%s,%s,%s,%s,%s,%s)"
    valores = (ano, mes, faturamento, despesas, lucro, data_sql)
    cursor.execute(sql, valores)
    conexao.commit()
    print(f"✅ Lucro mensal registrado com sucesso! Lucro líquido: R${lucro:.2f}")

def mostrar_lucro(cursor):
    print("\n--- Mostrar Lucro Mensal ---")
    print("1 - Listar todos")
    print("2 - Buscar por ID")
    print("3 - Buscar por Ano/Mês")
    print("4 - Buscar por intervalo de Datas")

    opcao = int(input("Escolha: "))

    if opcao == 1:
        cursor.execute("SELECT * FROM tbl_lucro_mensal")
    elif opcao == 2:
        id_lucro = int(input("Digite o ID: "))
        cursor.execute("SELECT * FROM tbl_lucro_mensal WHERE id_lucro=%s", (id_lucro,))
    elif opcao == 3:
        ano = int(input("Ano: "))
        mes = int(input("Mês: "))
        cursor.execute("SELECT * FROM tbl_lucro_mensal WHERE ano=%s AND mes=%s", (ano, mes))
    elif opcao == 4:
        data_inicio = input("Data inicial (DD-MM-AAAA): ")
        data_fim = input("Data final (DD-MM-AAAA): ")
        try:
            data_inicio_sql = datetime.strptime(data_inicio, "%d-%m-%Y").strftime("%Y-%m-%d")
            data_fim_sql = datetime.strptime(data_fim, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            print("⚠️ Datas inválidas!")
            return
        cursor.execute("SELECT * FROM tbl_lucro_mensal WHERE data_registro BETWEEN %s AND %s", (data_inicio_sql, data_fim_sql))
    else:
        print("⚠️ Opção inválida!")
        return

    lucros = cursor.fetchall()
    if lucros:
        for l in lucros:
            print(f"ID={l[0]} | Ano={l[1]} | Mês={l[2]} | Faturamento=R${l[3]} | Despesas=R${l[4]} | Lucro=R${l[5]} | Registro={l[6]}")
    else:
        print("Nenhum registro encontrado.")

def alterar_lucro(cursor, conexao):
    id_lucro = int(input("Digite o ID do lucro que deseja alterar: "))
    cursor.execute("SELECT * FROM tbl_lucro_mensal WHERE id_lucro=%s", (id_lucro,))
    lucro = cursor.fetchone()

    if not lucro:
        print("⚠️ Registro não encontrado.")
        return

    print(f"Atual: {lucro}")
    print("1 - Alterar faturamento")
    print("2 - Alterar despesas")
    print("3 - Alterar ano/mês")
    print("4 - Alterar tudo")
    escolha = int(input("Escolha: "))

    if escolha == 1:
        novo_fat = float(input("Novo faturamento R$: "))
        despesas = lucro[4]
        novo_lucro = novo_fat - despesas
        sql = "UPDATE tbl_lucro_mensal SET faturamento=%s, lucro_liquido=%s WHERE id_lucro=%s"
        valores = (novo_fat, novo_lucro, id_lucro)

    elif escolha == 2:
        novas_desp = float(input("Novas despesas R$: "))
        faturamento = lucro[3]
        novo_lucro = faturamento - novas_desp
        sql = "UPDATE tbl_lucro_mensal SET despesas=%s, lucro_liquido=%s WHERE id_lucro=%s"
        valores = (novas_desp, novo_lucro, id_lucro)

    elif escolha == 3:
        ano = int(input("Novo ano: "))
        mes = int(input("Novo mês: "))
        sql = "UPDATE tbl_lucro_mensal SET ano=%s, mes=%s WHERE id_lucro=%s"
        valores = (ano, mes, id_lucro)

    elif escolha == 4:
        ano = int(input("Ano: "))
        mes = int(input("Mês: "))
        novo_fat = float(input("Novo faturamento R$: "))
        novas_desp = float(input("Novas despesas R$: "))
        novo_lucro = novo_fat - novas_desp
        data_registro = input("Nova data de registro (DD-MM-AAAA): ")
        data_sql = datetime.strptime(data_registro, "%d-%m-%Y").strftime("%Y-%m-%d")
        sql = "UPDATE tbl_lucro_mensal SET ano=%s, mes=%s, faturamento=%s, despesas=%s, lucro_liquido=%s, data_registro=%s WHERE id_lucro=%s"
        valores = (ano, mes, novo_fat, novas_desp, novo_lucro, data_sql, id_lucro)

    else:
        print("⚠️ Opção inválida!")
        return

    cursor.execute(sql, valores)
    conexao.commit()
    print("✅ Lucro atualizado com sucesso!")

def excluir_lucro(cursor, conexao):
    id_lucro = int(input("Digite o ID do lucro que deseja excluir: "))
    sql = "DELETE FROM tbl_lucro_mensal WHERE id_lucro=%s"
    cursor.execute(sql, (id_lucro,))
    conexao.commit()
    print("🗑️ Registro excluído com sucesso!")

while True:
    print("\n--- MENU PRINCIPAL ---")
    print("1 - Clientes")
    print("2 - Atendimento ")
    print("3 - Preco ")
    print("4 - Finanças ")
    print("0 - Sair")

    op_geral = int(input("Escolha uma opção: "))

    if op_geral == 0:
        print("Saindo do sistema...")
        break

    elif op_geral == 1: #clientes
        while True:
            print("\n--- MENU CLIENTES ---")
            print("1 - Cadastrar cliente")
            print("2 - Mostrar clientes")
            print("3 - Alterar cliente")
            print("4 - Excluir cliente")
            print("0 - Voltar")

            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                cadastrar_cliente(cursor, conexao)
            elif opcao == 2:
                mostrar_clientes(cursor)
            elif opcao == 3:
                alterar_cliente(cursor, conexao)
            elif opcao == 4:
                excluir_cliente(cursor, conexao)
            elif opcao == 0:
                break
            else:
                print("⚠️ Opção inválida!")

    elif op_geral == 2:  # Produtos/Procedimentos
        while True:
            print("\n--- MENU PROCEDIMENTOS/PRODUTOS ---")
            print("1 - Cadastrar")
            print("2 - Mostrar")
            print("3 - Alterar")
            print("4 - Excluir")
            print("0 - Voltar")

            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                cadastrar_procedimento(cursor, conexao)
            elif opcao == 2:
                mostrar_procedimentos(cursor)
            elif opcao == 3:
                alterar_procedimento(cursor, conexao)
            elif opcao == 4:
                excluir_procedimento(cursor, conexao)
            elif opcao == 0:
                break
            else:
                print("⚠️ Opção inválida!")

    elif op_geral == 3:  # Preços
        while True:
            print("\n--- MENU PREÇOS ---")
            print("1 - Cadastrar preço")
            print("2 - Mostrar preços")
            print("3 - Alterar preço")
            print("4 - Excluir preço")
            print("0 - Voltar")

            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                cadastrar_preco(cursor, conexao)
            elif opcao == 2:
                mostrar_precos(cursor)
            elif opcao == 3:
                alterar_preco(cursor, conexao)
            elif opcao == 4:
                excluir_preco(cursor, conexao)
            elif opcao == 0:
                break
            else:
                print("⚠️ Opção inválida!")

    elif op_geral == 4:  # Finanças
        while True:
            print("\n--- MENU FINANÇAS ---")
            print("1 - Faturamento")
            print("2 - Gastos")
            print("3 - Lucro Mensal")
            print("0 - Voltar")

            op_finan = int(input("Escolha: "))

            if op_finan == 1: # Submenu Faturamento
                while True:
                    print("\n--- Faturamento ---")
                    print("1 - Cadastrar")
                    print("2 - Mostrar")
                    print("3 - Alterar")
                    print("4 - Excluir")
                    print("0 - Voltar")
                    op = int(input("Escolha: "))
                    if op == 1: cadastrar_faturamento(cursor, conexao)
                    elif op == 2: mostrar_faturamento(cursor)
                    elif op == 3: alterar_faturamento(cursor, conexao)
                    elif op == 4: excluir_faturamento(cursor, conexao)
                    elif op == 0: break

            elif op_finan == 2:  # Submenu Gastos
                while True:
                    print("\n--- MENU GASTOS ---")
                    print("1 - Cadastrar gasto")
                    print("2 - Mostrar gastos")
                    print("3 - Alterar gasto")
                    print("4 - Excluir gasto")
                    print("0 - Voltar")

                    opcao = int(input("Escolha: "))

                    if opcao == 1:
                        cadastrar_gasto(cursor, conexao)
                    elif opcao == 2:
                        mostrar_gastos(cursor)
                    elif opcao == 3:
                        alterar_gasto(cursor, conexao)
                    elif opcao == 4:
                        excluir_gasto(cursor, conexao)
                    elif opcao == 0:
                        break
                    else:
                        print("⚠️ Opção inválida!")

            elif op_finan == 3:  # Lucro Mensal
                while True:
                    print("\n--- MENU LUCRO MENSAL ---")
                    print("1 - Cadastrar")
                    print("2 - Mostrar")
                    print("3 - Alterar")
                    print("4 - Excluir")
                    print("0 - Voltar")

                    opcao = int(input("Escolha: "))

                    if opcao == 1:
                        cadastrar_lucro(cursor, conexao)
                    elif opcao == 2:
                        mostrar_lucro(cursor)
                    elif opcao == 3:
                        alterar_lucro(cursor, conexao)
                    elif opcao == 4:
                        excluir_lucro(cursor, conexao)
                    elif opcao == 0:
                        break
                    else:
                        print("⚠️ Opção inválida!")