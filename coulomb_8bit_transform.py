#!/usr/bin/env python3
"""
EIDA Coulomb 8-bit Blok Dönüşümü
Geliştirici: Güven Acar
Proje: EIDA — IoT için kuantum dirençli kriptografi altyapısı
"""

def coulomb_force_6(gate_bits):
    """
    6-bit kapıdan geçen kuvveti hesapla.
    gate_bits: [g₋₃, g₋₂, g₋₁, g₊₁, g₊₂, g₊₃]
    Pozisyon:  [-3,  -2,  -1,  +1,  +2,  +3]
    """
    positions = [-3, -2, -1, +1, +2, +3]
    F = 0.0
    
    for bit, pos in zip(gate_bits, positions):
        direction = 1 if pos > 0 else -1  # sağ: +1, sol: -1
        if bit == 1:
            # Zıt yük, çeker → +direction/|pos|
            F += (direction / abs(pos))
        else:
            # Aynı yük, iter → -direction/|pos|
            F -= (direction / abs(pos))
    
    return F


def coulomb_bit(passing_bit, gate_bits):
    """
    Geçen biti (0 veya 1) kapıdan geçir ve dönüştürülmüş biti döndür.
    
    passing_bit = 0 (elektron):
        F > 0 → 1,  F ≤ 0 → 0
    
    passing_bit = 1 (pozitron):
        F > 0 → 0,  F ≤ 0 → 1  (tam tersi)
    """
    F = coulomb_force_6(gate_bits)
    
    if passing_bit == 0:
        # Elektron
        return 1 if F > 0 else 0
    else:
        # Pozitron
        return 0 if F > 0 else 1


def get_gate(state, idx, n=8):
    """
    Bloktaki idx pozisyonunun etrafından 6-bit kapı oluştur.
    Dairesel erişim: sol 3 bit, sağ 3 bit
    
    n=8 için:
    idx=0 → pozisyonlar: [-3→5, -2→6, -1→7, +1→1, +2→2, +3→3]
    """
    offsets = [-3, -2, -1, +1, +2, +3]
    gate = []
    for offset in offsets:
        gate_idx = (idx + offset) % n
        gate.append(state[gate_idx])
    return gate


def pass_through_8bit(state, gate_block):
    """
    8-bit demetin kapı bloğundan geçişi.
    
    state: geçen demet (tuple veya list, 8 bit)
    gate_block: kapı durumu (tuple veya list, 8 bit)
    
    Her bit i için:
        gate_i = get_gate(gate_block, i)
        result[i] = coulomb_bit(state[i], gate_i)
    
    Çıktı: tuple (8 bit)
    """
    result = []
    for i in range(8):
        gate = get_gate(gate_block, i, n=8)
        transformed_bit = coulomb_bit(state[i], gate)
        result.append(transformed_bit)
    
    return tuple(result)


def bits_to_int(bits):
    """Bit listesini/tuplesi tamsayıya çevir."""
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value


def int_to_bits(value, length=8):
    """Tamsayıyı bit listesine çevir."""
    bits = []
    for i in range(length - 1, -1, -1):
        bits.append((value >> i) & 1)
    return tuple(bits)


def bits_hamming_distance(bits1, bits2):
    """Hamming mesafesi (farklı bit sayısı)."""
    return sum(b1 != b2 for b1, b2 in zip(bits1, bits2))


def test_single_transformation():
    """Tek bir dönüşümü test et ve göster."""
    print("=" * 70)
    print("EIDA COULOMB 8-BIT BLOK DÖNÜŞÜMÜ - TESTİ")
    print("=" * 70)
    
    # Örnek giriş ve kapı
    state = (1, 0, 1, 0, 1, 0, 1, 0)  # 10101010 = 170
    gate = (0, 0, 1, 1, 1, 0, 0, 1)   # 00111001 = 57
    
    print(f"\nGiriş durumu:   {state} = {bits_to_int(state):3d}")
    print(f"Kapı durumu:    {gate}  = {bits_to_int(gate):3d}")
    
    # Dönüşümü uygula
    result = pass_through_8bit(state, gate)
    
    print(f"Çıkış:          {result} = {bits_to_int(result):3d}")
    
    # Ayrıntılı gösterim
    print("\n" + "-" * 70)
    print("DETAYLI İŞLEM:")
    print("-" * 70)
    
    for i in range(8):
        gate_around = get_gate(gate, i, n=8)
        force = coulomb_force_6(gate_around)
        in_bit = state[i]
        out_bit = result[i]
        
        gate_str = ''.join(map(str, gate_around))
        print(f"Bit {i}: {in_bit} → ", end="")
        print(f"kapı=[{gate_str}] F={force:+.3f} → {out_bit}")
    
    hamming = bits_hamming_distance(state, result)
    print(f"\nHamming mesafesi (değişen bit sayısı): {hamming}/8")
    
    return state, gate, result


