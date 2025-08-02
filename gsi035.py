

def GEN(seed : str) -> str:
    resultado_parts = []
    t = len(seed)
    seed_reversed = seed[::-1]
    first = seed + seed_reversed
    first_reversed = first[::-1]
    rotacao_direita = first[-1] + first[:-1]
    resultado_parts.append(XOR_BITS(rotacao_direita, first_reversed))

    tabela_sbox = {
        "00": "01",
        "01": "00", 
        "10": "11",
        "11": "10"
    }
    for i in range(0, len(first), 2):
        bloco = first_reversed[i:i+2]
        resultado_parts.append(tabela_sbox.get(bloco, XOR_BITS(bloco, "01")))
    
    resultado_parts.pop(0) 
    resultado_parts.append("1")
    return "".join(resultado_parts)

def ENC(k: str, m: str) -> str:
  return XOR_BITS(k, m)

def DEC(k: str, c: str) -> str:
 return XOR_BITS(k, c)

def XOR_BITS(bit1: str, bit2: str) -> str:
    if len(bit1) != len(bit2):
        raise ValueError("Chave e mensagem devem ter o mesmo tamanho")
    return "".join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bit1, bit2))


def main():
    print("Olá! Este é o arquivo GSI035")
    print(f"Python versão em uso: {__import__('sys').version}")
    print("Gerando chave...")
    seed = "00"
    k = GEN(seed)
    print(f"Chave gerada: {k}")
    m = "11010101"
    c = ENC(k, m)
    print(f"Mensagem criptografada: {c}")
    n = DEC(k, c)
    print(f"Mensagem descriptografada: {n}")
    print(f"Mensagem criptografada: {m} é igual mensagem descriptografada: {n}")
    print(m == n)
if __name__ == "__main__":
    main()
