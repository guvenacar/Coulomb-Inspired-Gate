def get_gate_sequence(bits, index):
    """
    Her eleman için kapı dizisini belirle.
    bit 0 ise: o indexi başa al
    bit 1 ise: reverse et, sonra o indexi başa al
    """
    n = len(bits)
    if bits[index] == 0:
        # indexi başa al
        return bits[index:] + bits[:index]
    else:
        # reverse et, sonra indexi başa al
        rev = bits[::-1]
        # orijinal index, reverse'de n-1-index olur
        rev_index = n - 1 - index
        return rev[rev_index:] + rev[:rev_index]

def is_homogeneous(gate):
    """Kapı homojen mi? (hepsi 0 veya hepsi 1)"""
    return all(b == 0 for b in gate) or all(b == 1 for b in gate)

def is_symmetric_2bit(left, right):
    """2 bitlik kapıda simetri kontrolü: 01 10 veya 10 01 veya 00 00 veya 11 11"""
    if left == right and is_homogeneous(left):
        return True
    if left == [0,1] and right == [1,0]:
        return True
    if left == [1,0] and right == [0,1]:
        return True
    return False

def transform_bit(bit, gate):
    """
    Kapıdan geçen biti dönüştür.
    Homojen veya simetrik → değişmez
    Heterojen/asimetrik → dönüşür
    """
    if is_homogeneous(gate):
        return bit
    return 1 - bit

def process_1bit_gates(bits, index):
    """
    1 bitlik kapı: 8 kapı, ikililer oluştur
    Her eleman için 8 bit üretir (sadece ortadaki)
    """
    seq = get_gate_sequence(bits, index)
    n = len(seq)
    result = []
    for i in range(n):
        left = seq[i]
        right = seq[(i + 1) % n]
        gate = [left, right]
        new_bit = transform_bit(bits[index], gate)
        result.append(new_bit)
    return result  # 8 bit

def process_2bit_gates(bits, index):
    """
    2 bitlik kapı: 4 kapı, dörtlüler oluştur
    Her eleman için 4 bit üretir
    """
    seq = get_gate_sequence(bits, index)
    n = len(seq)
    
    # 1. adım: 2'şer grupla
    groups = []
    for i in range(0, n, 2):
        groups.append([seq[i], seq[(i+1) % n]])
    
    # 2. adım: her gruba sağdaki komşuyu ekle → dörtlüler
    result = []
    num_groups = len(groups)
    for i in range(num_groups):
        left = groups[i]
        right = groups[(i + 1) % num_groups]
        gate = left + right
        
        # simetri kontrolü
        if is_symmetric_2bit(left, right) or is_homogeneous(gate):
            new_bit = bits[index]
        else:
            new_bit = 1 - bits[index]
        result.append(new_bit)
    return result  # 4 bit

def process_6bit_gate(bits, index):
    """
    6 bitlik kapı: 8 mod 3 = 2, 2/2 = 1 kapı
    Her eleman için 1 bit üretir
    """
    seq = get_gate_sequence(bits, index)
    n = len(seq)
    
    # 3'er grupla
    groups = []
    for i in range(0, n, 3):
        if i + 2 < n:
            groups.append([seq[i], seq[i+1], seq[i+2]])
    
    # 8 mod 3 = 2 → 1 kapı
    # ilk grup sol kanat, ikinci grup sağ kanat
    if len(groups) >= 2:
        gate = groups[0] + groups[1]  # 6 bit kapı
        new_bit = transform_bit(bits[index], gate)
    else:
        new_bit = bits[index]
    return [new_bit]  # 1 bit

def process_8bit_gate(bits, index):
    """
    8 bitlik kapı: dizinin kendisi tek kapı
    Her eleman için 1 bit üretir
    """
    seq = get_gate_sequence(bits, index)
    gate = seq  # 8 bit kapı
    new_bit = transform_bit(bits[index], gate)
    return [new_bit]  # 1 bit

def process_all(bits):
    """
    8 bitlik dizi için 112 bit üret.
    Her eleman: 8 + 4 + 1 + 1 = 14 bit → 8 * 14 = 112 bit
    """
    n = len(bits)
    all_bits = []
    
    for i in range(n):
        b1 = process_1bit_gates(bits, i)   # 8 bit
        b2 = process_2bit_gates(bits, i)   # 4 bit
        b3 = process_6bit_gate(bits, i)    # 1 bit
        b4 = process_8bit_gate(bits, i)    # 1 bit
        all_bits.extend(b1 + b2 + b3 + b4)  # 14 bit
    
    return all_bits  # 112 bit

def bits_to_str(bits):
    return ''.join(map(str, bits))

def int_to_bits(n, length=8):
    return [(n >> (length - 1 - i)) & 1 for i in range(length)]

# 256 farklı dizi için hesapla
results = {}
for i in range(256):
    bits = int_to_bits(i)
    output = process_all(bits)
    results[i] = output

# Örüntü analizi
print("=== 256 dizi için 112 bit çıktı ===\n")

# Benzersiz çıktı sayısı
unique_outputs = set(tuple(v) for v in results.values())
print(f"Benzersiz çıktı sayısı: {len(unique_outputs)} / 256")
print()

# İlk 8 örnek
print("İlk 8 örnek:")
for i in range(8):
    bits = int_to_bits(i)
    out = results[i]
    print(f"{bits_to_str(bits)} -> {bits_to_str(out[:28])}... ({len(out)} bit)")
print()

# Çakışma var mı?
collision = False
output_list = [tuple(v) for v in results.values()]
for i in range(256):
    for j in range(i+1, 256):
        if output_list[i] == output_list[j]:
            print(f"ÇAKIŞMA: {int_to_bits(i)} ve {int_to_bits(j)} aynı çıktıyı üretiyor!")
            collision = True

if not collision:
    print("Çakışma yok! Her giriş benzersiz bir çıktı üretiyor.")

# Hamming mesafesi analizi (yakın girişler çok farklı çıktı üretmeli)
print("\n=== Hamming Mesafesi Analizi ===")
print("1 bit fark eden girişler için çıktıdaki fark:")

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

sample_pairs = [(0,1),(0,2),(0,4),(1,3),(7,15),(127,128),(0,255)]
for a, b in sample_pairs:
    ha = hamming(results[a], results[b])
    print(f"{bits_to_str(int_to_bits(a))} vs {bits_to_str(int_to_bits(b))}: {hamming(int_to_bits(a), int_to_bits(b))} bit fark giriş, {ha} bit fark çıkış ({ha/112*100:.1f}%)")

# Tüm sonuçları dosyaya yaz
with open('eida_results.txt', 'w') as f:
    for i in range(256):
        bits = int_to_bits(i)
        out = results[i]
        f.write(f"{bits_to_str(bits)} -> {bits_to_str(out)}\n")

print("\nTüm sonuçlar eida_results.txt dosyasına yazıldı.")