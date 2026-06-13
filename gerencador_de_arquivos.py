import os
import csv

class GerenciadorArquivo:
    """
    Classe responsável por salvar e recuperar dados em arquivos CSV,
    preservando os tipos básicos (int, float, string).
    """
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

    def salvarDados(self, lista):
        """
        Recebe uma lista de listas e salva no arquivo no formato CSV.
        Exemplo: [['Pizza', 50.0], ['Refri', 10]] -> "Pizza,50.0\nRefri,10\n"
        """
        try:
            with open(self.nome_arquivo, "w", encoding="utf-8") as arquivo:
                for sublista in lista:
                    # Converte cada elemento para string para poder unir com vírgula
                    linha = ",".join(str(elemento) for elemento in sublista)
                    arquivo.write(linha + "\n")
            print(f"Dados salvos com sucesso em {self.nome_arquivo}!")
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def recuperaDados(self):
        """
        Lê o arquivo CSV e retorna uma lista de listas com os tipos convertidos.
        """
        dados = []
        if not os.path.exists(self.nome_arquivo):
            return dados
        
        try:
            with open(self.nome_arquivo, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha:
                        continue
                    
                    elementos = linha.split(",")
                    linha_com_tipos = []
                    
                    for item in elementos:
                        # Lógica de conversão automática de tipos
                        try:
                            # Tenta converter para inteiro
                            valor = int(item)
                        except ValueError:
                            try:
                                # Tenta converter para float
                                valor = float(item)
                            except ValueError:
                                # Mantém como string se falhar em ambos
                                valor = item
                        
                        linha_com_tipos.append(valor)
                    
                    dados.append(linha_com_tipos)
            return dados
        except Exception as e:
            print(f"Erro ao recuperar dados: {e}")
            return []