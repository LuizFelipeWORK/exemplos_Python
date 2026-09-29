class Livro:
    def __init__(self, titulo: str,
                 ano: int) -> None:
        self.titulo = titulo
        self.ano = ano
        self.disponivel = True
 
    def __str__(self) -> str:
        status = "disponível" if self.disponivel else "emprestado"
        return f"{self.titulo} ({self.ano}) - {status}"
 
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Livro):
            return NotImplemented
        return (self.titulo == outro.titulo
                and self.ano == outro.ano)


if __name__ == "__main__":
    livro1 = Livro("Livro 1", 2026)
    livro2 = Livro("Livro 2", 2026)
    livro3 = Livro("Livro 1", 2026)

    print(livro1)
    print(livro2)
    print(livro3)

    print(f"Livro1 == Livro2: ", livro1==livro2)
    print(f"Livro1 == Livro3: ", livro1==livro3)
