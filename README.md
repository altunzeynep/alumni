# İstanbul Üniversitesi Mezun Takip Sistemi

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