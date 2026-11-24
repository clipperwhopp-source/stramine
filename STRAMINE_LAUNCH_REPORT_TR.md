# STRAMINE — yayın ve doğrulama raporu

**Tarih:** 25 Kasım 2026 (Europe/Istanbul)  
**Canlı site:** https://clipperwhopp-source.github.io/stramine/  
**Türkçe ana sayfa:** https://clipperwhopp-source.github.io/stramine/tr/  
**İngilizce ana sayfa:** https://clipperwhopp-source.github.io/stramine/en/

## Yayın ve kaynak

- **Sağlayıcı:** GitHub Pages, herkese açık `main` dalındaki `/docs` klasörü. Pages ayarı `public: true`, `https_enforced: true`, durum `built` olarak doğrulandı. [GitHub'ın resmî belgesi](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) herkese açık depolar için GitHub Free ile Pages kullanımını doğrular. Bu dağıtımda aylık barındırma ücreti, alan adı satın alımı veya ücretli hizmet yok.
- **Depo:** https://github.com/clipperwhopp-source/stramine
- **Yayımlanan site kodu ve kanıt commit'i:** `0cc109abc85bc6ea90aefad738171b6380dabfe7` (`main`). Bu rapor sonraki belgeleme commit'inde saklanır; statik site çıktısı aynı kalır. Site kodu, gerçek ürün görselleri, ekran görüntüleri ve canlı kontrol kayıtları depoda. Yerel proje: `/Users/askingunduz/Desktop/STRAMINE_OFFICIAL_WEBSITE`.
- Cloudflare Pages hesabı bu oturumda giriş istediği için `stramine.pages.dev` sahipliği doğrulanamadı. Talimattaki ücretsiz ve sürdürülebilir yedek yol olan GitHub Pages seçildi. Mevcut Cloudflare dağıtımlarına yazılmadı.

## Sayfalar ve mağaza bağlantıları

Kök sayfa, iki dilde 27 kanonik sayfa, temiz İngilizce yönlendirme yolları, 404, iletişim, stüdyo, ürün dizini, iki ürün detayı, destek/gizlilik merkezi, uygulama bazlı destek ve politika dizinleri, WallPair hesap silme dizini, sitemap ve robots yayımlandı. Tam liste: [FINAL_ROUTE_MAP.md](FINAL_ROUTE_MAP.md).

| Ürün | STRAMINE ürün sayfası | Doğrulanmış App Store | Google Play |
|---|---|---|---|
| WallPair | [TR](https://clipperwhopp-source.github.io/stramine/tr/apps/wallpair/) · [EN](https://clipperwhopp-source.github.io/stramine/en/apps/wallpair/) | [ID 6790543121](https://apps.apple.com/tr/app/id6790543121), HTTP 200 | Türkiye'den anonim sorguda 404; indirme düğmesi yok |
| Bi Dürüm Usta! | [TR](https://clipperwhopp-source.github.io/stramine/tr/apps/bi-durum-usta/) · [EN](https://clipperwhopp-source.github.io/stramine/en/apps/bi-durum-usta/) | [ID 6832259538](https://apps.apple.com/tr/app/id6832259538), HTTP 200 | Türkiye'den anonim sorguda 404; indirme düğmesi yok |

Google Play Console yönetim durumuna bu oturumda erişilemedi; 404 sonucu küresel yayın durumu iddiası değildir. Sahte Play bağlantısı veya “yakında” tarihi yayımlanmadı.

## Gizlilik, destek ve eski URL güvenliği

| Ürün | STRAMINE gizlilik dizini | STRAMINE destek dizini | Korunan tam politika / resmî destek |
|---|---|---|---|
| WallPair | [Gizlilik](https://clipperwhopp-source.github.io/stramine/tr/privacy/wallpair/) | [Destek](https://clipperwhopp-source.github.io/stramine/tr/support/wallpair/) | [Tam politika](https://clipperwhopp-source.github.io/wallpair-privacy/) · [Destek](https://wallpair.pages.dev/support/) |
| Bi Dürüm Usta! | [Gizlilik](https://clipperwhopp-source.github.io/stramine/tr/privacy/bi-durum-usta/) | [Destek](https://clipperwhopp-source.github.io/stramine/tr/support/bi-durum-usta/) | [Tam politika](https://bi-durum-usta-stramine.clipper-whopp.chatgpt.site/tr/privacy/) · [Destek](https://bi-durum-usta-stramine.clipper-whopp.chatgpt.site/tr/support/) |

İngilizce eşdeğerleri `/en/privacy/{slug}/` ve `/en/support/{slug}/` altında çalışır; oyunun İngilizce tam politika ve desteği mevcut Sites yayınına doğrudan gider. STRAMINE politika yolları **uygulamaya özel dizindir**; onaylı hukuki metin yerine geçmez. Anonim HTTP kontrolünde 27 yeni kanonik sayfa ve önceden 200 olan **23 mevcut URL** yine 200 döndü; sıfır hata. `wallpair.pages.dev/pair`, AASA, `assetlinks.json`, eski politika/destek ve oyun `app-ads.txt` aynen bırakıldı. Kanıt: `reports/live-http-check.json` ve [mevcut varlık denetimi](STRAMINE_EXISTING_WEB_ASSETS_AUDIT.md).

Oyunun 8 Kasım 2026 tarihli mevcut politikasında, 24 Kasım App Store yayınına rağmen “henüz mağazada yayımlanmamıştır” ifadesi kalıyor. Bu hukuki metni sessizce değiştirmedim; sahibi metni gözden geçirip **aynı mevcut politika URL'sinde** düzeltebilir. Canlı uygulama veya mağaza politika alanları değiştirilmedi.

## SEO, erişilebilirlik ve görsel kalite

- Her kanonik sayfada başlık, açıklama, canonical, `en`/`tr`/`x-default` hreflang ve OG/Twitter görseli var. Ürünlerde `SoftwareApplication` veya `VideoGame` JSON-LD kullanıldı. `sitemap.xml` 27 kanonik adres içerir. Çiğ köfte, dürüm, restoran servisi ve özel fotoğraf paylaşımı terimleri yalnız ilgili gerçek ürün içeriğinde kullanıldı; web SEO'su App Store sıralaması garantisi olarak sunulmuyor.
- **Gerçek canlı Lighthouse 13.6.0, mobil Türkçe ana sayfa:** Performans **100**, Erişilebilirlik **100**, İyi Uygulamalar **100**, SEO **100**. Ölçüm `reports/lighthouse-live-tr-mobile.json` içinde; tek koşullu bir laboratuvar sonucudur. FCP 0,9 sn, LCP 0,9 sn, CLS 0. Diğer sayfalar için bu puanlar genellenmez.
- Gerçek tarayıcıda 1280 piksel masaüstü ve 390 piksel telefon genişlikleri kontrol edildi. Ana sayfa, ürünler, dizin, gizlilik ve destek ekran görüntüleri `reports/screenshots/` içindedir. Son canlı ana sayfada yatay taşma yok; Türkçe/İngilizce bağlantı gerçekten tıklanarak doğrulandı. Uygulama görselleri onaylı/App Store kaynaklıdır; [kaynak listesi](ASSET_PROVENANCE.md).
- Güvenlik ve veri minimizasyonu: yalnız statik HTML/CSS ve görseller, çalışma zamanı JavaScript'i/analitik/çerez yok. Kamu deposu özel anahtar veya erişim belirteci için tarandı; bulunmadı. GitHub Pages HTTPS zorunlu. Dış bağlantılar yeni sekmede `noopener noreferrer` kullanır.

## Gelecek uygulama ve bakım

Yeni ürünü `data/apps.json` içine `published: false` olarak ekleyin; onaylı ikon/ekran görüntülerini `docs/assets/` içine koyun, iki dilde ürün ve SEO metinlerini, gerçek mağaza/destek/politika URL'lerini doğrulayın. Yayıma izin verildiğinde `published: true` yapın; `python3 site.py`, `python3 scripts/check_site.py` ve tarayıcı kontrolü ardından `main` dalına push edin. Ayrıntılı [README](README.md) ve [rota haritası](FINAL_ROUTE_MAP.md) depoda. Yayımlanmamış uygulama adları sitede görünmez.

**Yayını tamamlamak için sahibin yapması gereken zorunlu işlem yok.** İsteğe bağlı sonraki işler: tercih edilen `*.pages.dev` adresi için Cloudflare hesabına giriş; oyunun eski politika cümlesinin hukuki inceleme sonrası aynı URL'de düzeltilmesi; Google Play Console yayın durumunun hesap sahibi tarafından teyidi. App Store Connect destek/geliştirici URL alanları bu yayında değiştirilmedi; gerekli görülürse mevcut sürüm akışı ayrı değerlendirilmelidir.
