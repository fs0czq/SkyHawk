# 🔎 SkyHawk — Network & Port Scanner

<p align="center">
  <b>SkyHawk</b> — yerel ağlarda cihaz keşfi ve port taraması yapmak için geliştirilmiş, hafif ve çoklu iş parçacıklı (multi-threaded) bir Python aracıdır.  
  Hızlı tarama, port → servis eşleştirmesi ve opsiyonel web servis doğrulaması sunar.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/status-active-success" alt="Status">
</p>

## ✨ Özellikler

* 🚀 Çoklu iş parçacığı ile hızlandırılmış port tarama (`ThreadPoolExecutor`)
* 🌐 ARP tabanlı cihaz keşfi (Scapy)
* 🌎 HTTP/HTTPS servis doğrulama (requests)
* 🎨 Renkli ve okunabilir CLI çıktıları (`colorama`)
* 📝 Tüm sonuçların `scan_results.log` dosyasına kaydedilmesi
* ⚙️ Basit CLI argüman desteği ve yapılandırılabilir tarama parametreleri

---

## ⚙️ Kurulum

1. Depoyu klonlayın:

```
git clone https://github.com/fs0czq/SkyHawk.git
cd SkyHawk
```

2. (Önerilir) Sanal ortam oluşturun ve aktif edin:

```
python3 -m venv .venv
source .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate       # Windows
```

3. Gerekli paketleri yükleyin:

```
pip install -r requirements.txt
```

## 🚀 Kullanım (Detaylı)

SkyHawk komut satırından çalıştırılır. ARP taraması ve ham socket işlemleri nedeniyle **root / admin** yetkisi gerektirir.

### Temel kullanım

```
sudo python3 skyhawk.py
```

(Betiğin varsayılan hedefi: sistem gateway adresi üzerinden `/24` IP aralığı.)

### Tüm argüman örneği

```
sudo python3 skyhawk.py --target 192.168.1.0/24 --timeout 3 --threads 150
```

### Argümanlar

| Argüman          | Açıklama                                                                      |
| ---------------- | ----------------------------------------------------------------------------- |
| `--target`       | Taranacak IP aralığı. Ör: `192.168.1.0/24`. Varsayılan: sistem gateway `/24`. |
| `--timeout`      | Port tarama socket zaman aşımı (saniye). Varsayılan: `2`.                     |
| `--threads`      | Maksimum paralel thread sayısı (tarama hızı). Varsayılan: `100`.              |
| `--no-web-check` | HTTP/HTTPS servis doğrulamasını devre dışı bırakır (tarama hızlanır).         |

### Platform örnekleri

#### Linux (örnek)

Root ile çalıştırın:

```
sudo python3 skyhawk.py --target 10.0.0.0/24 --timeout 2 --threads 200
```

#### Windows (örnek)

CMD veya PowerShell’i **Yönetici** olarak açın:

```
python skyhawk.py --target 192.168.0.0/24
```

---

## ⚡ Performans İpuçları

* Büyük ağlarda (`/16` vb.) tarama yaparken `--threads` sayısını dikkatli artırın; ağ trafiği/cihaz yükünü göz önünde bulundurun.
* `--timeout` değerini çok düşük tutmak yanlış negatiflere neden olabilir; 1.5–3s arası güvenli bir aralıktır.
* `--no-web-check` kullanmak, HTTP/HTTPS ek kontrollerini atlayarak taramayı hızlandırır.

---

## 🛡️ Etik & Yasal Uyarı

Bu araç ağ keşfi ve servis tespiti amaçlıdır. Yetkiniz olmayan ağlarda tarama yapmak yasa dışıdır ve cezai sorumluluk doğurabilir. Projeyi **sadece** izniniz olan ağlarda kullanın. Yasal sorumluluk kullanıcıya aittir.
