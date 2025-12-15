from typing import Dict, List, Optional
import itertools
import csv

from models import (
    Livro,
    Usuario,
    Emprestimo,
    LivroIndisponivelError,
    LivroNaoEncontradoError,
    UsuarioNaoEncontradoError,
)


class SistemaBiblioteca:
    """
    Classe principal que gerencia os cadastros, empréstimos, devoluções,
    relatórios e integração com arquivos CSV (simulando um banco de dados).
    """

    def __init__(
        self,
        caminho_csv_livros: str = "livros.csv",
        caminho_csv_usuarios: str = "usuarios.csv",
    ):
        self.livros: Dict[int, Livro] = {}
        self.usuarios: Dict[int, Usuario] = {}
        self.emprestimos: Dict[int, Emprestimo] = {}

        self._gerador_ids_livro = itertools.count(1)
        self._gerador_ids_usuario = itertools.count(1)
        self._gerador_ids_emprestimo = itertools.count(1)

        # caminhos dos arquivos CSV
        self.caminho_csv_livros = caminho_csv_livros
        self.caminho_csv_usuarios = caminho_csv_usuarios

    # ================== LIVROS (CADASTRO + CSV) ==================

    def cadastrar_livro(
        self,
        titulo: str,
        autor: str,
        ano: int,
        total_copias: int,
        categoria: str,
        salvar: bool = True,
    ) -> Livro:
        """
        Cadastra um novo livro em memória e, opcionalmente, salva no CSV.
        """
        novo_id = next(self._gerador_ids_livro)
        livro = Livro(
            id_livro=novo_id,
            titulo=titulo,
            autor=autor,
            categoria=categoria,
            ano=ano,
            total_copias=total_copias,
        )
        self.livros[novo_id] = livro

        if salvar:
            self.salvar_livros_csv()

        return livro

    def carregar_livros_de_csv(self):
        """
        Carrega livros a partir do CSV.

        Cabeçalho esperado:
        id_livro,titulo,autor,categoria,ano,total_copias,copias_disponiveis

        Se 'id_livro' ou 'copias_disponiveis' não existirem, o código tenta
        se adaptar e assumir valores padrão.
        """
        try:
            with open(self.caminho_csv_livros, mode="r", encoding="utf-8") as f:
                leitor = csv.DictReader(f)

                max_id = 0
                for linha in leitor:
                    try:
                        id_livro_str = linha.get("id_livro")
                        if id_livro_str:
                            id_livro = int(id_livro_str)
                        else:
                            id_livro = next(self._gerador_ids_livro)

                        titulo = linha["titulo"].strip()
                        autor = linha["autor"].strip()
                        categoria = linha.get("categoria", "").strip()
                        ano = int(linha["ano"])
                        total_copias = int(linha["total_copias"])

                        livro = Livro(
                            id_livro=id_livro,
                            titulo=titulo,
                            autor=autor,
                            categoria=categoria,
                            ano=ano,
                            total_copias=total_copias,
                        )

                        # Se o CSV já tiver copias_disponiveis, respeitamos.
                        copias_disp_str = linha.get("copias_disponiveis")
                        if copias_disp_str:
                            try:
                                livro.copias_disponiveis = int(copias_disp_str)
                            except ValueError:
                                # Mantém o padrão (todas disponíveis)
                                pass

                        self.livros[id_livro] = livro
                        if id_livro > max_id:
                            max_id = id_livro
                    except KeyError as e:
                        print(f"[AVISO] Coluna ausente no CSV de livros: {e}. Linha ignorada: {linha}")
                    except ValueError:
                        print(f"[AVISO] Erro de conversão em linha de livros. Linha ignorada: {linha}")

                # Ajusta o gerador de IDs para continuar após o maior ID encontrado
                if max_id > 0:
                    self._gerador_ids_livro = itertools.count(max_id + 1)

        except FileNotFoundError:
            # Silencioso aqui; o main trata a mensagem amigável
            raise

    def salvar_livros_csv(self):
        """
        Salva o estado atual dos livros no CSV, incluindo copias_disponiveis.
        """
        fieldnames = [
            "id_livro",
            "titulo",
            "autor",
            "categoria",
            "ano",
            "total_copias",
            "copias_disponiveis",
        ]
        with open(self.caminho_csv_livros, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for livro in self.livros.values():
                writer.writerow(
                    {
                        "id_livro": livro.id_livro,
                        "titulo": livro.titulo,
                        "autor": livro.autor,
                        "categoria": livro.categoria,
                        "ano": livro.ano,
                        "total_copias": livro.total_copias,
                        "copias_disponiveis": livro.copias_disponiveis,
                    }
                )

    # ================== USUÁRIOS (CADASTRO + CSV) ==================

    def cadastrar_usuario(self, nome: str, contato: str, salvar: bool = True) -> Usuario:
        novo_id = next(self._gerador_ids_usuario)
        usuario = Usuario(
            id_usuario=novo_id,
            nome=nome,
            contato=contato,
        )
        self.usuarios[novo_id] = usuario

        if salvar:
            self.salvar_usuarios_csv()

        return usuario

    def carregar_usuarios_de_csv(self):
        """
        Carrega usuários a partir de um CSV.

        Cabeçalho esperado:
        id_usuario,nome,contato
        """
        try:
            with open(self.caminho_csv_usuarios, mode="r", encoding="utf-8") as f:
                leitor = csv.DictReader(f)

                max_id = 0
                for linha in leitor:
                    try:
                        id_usuario_str = linha.get("id_usuario")
                        if id_usuario_str:
                            id_usuario = int(id_usuario_str)
                        else:
                            id_usuario = next(self._gerador_ids_usuario)

                        nome = linha["nome"].strip()
                        contato = linha.get("contato", "").strip()

                        usuario = Usuario(
                            id_usuario=id_usuario,
                            nome=nome,
                            contato=contato,
                        )
                        self.usuarios[id_usuario] = usuario
                        if id_usuario > max_id:
                            max_id = id_usuario
                    except KeyError as e:
                        print(f"[AVISO] Coluna ausente no CSV de usuários: {e}. Linha ignorada: {linha}")
                    except ValueError:
                        print(f"[AVISO] Erro de conversão em linha de usuários. Linha ignorada: {linha}")

                if max_id > 0:
                    self._gerador_ids_usuario = itertools.count(max_id + 1)

        except FileNotFoundError:
            raise

    def salvar_usuarios_csv(self):
        """
        Salva o estado atual dos usuários no CSV.
        """
        fieldnames = ["id_usuario", "nome", "contato"]
        with open(self.caminho_csv_usuarios, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for usuario in self.usuarios.values():
                writer.writerow(
                    {
                        "id_usuario": usuario.id_usuario,
                        "nome": usuario.nome,
                        "contato": usuario.contato,
                    }
                )

    # ================== EMPRÉSTIMO E DEVOLUÇÃO ==================

    def emprestar_livro(self, id_usuario: int, id_livro: int) -> Emprestimo:
        usuario = self.usuarios.get(id_usuario)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {id_usuario} não encontrado.")

        livro = self.livros.get(id_livro)
        if not livro:
            raise LivroNaoEncontradoError(f"Livro com ID {id_livro} não encontrado.")

        livro.emprestar()

        id_emprestimo = next(self._gerador_ids_emprestimo)
        emprestimo = Emprestimo(
            id_emprestimo=id_emprestimo,
            id_usuario=id_usuario,
            id_livro=id_livro,
            ativo=True,
        )
        self.emprestimos[id_emprestimo] = emprestimo

        # Atualiza CSV de livros com copias_disponiveis alteradas
        self.salvar_livros_csv()

        return emprestimo

    def devolver_livro(self, id_emprestimo: int):
        emprestimo = self.emprestimos.get(id_emprestimo)

        if not emprestimo:
            raise ValueError(f"Empréstimo com ID {id_emprestimo} não encontrado.")

        if not emprestimo.ativo:
            raise ValueError(f"Empréstimo {id_emprestimo} já foi encerrado.")

        livro = self.livros.get(emprestimo.id_livro)
        if not livro:
            raise LivroNaoEncontradoError(f"Livro com ID {emprestimo.id_livro} não encontrado.")

        livro.devolver()
        emprestimo.ativo = False

        # Atualiza CSV de livros com copias_disponiveis alteradas
        self.salvar_livros_csv()

    # ================== CONSULTA E RELATÓRIOS ==================

    def buscar_livros(
        self,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        ano: Optional[int] = None,
        categoria: Optional[str] = None,
    ) -> List[Livro]:
        resultados = []
        for livro in self.livros.values():
            if titulo and titulo.lower() not in livro.titulo.lower():
                continue
            if autor and autor.lower() not in livro.autor.lower():
                continue
            if ano and ano != livro.ano:
                continue
            if categoria and categoria.lower() not in livro.categoria.lower():
                continue
            resultados.append(livro)
        return resultados

    def relatorio_livros_disponiveis(self) -> List[Livro]:
        return [livro for livro in self.livros.values() if livro.copias_disponiveis > 0]

    def relatorio_livros_emprestados(self) -> List[Emprestimo]:
        return [emp for emp in self.emprestimos.values() if emp.ativo]

    def relatorio_usuarios(self) -> List[Usuario]:
        return list(self.usuarios.values())
