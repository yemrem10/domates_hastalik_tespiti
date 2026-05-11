import sqlite3

def setup_db():
    conn = sqlite3.connect('hastaliklar.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bilgiler (
            hastalik_adi TEXT PRIMARY KEY,
            neden TEXT,
            onlem TEXT
        )
    ''')
    
    veriler = [
        ("Erken Yanıklık", "Bu hastalık, genellikle nemli ve sıcak havalarda hızla yayılan Alternaria solani adlı bir mantardan kaynaklanır. Bitki kalıntılarında veya toprakta kışlayan bu sporlar, yağmur ve rüzgar aracılığıyla alt yapraklara sıçrayarak kahverengi, halkalı lekeler oluşturur.", "Bitkiler arasında hava akışını sağlamak için uygun aralıklarla dikim yapılmalı ve sulama işlemi yapraklara su değdirmeden damlama yöntemiyle gerçekleştirilmelidir. Ayrıca, hastalığın döngüsünü kırmak için her yıl farklı ürün ekimi yapılmalı ve bahçe temizliğine özen gösterilmelidir."),
        ("Geç Yanıklık", "Bu hastalık, serin ve yüksek nemli havaları seven Phytophthora infestans isimli bir mikroorganizma nedeniyle oluşur. Özellikle gece ve gündüz arasındaki yüksek sıcaklık farkı ile çiğ oluşumu, sporların yapraklara yerleşip tüm bitkiyi hızla çürütmesine zemin hazırlar.", "Bitkilerin nemli kalmasını önlemek için sabah saatlerinde sulama yapılmalı ve alt yapraklar budanarak hava sirkülasyonu artırılmalıdır. Hastalık belirtileri görülmeden önce bakırlı ilaçlarla koruyucu önlem alınmalı ve hastalıklı bitki artıkları bahçeden tamamen uzaklaştırılmalıdır."),
        ("Yaprak Galeri Sineği", "Bu soruna, ergin sineklerin yaprak dokusunun içine bıraktığı yumurtalardan çıkan larvaların bitki özsuyuyla beslenmesi neden olur. Larvalar yaprağın içinde ilerlerken karakteristik, beyaz renkli ve kavisli tüneller (galeriler) açarak bitkinin fotosentez kapasitesini düşürür.", "Seralarda ve bahçelerde ergin sinekleri yakalamak için sarı yapışkan tuzaklar kullanılmalı ve çevredeki yabancı ot temizliğine dikkat edilmelidir. Ağır bulaşmalarda, larvalara nüfuz edebilen uygun insektisitler tercih edilmeli ve doğal düşmanları korumak adına gereksiz ilaçlamadan kaçınılmalıdır."),
        ("Magnezyum Eksikliği","Magnezyum eksikliği, genellikle asidik (düşük pH) veya aşırı potasyum ve kalsiyum içeren topraklarda magnezyumun bitki tarafından emilememesi sonucunda oluşur. Ayrıca, aşırı yağışlar veya yanlış sulama nedeniyle magnezyumun toprağın alt katmanlarına yıkanması, özellikle yaşlı yapraklarda damar aralarının sararmasına yol açar.","Toprak analizi yapılarak pH seviyesi dengelenmeli ve magnezyum içeren gübreler veya dolomitik kireç uygulaması ile toprak takviye edilmelidir. Belirtiler görüldüğünde, bitkinin hızlı tepki vermesi için magnezyum sülfat (Epsom tuzu) çözeltisiyle yapraktan püskürtme yöntemi uygulanarak eksiklik hızla giderilmelidir."),
        ("Azot Eksikliği", "Topraktaki organik madde miktarının yetersiz olması veya aşırı sulama/yağış nedeniyle azotun yıkanarak kök bölgesinden uzaklaşması bu eksikliğe yol açar. Ayrıca, çok soğuk veya aşırı kuru toprak koşulları köklerin azotu almasını zorlaştırarak bitkinin genelinde soluk yeşil veya sarı bir renk oluşmasına neden olur.", "Dikim öncesinde toprağı iyi yanmış ahır gübresi veya kompostla zenginleştirmek, sezon boyunca ise ihtiyaca göre azotlu gübre takviyesi yapmak gerekir. Bitkinin gelişim dönemlerine uygun bir gübreleme programı izlenmeli ve toprağın azot tutma kapasitesini artırmak için münavebede baklagillere yer verilmelidir."),
        ("Potasyum Eksikliği","Hafif ve kumlu topraklarda potasyumun kolayca yıkanması veya topraktaki aşırı kalsiyum ve magnezyumun potasyum alımını engellemesi bu eksikliğe yol açar. Ayrıca bitkinin meyve bağlama döneminde potasyuma olan ihtiyacının en üst seviyeye çıkması, topraktaki mevcut rezervlerin yetersiz kalmasına neden olabilir.", "Toprak analizi sonuçlarına göre dikim öncesi ve meyve büyüme aşamasında potasyum sülfat veya potasyum nitrat içerikli gübrelerle düzenli takviye yapılmalıdır. Toprağın su tutma kapasitesini artırmak için organik madde ilavesi yapılmalı ve dengeli bir sulama programı uygulanarak mineral alımı kolaylaştırılmalıdır."),
        ("Lekeli Solgunluk Virüsü","Bu hastalık, temel olarak trips adı verilen çok küçük zararlı böceklerin virüsü enfekteli bitkilerden sağlıklı olanlara taşımasıyla meydana gelir. Virüs, tripslerin beslenme faaliyeti sırasında bitki dokusuna bulaşır ve bitkinin iletim demetlerini etkileyerek büyümenin durmasına ve meyvelerde düzensiz halkalar oluşmasına neden olur.","En etkili yöntem, hastalığa karşı dirençli tohum çeşitlerini seçmek ve vektör olan tripslerle sarı/mavi yapışkan tuzaklar veya uygun insektisitler kullanarak mücadele etmektir. Ayrıca tarla çevresindeki konukçu yabancı otlar temizlenmeli ve hastalık belirtisi gösteren bitkiler derhal sökülüp imha edilerek yayılım durdurulmalıdır"),
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO bilgiler VALUES (?, ?, ?)', veriler)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_db()