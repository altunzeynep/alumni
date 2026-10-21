# Alumni Tracking System - Data Design (CDD)

## Database Schema
- **Users / Graduates Table**: Stores graduate profile information.
  - `id` (Integer, Primary Key)
  - `full_name` (String)
  - `email` (String, Unique)
  - `graduation_year` (Integer)

  ### `job_postings` (İş İlanları) Tablosu

Mezunların birbirleriyle iş imkanlarını paylaşabilmesi ve kariyer ağını genişletebilmesi için tasarlanan tablo yapısı:

| Sütun Adı | Veri Tipi | Kısıtlamalar / Özellikler | Açıklama |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | İlanın benzersiz kimlik numarası |
| `title` | String(150) | Not Null | İş pozisyonunun unvanı (Örn: Backend Developer) |
| `company` | String(100) | Not Null | İlanı veren şirketin adı |
| `description` | Text | Not Null | İş tanımı, aranan nitelikler ve şartlar |
| `location` | String(100) | Nullable | Çalışma yeri / Lokasyon (Örn: İstanbul / Uzaktan) |
| `contact_email` | String(150) | Not Null | Başvuru için iletişim e-posta adresi |
| `created_at` | DateTime | Default (Current Timestamp) | İlanın sisteme eklendiği tarih ve saat |

#### İlişkiler ve Domain Kuralları:
* Her ilan bir sisteme kaydedilir ve tüm mezunlar tarafından görüntülenebilir.
* İlanlar üzerinden mezunlar arası kariyer desteği ve yönlendirme sağlanması hedeflenir.