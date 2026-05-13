def get_gate_sequence(bits, index):
    n = len(bits)
    if bits[index] == 0:
        return bits[index:] + bits[:index]
    else:
        rev = bits[::-1]
        rev_index = n - 1 - index
        return rev[rev_index:] + rev[:rev_index]

def is_homogeneous(gate):
    return all(b == 0 for b in gate) or all(b == 1 for b in gate)

def is_symmetric_2bit(left, right):
    if left == right and is_homogeneous(left):
        return True
    if left == [0,1] and right == [1,0]:
        return True
    if left == [1,0] and right == [0,1]:
        return True
    return False

def transform_bit(bit, gate):
    if is_homogeneous(gate):
        return bit
    return 1 - bit

def process_1step(bits, index):
    """8 kapı → 8 bit"""
    seq = get_gate_sequence(bits, index)
    n = len(seq)
    return [transform_bit(bits[index], [seq[i], seq[(i+1)%n]]) for i in range(n)]

def process_2step(bits, index):
    """4 kapı → 4 bit"""
    seq = get_gate_sequence(bits, index)
    n = len(seq)
    groups = [[seq[i], seq[(i+1)%n]] for i in range(0, n, 2)]
    result = []
    for i in range(len(groups)):
        left = groups[i]
        right = groups[(i+1)%len(groups)]
        gate = left + right
        if is_symmetric_2bit(left, right):
            result.append(bits[index])
        else:
            result.append(transform_bit(bits[index], gate))
    return result

def process_nstep(bits, index, step, limit=None):
    """n adımlık kapılar, isteğe bağlı limit"""
    seq = get_gate_sequence(bits, index)
    n = len(seq)
    visited = set()
    result = []
    i = 0
    while i not in visited:
        if limit and len(result) >= limit:
            break
        visited.add(i)
        left = [seq[(i+j)%n] for j in range(step)]
        right = [seq[(i+step+j)%n] for j in range(step)]
        gate = left + right
        result.append(transform_bit(bits[index], gate))
        i = (i+step) % n
    return result

def process_all(bits):
    """
    1 adımlık → 8 bit
    2 adımlık → 4 bit
    3 adımlık → 2 kapı → 2 bit  (8 mod 3 = 2)
    4 adımlık → 2 kapı → 2 bit  (8 / 4 = 2)
    Toplam: 8+4+2+2 = 16 bit × 8 eleman = 128 bit
    """
    all_bits = []
    for i in range(len(bits)):
        all_bits.extend(process_1step(bits, i))        # 8 bit
        all_bits.extend(process_2step(bits, i))        # 4 bit
        all_bits.extend(process_nstep(bits, i, 3, 2)) # 2 bit
        all_bits.extend(process_nstep(bits, i, 4, 2)) # 2 bit
    return all_bits  # 128 bit

def bits_to_str(bits):
    return ''.join(map(str, bits))

def int_to_bits(n, length=8):
    return [(n >> (length - 1 - i)) & 1 for i in range(length)]

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

results = {}
for i in range(256):
    results[i] = process_all(int_to_bits(i))

total_bits = len(results[0])
print(f"=== 128 bitlik sistem ===")
print(f"Bit sayısı: {total_bits}")

unique = len(set(tuple(v) for v in results.values()))
print(f"Benzersiz : {unique} / 256")

# Çakışma kontrolü
collision = False
output_list = [tuple(v) for v in results.values()]
for i in range(256):
    for j in range(i+1, 256):
        if output_list[i] == output_list[j]:
            print(f"ÇAKIŞMA: {bits_to_str(int_to_bits(i))} ve {bits_to_str(int_to_bits(j))}")
            collision = True
if not collision:
    print("Çakışma yok! ✓")

# Hamming analizi
one_bit_pairs = [(i,j) for i in range(256) for j in range(i+1,256)
                 if hamming(int_to_bits(i), int_to_bits(j)) == 1]
avg_1bit = sum(hamming(results[i], results[j]) for i,j in one_bit_pairs) / len(one_bit_pairs)
total = sum(hamming(results[i], results[j]) for i in range(256) for j in range(i+1,256))
avg = total / (256*255//2)

print(f"1bit fark : {avg_1bit:.2f} / {total_bits} ({avg_1bit/total_bits*100:.1f}%)")
print(f"Genel ort.: {avg:.2f} / {total_bits} ({avg/total_bits*100:.1f}%)")

with open('eida128_results.txt', 'w') as f:
    for i in range(256):
        f.write(f"{bits_to_str(int_to_bits(i))} -> {bits_to_str(results[i])}\n")
print("\nSonuçlar eida128_results.txt dosyasına yazıldı.")

# Allahım!Beni günahlardan arındır,üzerimden merhameti ve huzuru eksik etme,rızık kaygısı yaşatma
#  Allâhümmeğfirlî verhamnî veâfinî verzügnî