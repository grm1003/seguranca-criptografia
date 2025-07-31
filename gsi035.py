

def GEN(seed : str) -> str:
    return seed  # Simplesmente retorna a semente como chave para fins de exemplo

def ENC(k: str, m: str) -> str:
  return XOR_BITS(k, m)

def DEC(k: str, c: str) -> str:
 return XOR_BITS(k, c)


def XOR_BITS(bit1: str, bit2: str) -> str:
    if len(bit1) != len(bit2):
        raise ValueError("Chave e mensagem devem ter o mesmo tamanho")
    resultado = ""
    for b1, b2 in zip(bit1, bit2):
        resultado += str(int(b1) ^ int(b2))
    return resultado


def main():
    print("Olá! Este é o arquivo GSI035")
    print(f"Python versão em uso: {__import__('sys').version}")
    m = "1101"
    k = "1001"
    c = ENC(k, m)
    print(f"Mensagem criptografada: {c}")
    n = DEC(k, c)
    print(f"Mensagem descriptografada: {n}")
    print(f"Mensagem criptografada: {m} é igual mensagem descriptografada: {n}")
    print(m == n)
if __name__ == "__main__":
    main()
