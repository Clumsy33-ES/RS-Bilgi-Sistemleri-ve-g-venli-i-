

[RSÜ_Elif_Sakar_230541088.docx](https://github.com/user-attachments/files/24386462/RSU_Elif_Sakar_230541088.docx)

CollatzMix-RNG
Kriptografik Sayı Üreteci (PRNG) – Tasarım, Uygulama ve Analiz

Elif Sakar
230541088
3-B

Proje Amacı

Bu çalışmanın amacı, temel kriptografik prensiplerden karıştırma (confusion) ve yayılma (diffusion) mantığını kullanarak basit ama özgün bir sözde-rastgele sayı üreteci (PRNG) tasarlamak, kodlamak ve üretilen çıktının zayıflıklarını akran kriptanalizi ile incelemektir.

Algoritma, Collatz benzeri bir kurala (çift → /2, tek → 3x+1) dayanır. Her adımda anahtar ile XOR ve ek karıştırma işlemleri uygulanarak çıktıların daha öngörülemez olması hedeflenmiştir. Üretilen sayılar dışarıya doğrudan verilmemiş, bunun yerine çift sayıya 0, tek sayıya 1 olacak şekilde bit dizisi üretilmiştir.

Algoritma Adı

CollatzMix-RNG

1. Tasarım Şartları
Algoritma Tipi

Akış tipi üreteç (PRNG / bitstream üreteci)
Her adımda yeni bir iç durum (state) üretilir ve buradan 0/1 çıktısı alınır.

Anahtar Boyutu

Minimum 64-bit anahtar kullanılmıştır.

Anahtar, kullanıcı parolasından türetilmiştir.

Üretim Çıkışı (Bit Üretimi)

Üretilen iç durum için:

State çift ise → 0

State tek ise → 1

Bu sayede dışarıya yalnızca 1 bitlik bilgi sızdıran bir çıktı akışı elde edilmiştir.

Kullanılan Temel İşlemler

Koşullu dönüşüm: Collatz benzeri adım (çift/tek kontrolü)

XOR karıştırma: Anahtar ile XOR işlemi

Permütasyon benzeri yayılma: 64-bit rotasyon (rotate) + XOR

Modüler aritmetik: Tüm işlemler mod 2⁶⁴ sınırında tutulmuştur

Tasarım Gerekçesi ve Felsefesi

Collatz kuralı basit bir matematiksel yapı olmasına rağmen ardışık uygulandığında karmaşık gibi görünen bir davranış sergiler. Ancak tek başına kriptografik olarak güçlü değildir. Bu nedenle algoritma;

anahtar karıştırma (XOR),

bit yayma (rotasyon + XOR),

modüler sınırlandırma

işlemleri ile desteklenmiştir.

Bu tasarım ile amaçlanan:

basit tahminlere karşı daha dirençli bir yapı oluşturmak,

anahtar değiştiğinde çıktının belirgin şekilde değişmesini sağlamak (çığ etkisi),

yine de analiz edilebilir, kolay–orta zorlukta bir algoritma elde etmektir.

Algoritmanın Çalışma Akışı

Kullanıcıdan parola alınır

Paroladan 64-bit anahtar türetilir

Seed ile başlangıç state belirlenir

RSÜ kadar döngü çalıştırılır:

state çift/tek kontrol edilir

Collatz dönüşümü uygulanır

anahtar ile XOR yapılır

rotasyon + XOR ile bitler yayılır

değer mod 2⁶⁴ sınırında tutulur

state’in tek/çift durumuna göre 0/1 bit üretilir

Üretilen bitler results.csv dosyasına yazılır

Matematiksel Gösterim

𝑥
0
x
0
	​

: başlangıç durumu (seed)

𝐾
K: 64-bit anahtar

Tüm işlemler 
 
m
o
d
 
2
64
mod2
64

Durum Güncelleme:
𝑥
𝑛
′
=
{
𝑥
𝑛
2
,
	
𝑥
𝑛
 
c
¸
ift ise


3
𝑥
𝑛
+
1
,
	
𝑥
𝑛
 tek ise
x
n
′
	​

={
2
x
n
	​

	​

,
3x
n
	​

+1,
	​

x
n
	​

 
c
¸
	​

ift ise
x
n
	​

 tek ise
	​

Anahtar Karıştırma:
𝑥
𝑛
′
′
=
𝑥
𝑛
′
⊕
𝐾
x
n
′′
	​

=x
n
′
	​

⊕K
Yayılma:
𝑥
𝑛
′
′
′
=
𝑥
𝑛
′
′
⊕
ROTL
(
𝑥
𝑛
′
′
,
17
)
⊕
ROTL
(
𝑥
𝑛
′
′
,
41
)
x
n
′′′
	​

=x
n
′′
	​

⊕ROTL(x
n
′′
	​

,17)⊕ROTL(x
n
′′
	​

,41)
Son Durum:
𝑥
𝑛
+
1
=
(
𝑥
𝑛
′
′
′
×
𝐶
)
 
m
o
d
 
2
64
x
n+1
	​

=(x
n
′′′
	​

×C)mod2
64
Bit Çıkışı:
𝑏
𝑛
=
{
0
,
	
𝑥
𝑛
+
1
 
c
¸
ift ise


1
,
	
𝑥
𝑛
+
1
 tek ise
b
n
	​

={
0,
1,
	​

x
n+1
	​

 
c
¸
	​

ift ise
x
n+1
	​

 tek ise
	​

Test ve Doğrulama
Test 1 – Deterministiklik

Aynı seed ve aynı anahtar ile algoritma iki kez çalıştırıldığında aynı bit dizisi üretilmiştir. Bu durum algoritmanın deterministik bir PRNG olduğunu göstermektedir.

Test 2 – Anahtar Hassasiyeti (Çığ Etkisi)

Anahtarın yalnızca 1 biti değiştirildiğinde (key ^ 1), aynı seed ile üretilen bit dizisinin belirgin şekilde değiştiği gözlemlenmiştir. Bu, algoritmanın anahtar değişimlerine duyarlı olduğunu göstermektedir.

Kırılma Görevi (Kriptanaliz)

Bu aşamada saldırgana yalnızca aşağıdaki bilgiler verilmiştir:

results.csv (0/1 bit dizisi)

RSÜ bilgisi (örneğin 300)

“çift = 0, tek = 1” kuralı

Seed ve anahtar paylaşılmamıştır.
Saldırganın görevi, yalnızca çıktı üzerinden algoritmanın zayıflıklarını analiz etmektir.

Sonuç

Bu çalışmada Collatz tabanlı bir matematiksel dönüşüm üzerine anahtar karıştırma ve bit yayma işlemleri eklenerek özgün bir PRNG tasarlanmıştır. Algoritma eğitim amaçlı olup, hem üretim hem de kırılma (analiz) aşamalarının anlaşılmasına uygun bir yapı sunmaktadır.
