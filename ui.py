from typing import Optional
from collections import defaultdict

from services import SistemaBiblioteca
from models import (
    LivroIndisponivelError,
    LivroNaoEncontradoError,
    UsuarioNaoEncontradoError,
)


def exibir_menu():
    print("\n====== SISTEMA DE BIBLIOTECA ======")
    print("1. Cadastrar livro")
    print("2. Cadastrar usuário")
    print("3. Realizar empréstimo")
    print("4. Registrar devolução")
    print("5. Consultar livros (disponíveis por categoria)")
    print("6. Relatórios")
    print("7. Painel de gerenciamento de livros")
    print("8. Painel de gerenciamento de usuários")  # NOVO
    print("0. Sair")


def exibir_menu_relatorios():
    print("\n====== RELATÓRIOS ======")
    print("1. Lista de livros disponíveis")
    print("2. Livros emprestados")
    print("3. Usuários cadastrados")
    print("0. Voltar")


def input_inteiro(msg: str) -> int:
    while True:
        try:
            valor = int(input(msg))
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


# ================== FLUXOS ==================


def cadastrar_livro_ui(sistema: SistemaBiblioteca):
    print("\n--- Cadastro de Livro ---")
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    categoria = input("Categoria (ex.: Romance, Fantasia, Técnico): ").strip()
    ano = input_inteiro("Ano de publicação: ")
    total_copias = input_inteiro("Número de cópias: ")

    livro = sistema.cadastrar_livro(titulo, autor, ano, total_copias, categoria)
    print(f"\nLivro cadastrado com sucesso! ID: {livro.id_livro}")


def cadastrar_usuario_ui(sistema: SistemaBiblioteca):
    print("\n--- Cadastro de Usuário ---")
    nome = input("Nome: ").strip()
    contato = input("Contato (telefone/e-mail): ").strip()

    usuario = sistema.cadastrar_usuario(nome, contato)
    print(f"\nUsuário cadastrado com sucesso! ID: {usuario.id_usuario}")


def emprestar_livro_ui(sistema: SistemaBiblioteca):
    print("\n--- Empréstimo de Livro ---")
    id_usuario = input_inteiro("ID do usuário: ")
    id_livro = input_inteiro("ID do livro: ")

    try:
        emprestimo = sistema.emprestar_livro(id_usuario, id_livro)
        print(f"\nEmpréstimo realizado com sucesso! ID do empréstimo: {emprestimo.id_emprestimo}")
    except (UsuarioNaoEncontradoError, LivroNaoEncontradoError, LivroIndisponivelError) as e:
        print(f"Erro ao realizar empréstimo: {e}")


def devolver_livro_ui(sistema: SistemaBiblioteca):
    print("\n--- Devolução de Livro ---")
    id_emprestimo = input_inteiro("ID do empréstimo: ")

    try:
        sistema.devolver_livro(id_emprestimo)
        print("\nDevolução registrada com sucesso!")
    except (ValueError, LivroNaoEncontradoError) as e:
        print(f"Erro ao registrar devolução: {e}")


def consultar_livros_ui(sistema: SistemaBiblioteca):
    """
    Lista TODOS os livros, separados por:
    - Disponíveis por categoria
    - Indisponíveis por categoria

    Ao final, pergunta se o usuário deseja realizar um empréstimo e,
    em caso afirmativo, chama a função de empréstimo.
    """
    print("\n--- Consulta de Livros (Todos por Disponibilidade e Categoria) ---")

    if not sistema.livros:
        print("Nenhum livro cadastrado no sistema.")
        return

    from collections import defaultdict

    disponiveis_por_cat = defaultdict(list)
    indisponiveis_por_cat = defaultdict(list)

    # Separa os livros em disponíveis e indisponíveis, agrupando por categoria
    for livro in sistema.livros.values():
        categoria = livro.categoria if livro.categoria else "Sem categoria"
        if livro.copias_disponiveis > 0:
            disponiveis_por_cat[categoria].append(livro)
        else:
            indisponiveis_por_cat[categoria].append(livro)

    # --- Livros disponíveis por categoria ---
    print("\n=== LIVROS DISPONÍVEIS POR CATEGORIA ===")
    if not disponiveis_por_cat:
        print("Nenhum livro disponível no momento.")
    else:
        total_disp = sum(len(lst) for lst in disponiveis_por_cat.values())
        print(f"Total de livros com pelo menos uma cópia disponível: {total_disp}\n")

        for categoria, livros_cat in disponiveis_por_cat.items():
            print(f"> Categoria: {categoria}")
            for livro in livros_cat:
                print(
                    f"  ID: {livro.id_livro} | "
                    f"Título: {livro.titulo} | "
                    f"Autor: {livro.autor} | "
                    f"Ano: {livro.ano} | "
                    f"Cópias: {livro.copias_disponiveis}/{livro.total_copias}"
                )
            print()

    # --- Livros indisponíveis por categoria ---
    print("\n=== LIVROS INDISPONÍVEIS POR CATEGORIA (SEM CÓPIAS LIVRES) ===")
    if not indisponiveis_por_cat:
        print("No momento, não há livros totalmente emprestados.")
    else:
        total_indisp = sum(len(lst) for lst in indisponiveis_por_cat.values())
        print(f"Total de livros sem cópias disponíveis: {total_indisp}\n")

        for categoria, livros_cat in indisponiveis_por_cat.items():
            print(f"> Categoria: {categoria}")
            for livro in livros_cat:
                print(
                    f"  ID: {livro.id_livro} | "
                    f"Título: {livro.titulo} | "
                    f"Autor: {livro.autor} | "
                    f"Ano: {livro.ano} | "
                    f"Cópias: {livro.copias_disponiveis}/{livro.total_copias}"
                )
            print()

    # --- Oferta de empréstimo ao final ---
    print("\nDeseja realizar o empréstimo de algum livro listado?")
    opc = input("Digite 's' para sim ou qualquer outra tecla para voltar ao menu: ").strip().lower()

    if opc == "s":
        # Reaproveita o fluxo já existente de empréstimo
        emprestar_livro_ui(sistema)
    else:
        print("Retornando ao menu principal...")


