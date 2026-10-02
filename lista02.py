class SalarioInvalidoError(Exception):
    pass


class EmailInvalidoError(Exception):
    pass


class Funcionario:
    SALARIO_MINIMO = 1512.00 

    def __init__(self, nome: str, salario: float):
        self.nome = nome
        self.salario = salario  #validação do setter

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, valor: float):
        if valor < self.SALARIO_MINIMO:
            raise SalarioInvalidoError(
                f"Salário (R$ {valor:.2f}) abaixo do mínimo permitido (R$ {self.SALARIO_MINIMO:.2f})."
            )
        self._salario = valor

    def aumentar(self, percentual: float):
        if not (0 < percentual <= 30):
            raise ValueError(
                f"Percentual de {percentual}% é inválido. Permissão apenas para 0 < percentual <= 30."
            )
        self.salario += self.salario * (percentual / 100)


class Email:
    def __init__(self, endereco: str):
        self.endereco = endereco

    @property
    def endereco(self) -> str:
        return self._endereco

    @endereco.setter
    def endereco(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise EmailInvalidoError(
                f"Endereço '{valor}' inválido. Deve conter '@' e '.'."
            )
        self._endereco = valor


# --- Teste dos casos de erro (Item 8) ---
if __name__ == "__main__":
    # Testes Funcionario
    try:
        f1 = Funcionario("Ana", 1000.00)
    except SalarioInvalidoError as e:
        print(f"[Erro Funcionario 1]: {e}")

    try:
        f2 = Funcionario("Carlos", 2000.00)
        f2.aumentar(50)
    except ValueError as e:
        print(f"[Erro Funcionario 2]: {e}")

    # Testes Email
    try:
        e1 = Email("usuario_sem_arroba.com")
    except EmailInvalidoError as e:
        print(f"[Erro Email 1]: {e}")

    try:
        e2 = Email("usuario@dominio_sem_ponto")
    except EmailInvalidoError as e:
        print(f"[Erro Email 2]: {e}")
