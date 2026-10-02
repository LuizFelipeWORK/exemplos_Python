class ErroDeConta(Exception):
    """Classe base para erros de domínio bancário."""

    pass


class ValorInvalidoError(ErroDeConta):
    pass


class SaldoInsuficienteError(ErroDeConta):
    pass


class LimiteExcedidoError(ErroDeConta):
    pass


class ContaBancaria:
    LIMITE_SAQUE = 1000.00

    def __init__(self, saldo_inicial: float = 0.0):
        self._saldo = max(0.0, saldo_inicial)

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        self._saldo += valor

    def sacar(self, valor: float):
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if valor > self.LIMITE_SAQUE:
            raise LimiteExcedidoError(
                f"Limite máximo por saque é de R$ {self.LIMITE_SAQUE:.2f}."
            )
        if valor > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente. Saldo atual: R$ {self._saldo:.2f}."
            )

        self._saldo -= valor


# --- Interface do Caixa Eletrônico ---
def caixa_eletronico():
    conta = ContaBancaria(saldo_inicial=500.00)

    while True:
        print("\n=== CAIXA ELETRÔNICO ===")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Consultar Saldo")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "4":
            print("Sessão encerra com sucesso. Até logo!")
            break

        try:
            if opcao == "1":
                valor = float(input("Digite o valor para depósito: R$ "))
                conta.depositar(valor)
                print(
                    f"Depósito realizado! Saldo atual: R$ {conta.saldo:.2f}"
                )

            elif opcao == "2":
                valor = float(input("Digite o valor para saque: R$ "))
                conta.sacar(valor)
                print(f"Saque realizado! Saldo atual: R$ {conta.saldo:.2f}")

            elif opcao == "3":
                print(f"Saldo atual: R$ {conta.saldo:.2f}")

            else:
                print("Opção inválida! Escolha entre 1 e 4.")

        except ValueError:
            print("Erro de entrada: Digite apenas valores numéricos válidos.")
        except ErroDeConta as e:
            #captura os 3 erros: ValorInvalido, SaldoInsuficiente e LimiteExcedido
            print(f"Falha na Operação ({e.__class__.__name__}): {e}")


if __name__ == "__main__":
    caixa_eletronico()
