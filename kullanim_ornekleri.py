# -*- coding: utf-8 -*-
"""
Türk Ceza Hukuku JSON Veri Seti — Kullanım Örnekleri

Bu dosya, TCK ve CMK JSON dosyalarının Python ile
nasıl kullanılacağını gösteren örnek kodlar içerir.
"""

import json
import os

def veri_yukle(dosya_adi):
    """JSON dosyasını yükler."""
    dosya_yolu = os.path.join(os.path.dirname(__file__), "..", dosya_adi)
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return json.load(f)


def madde_getir(veri, madde_no):
    """Belirli bir maddeyi getirir."""
    anahtar = f"madde_{madde_no}"
    madde = veri["maddeler"].get(anahtar)
    if madde:
        print(f"\n{'='*50}")
        print(f"Madde {madde['madde_no']}: {madde['baslik']}")
        print(f"{'='*50}")
        for fikra_key, fikra_metin in madde["fikralar"].items():
            print(f"  {fikra_key}: {fikra_metin[:100]}...")
    else:
        print(f"Madde {madde_no} bulunamadı.")
    return madde


def suc_ara(veri, suc_adi):
    """Suç terimini arar ve bilgilerini döndürür."""
    terimler = veri.get("suclar", {}).get("terimler", {})
    suc = terimler.get(suc_adi)
    if suc:
        print(f"\nSuç: {suc_adi}")
        print(f"  Kanun: {suc['kanun']} m.{suc['madde']}")
        print(f"  Ceza: {suc['ceza']}")
        print(f"  Kategori: {suc['kategori']}")
    else:
        print(f"'{suc_adi}' terimi bulunamadı.")
    return suc


def kategoriye_gore_listele(veri, kategori):
    """Belirli bir kategorideki tüm suçları listeler."""
    terimler = veri.get("suclar", {}).get("terimler", {})
    sonuclar = {
        k: v for k, v in terimler.items()
        if v.get("kategori") == kategori
    }
    print(f"\nKategori: {kategori} ({len(sonuclar)} suç)")
    print("-" * 40)
    for suc_adi, bilgi in sonuclar.items():
        print(f"  m.{bilgi['madde']:>5} | {suc_adi:<30} | {bilgi['ceza']}")
    return sonuclar


def metin_ara(veri, kelime):
    """Tüm maddelerde kelime arar."""
    sonuclar = []
    for key, madde in veri["maddeler"].items():
        if kelime.lower() in madde["tam_metin"].lower():
            sonuclar.append(madde)
    
    print(f"\n'{kelime}' kelimesi {len(sonuclar)} maddede bulundu:")
    for s in sonuclar:
        print(f"  Madde {s['madde_no']}: {s['baslik']}")
    return sonuclar


def istatistik(veri, kanun_adi):
    """Genel istatistikleri gösterir."""
    madde_sayisi = len(veri["maddeler"])
    
    print(f"\n{'='*50}")
    print(f"{kanun_adi} İstatistikleri")
    print(f"{'='*50}")
    print(f"  Toplam madde sayısı: {madde_sayisi}")
    
    if "suclar" in veri:
        terimler = veri["suclar"]["terimler"]
        kategoriler = veri["suclar"]["kategoriler"]
        print(f"  Toplam suç terimi: {len(terimler)}")
        print(f"  Kategori sayısı: {len(kategoriler)}")
        for kat_adi, kat_bilgi in kategoriler.items():
            suc_sayisi = sum(1 for t in terimler.values() if t["kategori"] == kat_adi)
            print(f"    - {kat_bilgi['ad']}: {suc_sayisi} suç")
    
    if "kurumlar" in veri:
        terimler = veri["kurumlar"]["terimler"]
        kategoriler = veri["kurumlar"]["kategoriler"]
        print(f"  Toplam kavram tanımı: {len(terimler)}")
        print(f"  Kategori sayısı: {len(kategoriler)}")
        for kat_adi in kategoriler:
            kavram_sayisi = sum(1 for t in terimler.values() if t["kategori"] == kat_adi)
            print(f"    - {kat_adi}: {kavram_sayisi} kavram")


if __name__ == "__main__":
    # TCK yükle ve örnekler
    tck = veri_yukle("TCK_5237.json")
    istatistik(tck, "Türk Ceza Kanunu")
    madde_getir(tck, 141)
    suc_ara(tck, "hirsizlik")
    kategoriye_gore_listele(tck, "kisilere_karsi")
    metin_ara(tck, "bilişim")
    
    print("\n" + "=" * 50)
    
    # CMK yükle ve örnekler
    cmk = veri_yukle("CMK_5271.json")
    istatistik(cmk, "Ceza Muhakemesi Kanunu")
    madde_getir(cmk, 100)
