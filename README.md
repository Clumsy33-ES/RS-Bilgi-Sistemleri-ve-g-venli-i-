

[RSÜ_Elif_Sakar_230541088.docx](https://github.com/user-attachments/files/24386462/RSU_Elif_Sakar_230541088.docx)
Proje Amacı
Bu çalışmanın amacı, temel kriptografik prensiplerden karıştırma (confusion) ve yayılma (diffusion) mantığını kullanarak basit ama özgün bir sözde-rastgele sayı üreteci (PRNG) tasarlamak, kodlamak ve üretilen çıktının zayıflıklarını akran kriptanalizi ile incelemektir.
Algoritma, Collatz benzeri bir kurala (çift → /2, tek → 3x+1) dayanır. Her adımda anahtar ile XOR ve ek karıştırma işlemleri uygulanarak çıktıların daha öngörülemez olması hedeflenmiştir. Üretilen sayılar dışarıya doğrudan verilmemiş, bunun yerine çift sayıya 0, tek sayıya 1 olacak şekilde bit dizisi üretilmiştir.

1.1 Tasarım Şartları
Algoritma tipi :Akış tipi üreteç (PRNG / bitstream üreteci)
Her adımda yeni bir iç durum üretilir ve buradan 0/1 çıktısı alınır.
Anahtar Boyutu: Minimum 64-bit anahtar kullanılmıştır.
Anahtar, kullanıcı parolasından türetilmiştir.
Üretim çıkışı(Bit üretimi):
Üretilen iç durum için:
state çift ise 0
state tek ise 1
Bu şekilde çıktı, dışarıya sadece 1 bit sızdıran bir akış haline getirilmiştir.
Kullanılan işlemler:
•	Koşullu dönüşüm: Collatz benzeri adım (çift/tek kontrolü)
•	XOR karıştırma: Anahtar ile karıştırma
•	Permütasyon benzeri yayılma: 64-bit rotasyon (rotate) + XOR
•	Modüler aritmetik: tüm işlemler mod 2^64 sınırında tutulmuştur




Algoritma Adı: CollatzMix-RNG
Collatz kuralı çok basit olmasına rağmen ardışık uygulandığında “karmaşık gibi görünen” bir ilerleme üretebiliyor. Ancak tek başına kriptografik olarak güçlü olmadığı için bu yapıyı anahtar karıştırma (XOR) ve bit yayma (rotasyon + XOR) işlemleriyle destekledim. Buradaki hedef, üretilen bit dizisinin:
•	basit tahminlere karşı daha dirençli olması,
•	anahtar değiştiğinde çıktının belirgin şekilde değişmesi (çığ etkisi),
•	yine de analiz edilebilir düzeyde kalması (kolay-orta zorluk)
olmasıdır.
1.	Kullanıcıdan parola alınır
2.	Parola → 64-bit anahtar türetilir
3.	Seed ile başlangıç state belirlenir
4.	RSÜ kadar döngü:
o	state çift/tek kontrol edilir
o	Collatz dönüşümü uygulanır
o	anahtar ile XOR yapılır
o	rotasyon + XOR ile bitler yayılır
o	mod 2^64 sınırında tutulur
o	state’in tek/çift durumuna göre 0/1 bit çıktısı alınır
5.	Bitler result.csv ye yazılır.
MATEMATİKSEL GÖSTERİM:
Kod:  
  




Test ve Doğrulama:
Aynı seed ve aynı key ile algoritma iki kez çalıştırıldığında aynı bit dizisini üretmektedir. Bu, algoritmanın deterministik bir PRNG olduğunu ve aynı başlangıçla aynı sonuç verdiğini gösterir.
Anahtar hassasiyeti Test 2:
Anahtarın yalnızca 1 biti değiştirildiğinde (ör. key ^ 1), aynı seed ile üretilen bit dizisinin belirgin şekilde değiştiği gözlemlenmiştir. Bu, anahtarın küçük değişikliklere duyarlı olduğunu ve çıktının ciddi şekilde farklılaştığını gösterir.
________________________________________

Kırılma Görevi
Bu aşamada saldırgana sadece:
•	Result.csv (0/1 bit dizisi)
•	RSÜ bilgisi (ör. 300)
•	“çift=0, tek=1” kuralı verilir.
Seed ve key paylaşılmaz. Saldırganın görevi, seçtiği bir yöntemle çıktının zayıflıklarını bulmaya çalışmaktır



Elif Sakar 
230541088
3-B
