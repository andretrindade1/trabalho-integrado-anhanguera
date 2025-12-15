# 📚 Sistema de Gerenciamento de Biblioteca (CLI em Python)

Sistema de gerenciamento de biblioteca desenvolvido em **Python**, utilizando **Programação Orientada a Objetos (POO)**, **persistência em arquivos CSV** e **interface em linha de comando (CLI)**.  
O projeto simula o funcionamento de uma biblioteca real, permitindo cadastro, consulta, empréstimo, devolução e geração de relatórios gerenciais.

Projeto desenvolvido como **Trabalho Integrado do curso de Ciência de Dados (Anhanguera Educacional)**, com foco em arquitetura, organização de código e regras de negócio.

---

## 🎯 Objetivos do Projeto

- Aplicar conceitos de **POO e arquitetura de software**
- Separar claramente **domínio, serviços e interface**
- Simular persistência de dados sem banco de dados (CSV)
- Implementar regras de negócio com validações e exceções
- Desenvolver uma aplicação funcional e extensível em Python puro

---

## 🧱 Arquitetura do Projeto

```text
.
├── main.py           # Ponto de entrada da aplicação
├── models.py         # Modelos de domínio (Livro, Usuário, Empréstimo + exceções)
├── services.py       # Camada de serviços e regras de negócio
├── ui.py             # Interface CLI (menus, fluxos e painéis)
├── livros.csv        # Base de dados simulada de livros
├── usuarios.csv      # Base de dados simulada de usuários
└── README.md         # Documentação do projeto
```

---

## ⚙️ Funcionalidades

### 📖 Livros
- Cadastro de livros (título, autor, categoria, ano, cópias)
- Controle automático de cópias disponíveis
- Persistência em CSV

### 👤 Usuários
- Cadastro de usuários
- Persistência em CSV

### 🔄 Empréstimos
- Empréstimo e devolução de livros
- Controle de disponibilidade
- Histórico de empréstimos ativos

### 📊 Relatórios
- Livros disponíveis
- Livros emprestados
- Usuários cadastrados
- Painéis gerenciais

---

## ▶️ Como Executar

### Pré-requisitos
- Python 3.10+

### Execução
```bash
python main.py
```

---

## 🛠️ Tecnologias Utilizadas

- Python 3
- Programação Orientada a Objetos
- dataclasses
- CSV como persistência
- Interface CLI

---

## 👤 Autor

**André Santos da Trindade**  
Estudante de Ciência de Dados  

---

## 📜 Licença

Projeto de uso acadêmico e educacional.
