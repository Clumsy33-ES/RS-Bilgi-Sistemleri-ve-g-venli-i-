import hashlib # SHA-256 için paroladan anahtar üretimi için
import csv # Sonuçları CSV dosyasına kaydetmek için

MASK64 = (1 << 64) - 1 # 1 i 64 bit sola kaydır ve 1 çıkar -> 64 bitlik maske oluşturur. 64 tane 1'den oluşur. 64-bit sınırında tutmak için

def rotl64(x: int, r: int) -> int: #x sayısını r bit sola döndürür 64 bitlik sınırda
    r &= 63 # 0-63 arası döndürme
    return ((x << r) & MASK64) | ((x & MASK64) >> (64 - r)) #ilk parantezde sola kaydırma, ikincide ise 64 bitten fazla olan kısmı sağa kaydırma işlemi yapılır.

def Anahtar_Uret(parola: str) -> int: # Paroladan 64-bit anahtar üretir
    h = hashlib.sha256(parola.encode("utf-8")).digest() # SHA-256 ile parolayı hash'ler , byte dizisi döner.ve ilk 8 byte'ı alır
    key = int.from_bytes(h[:8], "little") & MASK64 # İlk 8 byte'ı alır ve little-endian olarak tam sayıya çevirir
     # Anahtar 0 ise sabit bir anahtar kullan
    if key == 0:
        key = 0x9E3779B97F4A7C15  # 64-bit sabit 
    return key

def next_state(state: int, key: int) -> int: # Bir sonraki durumu hesaplar yani yeni rastgele sayı üretir
    x = state & MASK64 
    k = key & MASK64

    # 1) Collatz adımı
    if (x & 1) == 0:          # çift
        x = (x >> 1)          # /2
    else:                      # tek
        x = (3 * x + 1) & MASK64

    # 2) Anahtar karıştırma
    x ^= k # Anahtar ile XOR işlemi yapılır. buda şu şekilde çalışır: x'in bitleri ile k'nin bitleri karşılaştırılır. Eğer iki bit farklıysa sonuç biti 1 olur, aynıysa 0 olur.

    # 3) Yayılma (diffusion) 
    x ^= rotl64(x, 17) # x'i 17 bit sola döndür ve orijinal x ile XOR yap
    x ^= rotl64(x, 41) # x'i 41 bit sola döndür ve orijinal x ile XOR yap
    #bu adımın amacı, bitlerin daha iyi karışmasını sağlamak ve rastgeleliği artırmaktır. yani 2 farklı kaydırma miktarı kullanarak bitlerin birbirine daha fazla etkileşimde bulunmasını sağlar.

    # 4) Ek karıştırma (mod 2^64 çarpma)
    x = (x * 0xD6E8FEB86659FD93) & MASK64 # Büyük bir asal sayı ile çarpma işlemi yapılır. Bu, bitlerin daha da karışmasını sağlar.

    return x

def Bit_Uret(seed: int, key: int, rsu: int) -> list[int]: # Rastgele bitler üretir
    """
    rsu = kaç adet çıktı (bit) üreteceğiz.
    Çift -> 0, Tek -> 1
    """
    bits = []   # Üretilen bitleri saklamak için liste
    s = seed & MASK64 # Başlangıç durumu (seed) 64 bit ile sınırlandırılır
     # Belirtilen sayıda bit üret
    for _ in range(rsu): # rsu kadar döngü 
        s = next_state(s, key) # Yeni durumu hesapla
        bit = 1 if (s & 1) == 1 else 0 # Sonucun tek mi çift mi olduğunu kontrol et.
        bits.append(bit)    # Bit listesini güncelle
    return bits

def bits_to_string(bits: list[int]) -> str: # Bit listesini stringe çevirir.
    return "".join("1" if b else "0" for b in bits) # Bit listesindeki her bir biti '1' veya '0' karakterine çevirir ve birleştirir

def save_csv(bits: list[int], path: str = "results.csv") -> None: # Bit listesini CSV dosyasına kaydeder
    with open(path, "w", newline="", encoding="utf-8") as f: # Dosyayı yazma modunda açar
        w = csv.writer(f) # CSV yazıcı oluşturur
        w.writerow(["index", "bit"])    # Başlık satırı yazar
         # Her bit için indeks ve bit değerini yazar
        for i, b in enumerate(bits): # İndeks ve bit değeri
            w.writerow([i, b]) # İndeks ve bit değerini yazar

def demo(): # Demo fonksiyonu
     # Parametreler
    parola = "elif-123" # Anahtar üretimi için parola
    seed = 123456789 # Başlangıç durumu (seed)
    rsu = 300  # 300 RSÜ = 300 bit örnek

    key = Anahtar_Uret(parola) # Paroladan anahtar üret

    bits = Bit_Uret(seed, key, rsu) # Rastgele bitler üret

    print("Anahtar (hex):", hex(key)) 
    print("RSU:", rsu)
    print("İlk 80 bit:", bits_to_string(bits[:80]))

    save_csv(bits, "results.csv")
    print("results.csv yazıldı.")

if __name__ == "__main__":  
    demo()