def test_avalanche_effect():
    """Avalanche etkisini test et (1 bit değişikliğin etkisi)."""
    print("\n" + "=" * 70)
    print("AVALANCHE ETKİSİ TESTİ")
    print("=" * 70)
    
    gate = (0, 1, 1, 0, 1, 0, 1, 1)
    
    results_per_flip = {}
    
    print(f"\nKapı: {gate} = {bits_to_int(gate)}\n")
    print("Giriş bit çevrilmesi → Çıkış değişimi:")
    print("-" * 70)
    
    for flip_pos in range(8):
        # Referans durumu: 00000000
        state_ref = (0,) * 8
        result_ref = pass_through_8bit(state_ref, gate)
        
        # Flip pozisyonundaki bit
        state_flip = list(state_ref)
        state_flip[flip_pos] = 1
        state_flip = tuple(state_flip)
        result_flip = pass_through_8bit(state_flip, gate)
        
        # Avalanche: kaç bit değişti?
        avalanche = bits_hamming_distance(result_ref, result_flip)
        results_per_flip[flip_pos] = avalanche
        
        print(f"Bit {flip_pos} flip: {state_flip} → {result_flip} | "
              f"Değişim: {avalanche}/8 (%{100*avalanche/8:.1f})")
    
    avg_avalanche = sum(results_per_flip.values()) / len(results_per_flip)
    print(f"\nOrtalama avalanche: {avg_avalanche:.1f}/8 (%{100*avg_avalanche/8:.1f})")


def test_bijection_sampling():
    """
    Bijeksiyon özelliğini örneklemle test et (tam test 256² uzay için yavaş).
    16 rastgele kapı ve her kapı için 256 giriş testi.
    """
    print("\n" + "=" * 70)
    print("BİJEKSİYON TESTİ (Örneklemli)")
    print("=" * 70)
    
    import random
    
    random.seed(42)
    
    collision_found = False
    total_tests = 0
    total_unique = 0
    
    for gate_test in range(16):
        gate = tuple(random.randint(0, 1) for _ in range(8))
        
        outputs = {}
        collisions = 0
        
        # Bu kapı için tüm 256 girişi test et
        for state_int in range(256):
            state = int_to_bits(state_int, 8)
            result = pass_through_8bit(state, gate)
            result_int = bits_to_int(result)
            
            if result_int in outputs:
                collisions += 1
                collision_found = True
            else:
                outputs[result_int] = state_int
        
        total_tests += 1
        total_unique += len(outputs)
        
        status = "✓ BİJEKTİF" if collisions == 0 else f"✗ {collisions} çarpışma"
        print(f"Kapı {gate_test}: {gate} | Benzersiz çıkış: {len(outputs)}/256 | {status}")
    
    avg_unique = total_unique / total_tests
    print(f"\nOrtalama benzersiz çıkış: {avg_unique:.1f}/256")
    if collision_found:
        print("⚠️  Bazı kapılarda bijeksiyon sağlanmıyor!")
    else:
        print("✓ Tüm test kapılarında bijeksiyon sağlandı.")


def demo_sequence():
    """Ardışık dönüşümlerin etkisini göster."""
    print("\n" + "=" * 70)
    print("ARDIŞIK DÖNÜŞÜM DEMOSu")
    print("=" * 70)
    
    state = (0, 0, 0, 0, 0, 0, 0, 1)  # 1 bit set
    gate = (1, 0, 1, 0, 1, 0, 1, 0)
    
    print(f"\nBaşlangıç: {state} = {bits_to_int(state)}")
    print(f"Sabit kapı: {gate}\n")
    
    current = state
    for tur in range(5):
        current = pass_through_8bit(current, gate)
        print(f"Tur {tur+1}: {current} = {bits_to_int(current)}")


if __name__ == "__main__":
    import sys
    
    # Çıktıyı txt dosyasına yönlendir
    output_file = open('coulomb_8bit_output.txt', 'w', encoding='utf-8')
    sys.stdout = output_file
    
    try:
        # Testleri çalıştır
        test_single_transformation()
        test_avalanche_effect()
        test_bijection_sampling()
        demo_sequence()
        
        print("\n" + "=" * 70)
        print("TÜM TESTLER TAMAMLANDI")
        print("=" * 70)
    finally:
        output_file.close()
        sys.stdout = sys.__stdout__  # stdout'u geri eski haline getir
        print("✓ Çıktı coulomb_8bit_output.txt dosyasına kaydedildi.")
