

def GEN(seed : str) -> str:
    tabela_sbox = {
        "00": "01",
        "01": "00", 
        "10": "11",
        "11": "10"
    }
    min_size = 4*len(seed)  # Define o tamanho mínimo da chave

    # Expande a seed até ter pelo menos o tamanho mínimo
    seed_expanded = seed
    while len(seed_expanded) < min_size:
        seed_expanded = seed_expanded + seed_expanded[::-1]
    
    # Primeira transformação: aplica S-box na seed expandida
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


def test_encryption_decryption():
    # Teste 1: Verificar se a mensagem é recuperada corretamente
    seed = "00"
    k = GEN(seed)
    m = "11010101"
    c = ENC(k, m)
    n = DEC(k, c)
    print("\nTeste 1 - Recuperação da mensagem:")
    print(f"Mensagem original: {m}")
    print(f"Mensagem decriptada: {n}")
    print(f"Teste passou? {m == n}")

def test_key_generation():
    # Teste 2: Verificar se seeds diferentes geram chaves diferentes
    seed1 = "00"
    seed2 = "11"
    k1 = GEN(seed1)
    k2 = GEN(seed2)
    print("\nTeste 2 - Chaves diferentes para seeds diferentes:")
    print(f"Chave 1 (seed 00): {k1}")
    print(f"Chave 2 (seed 11): {k2}")
    print(f"Teste passou? {k1 != k2}")

def test_diffusion():
    # Teste 3: Verificar difusão - mudança de 1 bit na mensagem
    seed = "00"
    k = GEN(seed)
    m1 = "11010101"
    m2 = "11010100"  # Último bit diferente
    c1 = ENC(k, m1)
    c2 = ENC(k, m2)
    diff_bits = sum(1 for a, b in zip(c1, c2) if a != b)
    print("\nTeste 3 - Difusão (mudança de 1 bit na mensagem):")
    print(f"Cifra 1: {c1}")
    print(f"Cifra 2: {c2}")
    print(f"Número de bits diferentes: {diff_bits}")
    print(f"Teste passou? {diff_bits > 1}")  # Esperamos que mais de 1 bit mude

def test_confusion():
    # Teste 4: Verificar confusão - mesma mensagem com chaves diferentes
    m = "11010101"
    k1 = GEN("11")
    k2 = GEN("01")
    c1 = ENC(k1, m)
    c2 = ENC(k2, m)
    diff_bits = sum(1 for a, b in zip(c1, c2) if a != b)
    print("\nTeste 4 - Confusão (mesma mensagem, chaves diferentes):")
    print(f"Cifra 1: {c1}")
    print(f"Cifra 2: {c2}")
    print(f"Número de bits diferentes: {diff_bits}")
    print(f"Teste passou? {diff_bits >= len(m)/2}")  # Esperamos que pelo menos metade dos bits mude

def main():
    print("Testes do algoritmo de criptografia GSI035")
    print("-" * 50)
    
    test_encryption_decryption()  # Teste de recuperação da mensagem
    test_key_generation()         # Teste de geração de chaves
    test_diffusion()             # Teste de difusão
    test_confusion()             # Teste de confusão

if __name__ == "__main__":
    main()
