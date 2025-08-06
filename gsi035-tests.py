
from gsi035 import DEC, ENC, GEN


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
    k2 = GEN("00")
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
