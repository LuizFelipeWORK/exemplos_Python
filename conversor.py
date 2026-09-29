class ConversorMedidas:
    @staticmethod
    def celsius_para_fahrenheit(celsius: float) -> float:
        return (celsius * 9/5) + 32

# Chamada direta pela classe, sem instanciar
temp_f = ConversorMedidas.celsius_para_fahrenheit(25.0)
print(temp_f)  
