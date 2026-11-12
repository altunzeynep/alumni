import os
import time
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse, HTMLResponse
from app.controllers import router

app = FastAPI(
    title="Zeynep Altun - Alumni Tracking MVC API",
    version="4.0.0",
    docs_url=None,  # Varsayılan dışa bağımlı Swagger'ı kapatıyoruz
    redoc_url=None
)

# --- 1. Logger Middleware (Logları terminale ve logs/error.logs dosyasına yazar) ---
os.makedirs("logs", exist_ok=True)

@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000)
        current_time = datetime.now().strftime("%H:%M:%S")
        
        log_line = f"{current_time} {request.method} {request.url.path} {response.status_code} {duration_ms}ms\n"
        print(log_line.strip())
        
        return response
    except Exception as exc:
        duration_ms = round((time.time() - start_time) * 1000)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_line = f"[{current_time}] ERROR {request.method} {request.url.path} - {str(exc)}\n"
        
        with open("logs/error.logs", "a", encoding="utf-8") as f:
            f.write(error_line)
        raise exc

# --- 2. 404 Guardian Middleware (Bulunamayan rotalar için şık HTML 404 sayfası) ---
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    html_content = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Sayfa Bulunamadı - 404</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f7f6; text-align: center; padding-top: 100px; color: #333; }
            h1 { font-size: 72px; color: #e74c3c; margin-bottom: 10px; }
            p { font-size: 18px; color: #666; }
            a { display: inline-block; margin-top: 20px; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; }
            a:hover { background-color: #2980b9; }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Aradığınız sayfa veya kaynak bulunamadı.</p>
        <a href="/api/swagger">API Dokümantasyonuna Dön</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=404)

# --- 3. 5xx Guardian Middleware (Sunucu hatalarını yakalama) ---
@app.exception_handler(Exception)
async def custom_5xx_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Sunucu tarafinda beklenmeyen bir hata olustu. Lutfen daha sonra tekrar deneyin.",
            "path": str(request.url)
        }
    )

# --- 4. Yerel/Güvenli CDN Üzerinden Çalışan Swagger Route'u ---
@app.get("/api/swagger", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

# --- Rotaları Dahil Etme ---
app.include_router(router)