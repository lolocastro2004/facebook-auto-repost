import os
import requests

# ✅ Cargar variables de entorno desde .env si estás en local
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("📦 .env cargado correctamente.")
except ImportError:
    print("ℹ️ python-dotenv no está instalado, se omite carga local.")

# 🔐 Leer las variables (funciona en GitHub Actions y local)
lu17_access_token = os.getenv("LU17_ACCESS_TOKEN")
trelew_access_token = os.getenv("TRELEW_ACCESS_TOKEN")
lu17_page_id = os.getenv("LU17_PAGE_ID")
trelew_page_id = os.getenv("TRELEW_PAGE_ID")

# ✅ Mostrar resumen de lo cargado
print(f"🧪 LU17_ACCESS_TOKEN: {lu17_access_token[:6]}...{lu17_access_token[-6:]}" if lu17_access_token else "❌ LU17_ACCESS_TOKEN no encontrado")
print(f"🧪 TRELEW_ACCESS_TOKEN: {trelew_access_token[:6]}...{trelew_access_token[-6:]}" if trelew_access_token else "❌ TRELEW_ACCESS_TOKEN no encontrado")
print(f"📄 LU17_PAGE_ID: {lu17_page_id}")
print(f"📄 TRELEW_PAGE_ID: {trelew_page_id}")

# ❗Abortar si falta alguna variable
if not all([lu17_access_token, trelew_access_token, lu17_page_id, trelew_page_id]):
    print("❌ Faltan variables de entorno. Abortando ejecución.")
    exit(1)

# ✅ Obtener el último post de LU17
url_lu17 = f"https://graph.facebook.com/v19.0/{lu17_page_id}/posts?access_token={lu17_access_token}"
response = requests.get(url_lu17)

if response.status_code != 200:
    print("❌ Error al obtener posts:", response.text)
    exit(1)

data = response.json()
posts = data.get("data", [])

if not posts:
    print("⚠️ No se encontraron publicaciones en LU17.")
    exit(0)

# ✅ Tomar el post más reciente
latest_post = posts[0]
post_id = latest_post.get("id")
post_link = f"https://www.facebook.com/{post_id}"
print(f"🆕 Último post de LU17: {post_id}")

# ✅ Publicar como link (para que genere el preview)
url_trelew = f"https://graph.facebook.com/v19.0/{trelew_page_id}/feed"
payload = {
    "link": post_link,
    "access_token": trelew_access_token
}


post_response = requests.post(url_trelew, data=payload)

if post_response.status_code == 200:
    print("✅ Publicación creada correctamente en Trelew Noticias.")
else:
    print("❌ Error al publicar:", post_response.text)

