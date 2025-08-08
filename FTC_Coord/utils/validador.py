import datetime
import re

class Validador:

    @staticmethod
    def validar_email(email):
        """Valida formato de email básico."""
        padrao = r"^[^@]+@[^@]+\.[^@]+$"
        return bool(re.match(padrao, email))

    @staticmethod
    def validar_telefone(numero, digitos_min=9):
        """Confirma se o telefone tem somente dígitos e tamanho mínimo."""
        return numero.isdigit() and len(numero) >= digitos_min

    @staticmethod
    def validar_codigo_postal(codigo):
        """Verifica se o código postal é numérico."""
        return codigo.isdigit()

    @staticmethod
    def validar_data(data):
        """Verifica se a data é válida e não está no futuro."""
        try:
            if isinstance(data, datetime.datetime):
                data = data.date()
            elif not isinstance(data, datetime.date):
                raise ValueError("Formato de data inválido.")
            return data <= datetime.date.today()
        except Exception as e:
            print(f"⚠️ Erro na validação de data: {e}")
            return False

    @staticmethod
    def validar_numerico(valor):
        """Valida se um valor é composto apenas por dígitos."""
        return str(valor).isdigit()

    @staticmethod
    def validar_obrigatorios(campos_dict):
        """
        Verifica se todos os campos obrigatórios estão preenchidos.
        Aceita strings não vazias, números, datas — ignora valores nulos ou vazios.
        """
        return all(bool(campo) for campo in campos_dict.values())
    