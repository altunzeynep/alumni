from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from app.controllers import router

app = FastAPI(
    title="Zeynep Altun - Alumni Tracking MVC API",
    version="4.0.0",
    docs_url=None,  # Varsayılanı kapatıyoruz, özel route ekleyeceğiz
    redoc_url=None
)

# Yerel CDN üzerinden çalışan güvenli Swagger route'u
@app.get("/api/swagger", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

app.include_router(router)