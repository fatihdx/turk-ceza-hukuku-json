# Türk Ceza Hukuku — Yapılandırılmış JSON Veri Seti

Türk Ceza Kanunu (TCK 5237) ve Ceza Muhakemesi Kanunu (CMK 5271) maddelerinin makine tarafından okunabilir, yapılandırılmış JSON formatında açık kaynak veri seti.

## Neden Bu Proje?

Türkiye'de hukuki metinler PDF, HTML veya düz metin olarak yayınlanıyor. Bu formatlar insan tarafından okunabilir ama yazılım tarafından **işlenemez**. Bir NLP modeli eğitmek, istatistik çıkarmak, filtreleme yapmak veya otomatik analiz geliştirmek istediğinizde bu metinleri önce yapılandırmanız gerekiyor.

Bu proje o adımı sizin yerinize yapar.

## İçerik

| Dosya | Kanun | Madde | Ek Veri |
|-------|-------|-------|---------|
| `TCK_5237.json` | Türk Ceza Kanunu | 344 madde | 161 suç terimi, 5 suç kategorisi |
| `CMK_5271.json` | Ceza Muhakemesi Kanunu | 344 madde | 50 kurum/kavram tanımı, 6 ana kategori |

## Veri Yapısı

### TCK — Madde Örneği

```json
{
  "madde_no": 2,
  "baslik": "Suçta ve cezada kanunîlik ilkesi",
  "tam_metin": "...",
  "fikralar": {
    "fikra_1": "Kanunun açıkça suç saymadığı bir fiil için...",
    "fikra_2": "İdarenin düzenleyici işlemleriyle suç ve ceza konulamaz.",
    "fikra_3": "...kıyas yapılamaz..."
  }
}
```

### TCK — Suç Terimi Örneği

```json
{
  "soykirim": {
    "kanun": "TCK",
    "madde": "76",
    "ceza": "Ağırlaştırılmış müebbet hapis",
    "kategori": "uluslararasi_suclar"
  }
}
```

### TCK — Suç Kategorileri

| Kategori | Açıklama | Madde Aralığı |
|----------|----------|---------------|
| `uluslararasi_suclar` | Uluslararası Suçlar | 76-80 |
| `kisilere_karsi` | Kişilere Karşı Suçlar | 81-169 |
| `mala_karsi` | Mala Karşı Suçlar | — |
| `topluma_karsi` | Topluma Karşı Suçlar | — |
| `millete_devlete_karsi` | Millete ve Devlete Karşı Suçlar | — |

### CMK — Madde Örneği

```json
{
  "madde_no": 1,
  "madde_tipi": "...",
  "baslik": "...",
  "tam_metin": "...",
  "fikralar": { ... },
  "kitap": "Birinci Kitap",
  "kisim": "...",
  "bolum": "..."
}
```

### CMK — Kavram Tanımı Örneği

```json
{
  "supheli": {
    "kanun": "CMK",
    "madde": "2/1-a",
    "tanim": "Soruşturma evresinde, suç şüphesi altında bulunan kişi",
    "kategori": "yargilama_sujeleri"
  }
}
```

### CMK — Kavram Kategorileri

| Kategori | Açıklama |
|----------|----------|
| `yargilama_sujeleri` | Şüpheli, sanık, müdafi, Cumhuriyet savcısı vb. |
| `koruma_tedbirleri` | Yakalama, gözaltı, tutuklama, arama, elkoyma vb. |
| `deliller` | İspat, tanıklık, bilirkişi, keşif vb. |
| `sorusturma` | Soruşturma evresi, kolluk, iddianame vb. |
| `kovusturma` | Duruşma, hüküm, uzlaşma, basit yargılama vb. |
| `kanun_yollari` | İstinaf, temyiz, yargılamanın yenilenmesi vb. |

## Kullanım Örnekleri (Python)

### Belirli bir maddeyi getirme

```python
import json

with open("TCK_5237.json", "r", encoding="utf-8") as f:
    tck = json.load(f)

madde = tck["maddeler"]["madde_141"]
print(f"Madde {madde['madde_no']}: {madde['baslik']}")
```

### Bir suç teriminin cezasını bulma

```python
suc = tck["suclar"]["terimler"]["hirsizlik"]
print(f"Kanun: {suc['kanun']} Madde: {suc['madde']}")
print(f"Ceza: {suc['ceza']}")
print(f"Kategori: {suc['kategori']}")
```

### CMK'da belirli bir kavramı arama

```python
with open("CMK_5271.json", "r", encoding="utf-8") as f:
    cmk = json.load(f)

kavram = cmk["kurumlar"]["terimler"]["tutuklama"]
print(f"Tanım: {kavram['tanim']}")
print(f"Dayanak: {kavram['kanun']} m.{kavram['madde']}")
```

### Tüm suçları kategoriye göre filtreleme

```python
terimler = tck["suclar"]["terimler"]

kisilere_karsi = {
    k: v for k, v in terimler.items()
    if v["kategori"] == "kisilere_karsi"
}

print(f"Kişilere karşı suç sayısı: {len(kisilere_karsi)}")
for suc_adi, bilgi in list(kisilere_karsi.items())[:5]:
    print(f"  - {suc_adi}: m.{bilgi['madde']} → {bilgi['ceza']}")
```

### Kelime arama (tüm maddelerde)

```python
aranan = "bilişim"
sonuclar = []

for key, madde in tck["maddeler"].items():
    if aranan.lower() in madde["tam_metin"].lower():
        sonuclar.append(madde)

print(f'"{aranan}" geçen madde sayısı: {len(sonuclar)}')
for s in sonuclar:
    print(f"  Madde {s['madde_no']}: {s['baslik']}")
```

## Olası Kullanım Alanları

- **NLP model eğitimi** — Türkçe hukuki metin sınıflandırma, varlık tanıma (NER), soru-cevap
- **Hukuk araştırması** — Madde bazlı istatistik, ceza karşılaştırma, kavram analizi
- **Chatbot / asistan** — Hukuki soru-cevap sistemleri için bilgi tabanı
- **Eğitim** — Hukuk fakültesi öğrencileri ve stajyer avukatlar için referans
- **Otomasyon** — Belge şablonlarında madde referansı otomatik doldurma

## Veri Kaynağı ve Lisans

Kanun metinleri [Resmi Gazete](https://www.resmigazete.gov.tr/) ve [mevzuat.gov.tr](https://www.mevzuat.gov.tr/) üzerinden kamuya açık olarak yayınlanmaktadır. Bu veri seti, kamuya açık mevzuat metinlerinin yapılandırılmış halidir.

Proje MIT Lisansı ile lisanslanmıştır — serbestçe kullanabilir, değiştirebilir ve dağıtabilirsiniz.

## Katkıda Bulunma

Katkılarınızı bekliyoruz:

- Eksik veya hatalı madde bildirimi (Issue açın)
- Yeni kanunların JSON formatında eklenmesi (Pull Request gönderin)
- Kullanım örnekleri ve entegrasyon rehberleri

## Yol Haritası

- [ ] Türk Borçlar Kanunu (TBK 6098) eklenmesi
- [ ] Türk Medeni Kanunu (TMK 4721) eklenmesi
- [ ] Kabahatler Kanunu (KK 5326) eklenmesi
- [ ] JSON Schema doğrulama dosyası
- [ ] Madde değişiklik geçmişi (tarihçe)
- [ ] REST API ile erişim (opsiyonel)

---

**Bu proje, Türk hukuk sisteminin dijitalleşmesine katkı sağlamak amacıyla geliştirilmektedir.**
