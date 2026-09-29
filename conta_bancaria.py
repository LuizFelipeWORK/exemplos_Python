from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. EXCEÇÕES PERSONALIZADAS (HERANÇA)
# ==========================================
class ErroBancario(Exception): pass
class SaldoInsuficienteError(ErroBancario): pass
class ValorInvalidoError(ErroBancario): pass


# ==========================================
# 2. MÉTODOS ESTÁTICOS (@staticmethod)
# ==========================================
class ValidadorCPF:
    @staticmethod
    def e_valido(cpf: str) -> bool:
        cpf_limpo = "".join(filter(str.isdigit, cpf))
        return len(cpf_limpo) == 11


# ==========================================
# 3. COMPOSIÇÃO (OBJETO DENTRO DE OBJETO)
# ==========================================
class Transacao:
    def __init__(self, tipo: str, valor: float):
        self.tipo = tipo
        self.valor = valor
        self.data = datetime.now()

    def __str__(self) -> str:
        return f"[{self.data.strftime('%H:%M:%S')}] {self.tipo}: R$ {self.valor:.2f}"

    def __repr__(self) -> str:
        return f"Transacao(tipo='{self.tipo}', valor={self.valor})"


class Cliente:
    def __init__(self, nome: str, cpf: str):
        if not ValidadorCPF.e_valido(cpf):
            raise ValorInvalidoError(f"CPF inválido: {cpf}")
        self.nome = nome
        self._cpf = cpf  # Atributo protegido

    @property
    def cpf(self) -> str:
        return self._cpf

    def __str__(self) -> str:
        return f"Cliente: {self.nome} (CPF: {self._cpf})"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Cliente):
            return NotImplemented
        return self._cpf == outro._cpf


# ==========================================
# 4. CLASSE ABSTRATA & ENCAPSULAMENTO
# ==========================================
class Conta(ABC):
    banco = "Python Bank"  # Atributo de Classe

    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0):
        self._numero = numero
        self._cliente = cliente  # Composição: Conta "tem um" Cliente
        self._saldo = max(0.0, saldo_inicial)
        self._historico: list[Transacao] = []  # Composição: Conta "tem várias" Transações

    # Encapsulamento com @property
    @property
    def numero(self) -> int:
        return self._numero

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def saldo(self) -> float:
        return self._saldo

    # Construtor Alternativo (@classmethod)
    @classmethod
    def criar_zerada(cls, numero: int, cliente: Cliente) -> "Conta":
        return cls(numero, cliente, saldo_inicial=0.0)

    # Operações
    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser maior que zero.")
        self._saldo += valor
        self._historico.append(Transacao("DEPÓSITO", valor))

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser maior que zero.")
        if valor > self._saldo:
            raise SaldoInsuficienteError(f"Saldo insuficiente na Conta #{self._numero}.")
        self._saldo -= valor
        self._historico.append(Transacao("SAQUE", valor))

    # Método Abstrato (Polimorfismo obrigatório nas subclasses)
    @abstractmethod
    def aplicar_fechamento_mensal(self) -> None:
        pass

    # Métodos Mágicos (Dunder Methods)
    def __str__(self) -> str:
        return f"{self.banco} | Conta #{self._numero} | Titular: {self._cliente.nome} | Saldo: R$ {self._saldo:.2f}"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Conta):
            return NotImplemented
        return self._numero == outro._numero

    def __len__(self) -> int:
        return len(self._historico)  # Permite usar len(conta)

    def __getitem__(self, indice: int) -> Transacao:
        return self._historico[indice]  # Permite usar conta[0]


# ==========================================
# 5. HERANÇA & POLIMORFISMO
# ==========================================
class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0, limite: float = 500.0):
        super().__init__(numero, cliente, saldo_inicial)  # Uso do super()
        self.limite = limite

    # Sobrescrita do método sacar com regra de limite
    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser maior que zero.")
        if valor > (self._saldo + self.limite):
            raise SaldoInsuficienteError(f"Valor excede o saldo e o limite de cheque especial (R$ {self.limite:.2f}).")
        self._saldo -= valor
        self._historico.append(Transacao("SAQUE (C.C.)", valor))

    def aplicar_fechamento_mensal(self) -> None:
        taxa = 20.0
        self._saldo -= taxa
        self._historico.append(Transacao("TAXA MANUTENÇÃO", taxa))


class ContaPoupanca(Conta):
    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0, taxa_rendimento: float = 0.005):
        super().__init__(numero, cliente, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    def aplicar_fechamento_mensal(self) -> None:
        rendimento = self._saldo * self.taxa_rendimento
        self._saldo += rendimento
        self._historico.append(Transacao("RENDIMENTO POUPANÇA", rendimento))


# ==========================================
# DEMONSTRAÇÃO PRÁTICA (FLUXO DE EXECUÇÃO)
# ==========================================
if __name__ == "__main__":
    # 1. Criação de clientes e teste de validação estática
    cliente1 = Cliente("Maria Silva", "12345678901")
    cliente2 = Cliente("João Souza", "98765432100")
    cliente_duplicado = Cliente("Maria Silva", "12345678901")

    print(f"Comparação de Clientes (Maria == Duplicado): {cliente1 == cliente_duplicado}\n")

    # 2. Instanciação de Contas (Uso do Construtor Padrão e Classmethod)
    cc = ContaCorrente(numero=1001, cliente=cliente1, saldo_inicial=200.0, limite=300.0)
    cp = ContaPoupanca.criar_zerada(numero=2002, cliente=cliente2)

    # 3. Operações e Tratamento de Exceções
    print("--- REALIZANDO OPERAÇÕES ---")
    cc.depositar(100.0)
    
    try:
        cc.sacar(700.0)  # Tenta sacar mais do que saldo + limite (200 + 100 + 300 = 600)
    except ErroBancario as erro:
        print(f"Erro Capturado: {erro}")

    # Saque válido utilizando o limite do cheque especial
    cc.sacar(550.0)

    # Operações na Poupança
    cp.depositar(1000.0)

    # 4. Polimorfismo na Prática
    print("\n--- APLICANDO FECHAMENTO MENSAL (POLIMORFISMO) ---")
    contas: list[Conta] = [cc, cp]
    for conta in contas:
        conta.aplicar_fechamento_mensal()
        print(conta)

    # 5. Uso de Métodos Mágicos (__len__ e __getitem__)
    print(f"\n--- HISTÓRICO DA CONTA CORRENTE ({len(cc)} transações) ---")
    for transacao in cc:
        print(f" -> {transacao}")
