İstanbul Üniversitesi Mezun Takip Sistemi

## Alumni Tracking System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)](https://www.docker.com/)

Bu proje, **İstanbul Üniversitesi Web Programlama** dersi kapsamında geliştirilmekte olan **Mezun Takip Sistemi** (*Alumni Tracking System*) için hazırlanmıştır.

Proje; FastAPI altyapısı, katmanlı mimarisi, Docker konteyner desteği, PostgreSQL veritabanı altyapısı ve `/api/swagger` uç noktasıyla tam donanımlı olarak tasarlanmıştır.

---

## 📌 İçindekiler
1. [Proje Hakkında](#proje-hakkında)
2. [Teknoloji Yığını](#teknoloji-yığını)
3. [Proje Dizin Yapısı](#proje-dizin-yapısı)
4. [Uç Noktalar (Endpoints)](#uç-noktalar-endpoints)
5. [Kurulum ve Çalıştırma (Docker)](#kurulum-ve-çalıştırma-docker)

---

## 1. Proje Hakkında
Mezun Takip Sistemi, üniversite mezunları ile öğrenciler arasında köprü kurmayı, kariyer takibi yapmayı ve kurumsal iletişimi güçlendirmeyi hedefler. Platform üzerinden mezunlar profesyonel profillerini güncelleyebilir, güncel öğrenciler ise ağ kurma fırsatlarından yararlanabilir.

## 2. Teknoloji Yığını
* **Backend:** Python, FastAPI, Pydantic, SQLAlchemy
* **Veritabanı:** PostgreSQL 16
* **Konteynerizasyon:** Docker & Docker Compose
* **Dokümantasyon:** Swagger UI (`/api/swagger`)

## 3. Proje Dizin Yapısı
```text
alumni/
├── app/
│   ├── __init__.py
│   └── main.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
4. Uç Noktalar (Endpoints)
GET / - Sistem sağlık ve karşılama kontrolü

GET /hello - Temel selamlama rotası

GET /hello/{name} - Kişiselleştirilmiş selamlama rotası

GET /sum/{a}/{b} - İki sayının matematiksel toplamı

GET /about - Proje manifesto ve bilgi rotası

GET /api/swagger - Swagger UI Dokümantasyonu

GET /api/users - Tüm mezun/kullanıcı kayıtlarını listele

POST /api/users - Yeni kullanıcı kaydı oluştur

PUT /api/users/{id} - Kullanıcı kaydını tamamen güncelle

PATCH /api/users/{id} - Kullanıcı kaydını kısmi (partial) güncelle

DELETE /api/users/{id} - Kullanıcı kaydını sistemden sil

5. Kurulum ve Çalıştırma (Docker)
Projeyi Docker ortamında ayağa kaldırmak için ana dizindeyken şu komutu çalıştırmanız yeterlidir:

Bash
docker-compose up --build
Uygulama ayağa kalktıktan sonra tarayıcınızdan http://localhost:8000/api/swagger adresini ziyaret edebilirsiniz.

## Alumni Tracking System (MVC Architecture)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)](https://www.python.org/)
[![MVC Pattern](https://img.shields.io/badge/Architecture-MVC-blue?style=flat)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)](https://www.docker.com/)

Bu proje, **İstanbul Üniversitesi Web Programlama** dersi kapsamında geliştirilmekte olan **Mezun Takip Sistemi** (*Alumni Tracking System*) için hazırlanmıştır. 

Hafta 4 gereksinimleri doğrultusunda proje **MVC (Model-View-Controller)** mimari desenine refaktör edilmiştir. Kod tabanı modüler katmanlara ayrılmış, sürdürülebilirlik ve ölçeklenebilirlik en üst düzeye çıkarılmıştır.

---

## 📌 İçindekiler
1. [Proje Mimarisi (MVC)](#proje-mimarisi-mvc)
2. [Proje Dizin Yapısı](#proje-dizin-yapısı)
3. [Uç Noktalar (Endpoints)](#uç-noktalar-endpoints)
4. [Kurulum ve Çalıştırma (Docker)](#kurulum-ve-çalıştırma-docker)

---

## 1. Proje Mimarisi (MVC)
* **Model (`app/models.py`):** Veri şemalarını ve doğrulama kurallarını barındırır.
* **Controller (`app/controllers.py`):** İş mantığını (business logic) ve HTTP istek rotalarını yönetir.
* **Database (`app/database.py`):** Veri katmanını soyutlar ve sonraki haftalardaki ORM geçişine zemin hazırlar.

## 2. Proje Dizin Yapısı
```text
alumni/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── controllers.py
│   └── database.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt

## Documentation
- Check out the [Data Design Documentation](./cdd.md) for database schemas and architecture details.



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