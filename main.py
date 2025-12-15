from services import SistemaBiblioteca
from ui import executar_interface


def main():
    sistema = SistemaBiblioteca()

    # Carrega livros do CSV
    try:
        sistema.carregar_livros_de_csv()
        print("Livros iniciais carregados a partir de 'livros.csv'.")
    except FileNotFoundError:
        print("Arquivo 'livros.csv' não encontrado. O sistema iniciará sem livros pré-cadastrados.")

    # Carrega usuários do CSV
    try:
        sistema.carregar_usuarios_de_csv()
        print("Usuários iniciais carregados a partir de 'usuarios.csv'.")
    except FileNotFoundError:
        print("Arquivo 'usuarios.csv' não encontrado. O sistema iniciará sem usuários pré-cadastrados.")

    executar_interface(sistema)


if __name__ == "__main__":
    main()
