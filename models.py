from dataclasses import dataclass, field


# ================== EXCEÇÕES PERSONALIZADAS ==================


class LivroIndisponivelError(Exception):
    """Erro levantado quando não há cópias disponíveis para empréstimo."""
    pass


class LivroNaoEncontradoError(Exception):
    """Erro levantado quando o livro não é encontrado."""
    pass


class UsuarioNaoEncontradoError(Exception):
    """Erro levantado quando o usuário não é encontrado."""
    pass


# ================== CLASSES DE DOMÍNIO (POO) ==================


@dataclass
class Livro:
    """
    Representa um livro da biblioteca.
    """
    id_livro: int
    titulo: str
    autor: str
    categoria: str  # <-- NOVO CAMPO
    ano: int
    total_copias: int
    copias_disponiveis: int = field(init=False)

    def __post_init__(self):
        # Ao criar o livro, todas as cópias estão disponíveis
        self.copias_disponiveis = self.total_copias

    def emprestar(self):
        """
        Tenta emprestar uma cópia do livro.
        """
        if self.copias_disponiveis <= 0:
            raise LivroIndisponivelError(
                f"Livro '{self.titulo}' está indisponível para empréstimo."
            )
        self.copias_disponiveis -= 1

    def devolver(self):
        """
        Devolve uma cópia do livro, incrementando o estoque disponível.
        """
        if self.copias_disponiveis < self.total_copias:
            self.copias_disponiveis += 1


@dataclass
class Usuario:
    """
    Representa um usuário da biblioteca.
    """
    id_usuario: int
    nome: str
    contato: str


@dataclass
class Emprestimo:
    """
    Representa um empréstimo de um livro para um usuário.
    """
    id_emprestimo: int
    id_usuario: int
    id_livro: int
    ativo: bool = True
