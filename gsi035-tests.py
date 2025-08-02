import time



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


def contar_bits_diferentes(a: str, b: str) -> int:
    """Conta quantos bits são diferentes entre duas strings binárias."""
    return sum(1 for x, y in zip(a, b) if x != y)

def testar_tempo_execucao(seed: str, mensagem: str):
    """Mede o tempo de execução de GEN, ENC e DEC."""
    inicio = time.time()
    k = GEN(seed)
    tempo_gen = time.time() - inicio

    k_final = (k * ((len(mensagem)//len(k))+1))[:len(mensagem)]

    inicio = time.time()
    c = ENC(k_final, mensagem)
    tempo_enc = time.time() - inicio

    inicio = time.time()
    _ = DEC(k_final, c)
    tempo_dec = time.time() - inicio

    return tempo_gen, tempo_enc, tempo_dec

def testar_difusao(seed: str, mensagem: str):
    """Altera 1 bit da mensagem e verifica quantos bits do ciphertext mudam."""
    k = GEN(seed)
    k_final = (k * ((len(mensagem)//len(k))+1))[:len(mensagem)]
    
    # Mensagem original e criptografada
    c1 = ENC(k_final, mensagem)
    
    # Altera o primeiro bit da mensagem
    mensagem_alterada = ('1' if mensagem[0]=='0' else '0') + mensagem[1:]
    c2 = ENC(k_final, mensagem_alterada)

    bits_diferentes = contar_bits_diferentes(c1, c2)
    return c1, c2, bits_diferentes

def testar_confusao(seed: str, mensagem: str):
    """Altera 1 bit da chave e verifica quantos bits do ciphertext mudam."""
    k1 = GEN(seed)
    k_final1 = (k1 * ((len(mensagem)//len(k1))+1))[:len(mensagem)]
    
    # Criptografa com chave original
    c1 = ENC(k_final1, mensagem)

    # Seed alterada no primeiro bit
    seed_alterada = ('1' if seed[0]=='0' else '0') + seed[1:]
    k2 = GEN(seed_alterada)
    k_final2 = (k2 * ((len(mensagem)//len(k2))+1))[:len(mensagem)]

    # Criptografa com chave alterada
    c2 = ENC(k_final2, mensagem)

    bits_diferentes = contar_bits_diferentes(c1, c2)
    return c1, c2, bits_diferentes

def main():
    print("Olá! Este é o arquivo GSI035")
    print(f"Python versão em uso: {__import__('sys').version}")
    print("Gerando chave...")

    seed = "0101"
    mensagem = "11010101"

    # Gerar chave
    k = GEN(seed)
    print(f"Chave gerada: {k}")

    # Ajustar chave ao tamanho da mensagem
    k_final = (k * ((len(mensagem) // len(k)) + 1))[:len(mensagem)]

    # Criptografar
    c = ENC(k_final, mensagem)
    print(f"Mensagem original: {mensagem}")
    print(f"Mensagem criptografada: {c}")

    # Descriptografar
    m_decripto = DEC(k_final, c)
    print(f"Mensagem descriptografada: {m_decripto}")
    print(f"Mensagem original é igual à descriptografada? {mensagem == m_decripto}")
    print()

    # Teste de Tempo
    print("=== Teste de Tempo de Execução ===")
    tgen, tenc, tdec = testar_tempo_execucao(seed, mensagem)
    print(f"TEMPO GEN: {tgen:.8f} segundos")
    print(f"TEMPO ENC: {tenc:.8f} segundos")
    print(f"TEMPO DEC: {tdec:.8f} segundos\n")

    # Teste de Difusão
    print("=== Teste de Difusão ===")
    c1, c2, dif = testar_difusao(seed, mensagem)
    print(f"Ciphertext original : {c1}")
    print(f"Ciphertext alterado : {c2}")
    print(f"Bits diferentes     : {dif}/{len(mensagem)}\n")

    # Teste de Confusão
    print("=== Teste de Confusão ===")
    c1, c2, dif = testar_confusao(seed, mensagem)
    print(f"Ciphertext com chave original : {c1}")
    print(f"Ciphertext com chave alterada : {c2}")
    print(f"Bits diferentes               : {dif}/{len(mensagem)}\n")

if __name__ == "__main__":
    main()