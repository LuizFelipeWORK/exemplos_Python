from livro import Livro


class ErroDeBiblioteca(Exception): pass
class LivroIndisponivelError(ErroDeBiblioteca): pass
class LivroNaoEncontradoError(ErroDeBiblioteca): pass


class Biblioteca:
    def __init__(self) -> None:
        self._acervo: list[Livro] = []
 
    def cadastrar(self, livro: Livro) -> None:
        self._acervo.append(livro)
 
    def _buscar(self, titulo: str) -> Livro:
        for livro in self._acervo:
            if livro.titulo == titulo:
                return livro
        raise LivroNaoEncontradoError(titulo)
    
    def emprestar(self, titulo: str) -> None:
        livro = self._buscar(titulo)
        if not livro.disponivel:
            raise LivroIndisponivelError(titulo)
        livro.disponivel = False
 
    def devolver(self, titulo: str) -> None:
        self._buscar(titulo).disponivel = True

    def disponiveis(self):
        
        for livro in self._acervo:
            if livro.disponivel:
                print(livro)

######## DEMONSTRAÇAO ########

if __name__ == "__main__":
    biblio = Biblioteca()
    biblio.cadastrar(Livro("Dom Casmurro", 1899))
    biblio.cadastrar(Livro("Vidas Secas", 1938))
    biblio.cadastrar(Livro("Memórias póstumas de Brás Cubas", 1881))

    biblio.disponiveis()

    try:
        biblio.emprestar("Dom Casmurro")
        biblio.emprestar("Dom Casmurro")    
    except LivroIndisponivelError as erro:
        print(f"Livro Indisponível: {erro}")
    except LivroNaoEncontradoError as erro:
        print(f"Livro não encontrado: {erro}")

    print("\nPÓS EMPRÉSTIMO:\n")
    biblio.disponiveis()

    try:
        biblio.emprestar("Não existe")
    except LivroIndisponivelError as erro:
        print(f"Livro Indisponível: {erro}")
    except LivroNaoEncontradoError as erro:
        print(f"Livro não encontrado: {erro}")

    biblio.devolver("Dom Casmurro")

    print("\nPÓS DEVOLUÇÃO:\n")
    biblio.disponiveis()
