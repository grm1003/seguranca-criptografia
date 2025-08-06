

def GEN(seed : str) -> str:
    min_size = 4*len(seed)  # Define o tamanho mínimo da chave

    # Expande a seed até ter pelo menos o tamanho mínimo
    seed_expanded = seed
    while len(seed_expanded) < min_size:
        seed_expanded = seed_expanded + seed_expanded[::-1]
    
    # Primeira transformação: aplica S-box na seed expandida
        tabela_sbox = {
        "00": "01",
        "01": "00", 
        "10": "11",
        "11": "10"
    }
    resultado = ""
    for i in range(0, len(seed_expanded), 2):
        bloco = seed_expanded[i:i+2]
        resultado += tabela_sbox.get(bloco, XOR_BITS(bloco, "01"))
    
    # Segunda transformação: rotação baseada no valor da seed
    seed_value = int(seed, 2)  # converte seed para número
    rotacao = (seed_value % len(resultado)) + 1
    resultado = resultado[rotacao:] + resultado[:rotacao]
    
    # Terceira transformação: aplica padrão baseado na seed
    padrao = ""
    for i in range(len(resultado)):
        if i % 2 == (seed_value % 2):
            padrao += "1"
        else:
            padrao += "0"
    resultado = XOR_BITS(resultado, padrao)
    
    temp = ""
    for i in range(0, len(resultado), 2):
        bloco = resultado[i:i+2]
        temp += tabela_sbox.get(bloco, XOR_BITS(bloco, "01"))
    resultado = temp

    return resultado[:min_size] 

def ENC(k: str, m: str) -> str:
    # Primeiro passo: XOR inicial
    resultado = XOR_BITS(k, m)
    
    # Segundo passo: substituição usando S-box para confusão
    temp = ""
    for i in range(0, len(resultado), 2):
        bloco = resultado[i:i+2] if i+1 < len(resultado) else resultado[i] + "0"
        if len(bloco) == 2:
            valor_bloco = int(bloco, 2)
            novo_bloco = format((valor_bloco + int(k[i:i+2], 2)) % 4, '02b')
            temp += novo_bloco
        else:
            temp += bloco
    resultado = temp
    
    # Terceiro passo: rotação final
    rotacao = (int(k, 2) % len(resultado)) + 1
    return resultado[rotacao:] + resultado[:rotacao]

def DEC(k: str, c: str) -> str:
    # Primeiro passo: rotação inversa
    rotacao = (int(k, 2) % len(c)) + 1
    rotacao_inversa = len(c) - rotacao
    resultado = c[rotacao_inversa:] + c[:rotacao_inversa]
    
    # Segundo passo: desfaz a substituição
    temp = ""
    for i in range(0, len(resultado), 2):
        bloco = resultado[i:i+2] if i+1 < len(resultado) else resultado[i] + "0"
        if len(bloco) == 2:
            valor_bloco = int(bloco, 2)
            valor_k = int(k[i:i+2], 2)
            novo_bloco = format((valor_bloco - valor_k) % 4, '02b')
            temp += novo_bloco
        else:
            temp += bloco
    resultado = temp
    
    # Terceiro passo: XOR final
    return XOR_BITS(k, resultado)

def XOR_BITS(bit1: str, bit2: str) -> str:
    if len(bit1) != len(bit2):
        raise ValueError("Chave e mensagem devem ter o mesmo tamanho")
    resultado = ""
    for b1, b2 in zip(bit1, bit2):
        resultado += str(int(b1) ^ int(b2))
    return resultado

def main():
    print("Testes do algoritmo de criptografia GSI035")
    print("-" * 50)
    
    seed = "00"
    k = GEN(seed)
    m = "11010101"
    c = ENC(k, m)
    n = DEC(k, c)
    print("\nTeste 1 - Recuperação da mensagem:")
    print(f"Mensagem original: {m}")
    print(f"Mensagem decriptada: {n}")
    print(f"Teste passou? {m == n}")


if __name__ == "__main__":
    main()
