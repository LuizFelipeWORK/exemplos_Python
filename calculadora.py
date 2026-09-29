# ==========================================
# 1. EXCEÇÃO PERSONALIZADA
# ==========================================
class OperacaoInvalidaError(Exception):
    """Lançada quando o operador fornecido não é suportado."""
    pass


# ==========================================
# 2. CLASSE CALCULADORA (MÉTODOS ESTÁTICOS)
# ==========================================
class Calculadora:
    @staticmethod
    def somar(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtrair(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiplicar(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def dividir(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Tentativa de divisão por zero não permitida.")
        return a / b

    def calcular(self, operacao: str, a: float, b: float) -> float:
        operacoes = {
            "+": self.somar,
            "-": self.subtrair,
            "*": self.multiplicar,
            "/": self.dividir,
        }
        if operacao not in operacoes:
            raise OperacaoInvalidaError(f"Operador '{operacao}' inválido. Use: +, -, * ou /.")
        
        return operacoes[operacao](a, b)


# ==========================================
# 3. INTERFACE DE USUÁRIO E TRATAMENTO
# ==========================================
def executar_calculadora():
    calc = Calculadora()
    print("=== CALCULADORA COM TRATAMENTO DE ERROS ===")

    while True:
        try:
            entrada_op = input("\nDigite a operação (+, -, *, /) ou 'sair': ").strip().lower()
            
            if entrada_op == "sair":
                print("Encerrando a calculadora. Até logo!")
                break

            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))

            resultado = calc.calcular(entrada_op, num1, num2)

        except ValueError:
            print("Erro de Entrada: Digite apenas números válidos (ex: 10 ou 5.5).")
        except ZeroDivisionError as erro:
            print(f"Erro Matemático: {erro}")
        except OperacaoInvalidaError as erro:
            print(f"Erro de Operação: {erro}")
        except Exception as erro:
            print(f"Erro Inesperado: {erro}")
        else:
            # Executado apenas se NENHUMA exceção ocorrer no bloco try
            print(f"Resultado: {num1} {entrada_op} {num2} = {resultado:.2f}")


if __name__ == "__main__":
    executar_calculadora()