def relatorios_ui(sistema: SistemaBiblioteca):
    while True:
        exibir_menu_relatorios()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            livros = sistema.relatorio_livros_disponiveis()
            if not livros:
                print("\nNenhum livro disponível no momento.")
            else:
                print("\n--- Livros Disponíveis ---")
                for livro in livros:
                    print(
                        f"ID: {livro.id_livro} | "
                        f"Título: {livro.titulo} | "
                        f"Autor: {livro.autor} | "
                        f"Categoria: {livro.categoria} | "
                        f"Ano: {livro.ano} | "
                        f"Cópias disponíveis: {livro.copias_disponiveis}/{livro.total_copias}"
                    )

        elif opcao == "2":
            emprestimos = sistema.relatorio_livros_emprestados()
            if not emprestimos:
                print("\nNão há livros emprestados no momento.")
            else:
                print("\n--- Livros Emprestados ---")
                for emp in emprestimos:
                    livro = sistema.livros.get(emp.id_livro)
                    usuario = sistema.usuarios.get(emp.id_usuario)
                    print(
                        f"ID Empréstimo: {emp.id_emprestimo} | "
                        f"Livro: {livro.titulo if livro else 'N/A'} (ID {emp.id_livro}) | "
                        f"Usuário: {usuario.nome if usuario else 'N/A'} (ID {emp.id_usuario})"
                    )

        elif opcao == "3":
            usuarios = sistema.relatorio_usuarios()
            if not usuarios:
                print("\nNenhum usuário cadastrado.")
            else:
                print("\n--- Usuários Cadastrados ---")
                for usuario in usuarios:
                    print(
                        f"ID: {usuario.id_usuario} | "
                        f"Nome: {usuario.nome} | "
                        f"Contato: {usuario.contato}"
                    )
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")


def painel_livros_ui(sistema: SistemaBiblioteca):
    print("\n====== PAINEL DE GERENCIAMENTO DE LIVROS ======")

    if not sistema.livros:
        print("Nenhum livro cadastrado no sistema.")
        return

    for livro in sistema.livros.values():
        emprestimos_ativos = [
            emp for emp in sistema.emprestimos.values()
            if emp.ativo and emp.id_livro == livro.id_livro
        ]

        usuarios_com_livro = []
        for emp in emprestimos_ativos:
            usuario = sistema.usuarios.get(emp.id_usuario)
            if usuario:
                usuarios_com_livro.append(usuario.nome)

        if livro.copias_disponiveis == livro.total_copias:
            status = "Totalmente disponível"
        elif livro.copias_disponiveis == 0:
            status = "Todas as cópias emprestadas"
        else:
            status = "Parcialmente emprestado"

        print("\n-------------------------------------")
        print(f"ID: {livro.id_livro}")
        print(f"Título: {livro.titulo}")
        print(f"Autor: {livro.autor}")
        print(f"Categoria: {livro.categoria}")
        print(f"Ano: {livro.ano}")
        print(f"Cópias: {livro.copias_disponiveis}/{livro.total_copias}")
        print(f"Status: {status}")

        if usuarios_com_livro:
            print("Emprestado para:")
            for nome in usuarios_com_livro:
                print(f"  - {nome}")
        else:
            print("Emprestado para: ninguém no momento.")


def painel_usuarios_ui(sistema: SistemaBiblioteca):
    """
    Painel de gerenciamento de usuários:
    - Lista todos os usuários
    - Mostra quantos livros cada um tem emprestado
    - Lista os títulos emprestados para cada usuário
    """
    print("\n====== PAINEL DE GERENCIAMENTO DE USUÁRIOS ======")

    if not sistema.usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in sistema.usuarios.values():
        emprestimos_ativos = [
            emp for emp in sistema.emprestimos.values()
            if emp.ativo and emp.id_usuario == usuario.id_usuario
        ]

        livros_usuario = []
        for emp in emprestimos_ativos:
            livro = sistema.livros.get(emp.id_livro)
            if livro:
                livros_usuario.append(livro.titulo)

        print("\n-------------------------------------")
        print(f"ID Usuário: {usuario.id_usuario}")
        print(f"Nome: {usuario.nome}")
        print(f"Contato: {usuario.contato}")
        print(f"Quantidade de livros emprestados: {len(emprestimos_ativos)}")

        if livros_usuario:
            print("Livros emprestados:")
            for titulo in livros_usuario:
                print(f"  - {titulo}")
        else:
            print("Nenhum livro emprestado no momento.")


def executar_interface(sistema: SistemaBiblioteca):
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_livro_ui(sistema)
        elif opcao == "2":
            cadastrar_usuario_ui(sistema)
        elif opcao == "3":
            emprestar_livro_ui(sistema)
        elif opcao == "4":
            devolver_livro_ui(sistema)
        elif opcao == "5":
            consultar_livros_ui(sistema)
        elif opcao == "6":
            relatorios_ui(sistema)
        elif opcao == "7":
            painel_livros_ui(sistema)
        elif opcao == "8":
            painel_usuarios_ui(sistema)
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
