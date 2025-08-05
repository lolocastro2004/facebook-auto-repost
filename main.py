import os
import requests

# Cargar .env si estás en local
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("📦 .env cargado (modo local)")
except:
    pass

# Leer variables de entorno
LU17_ACCESS_TOKEN = os.getenv("LU17_ACCESS_TOKEN")
TRELEW_ACCESS_TOKEN = os.getenv("TRELEW_ACCESS_TOKEN")
LU17_PAGE_ID = os.getenv("LU17_PAGE_ID")
TRELEW_PAGE_ID = os.getenv("TRELEW_PAGE_ID")

# Validar
if not all([LU17_ACCESS_TOKEN, TRELEW_ACCESS_TOKEN, LU17_PAGE_ID, TRELEW_PAGE_ID]):
    print("❌ Faltan variables de entorno.")
    exit(1)

# Archivo para guardar el último post compartido
LAST_POST_FILE = "last_post.txt"

def get_last_shared_post_id():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_shared_post_id(post_id):
    with open(LAST_POST_FILE, "w") as f:
        f.write(post_id)

# Obtener posts de LU17
url = f"https://graph.facebook.com/v19.0/{LU17_PAGE_ID}/posts?access_token={LU17_ACCESS_TOKEN}"
response = requests.get(url)

if response.status_code != 200:
    print("❌ Error al obtener posts:", response.text)
    exit(1)

posts = response.json().get("data", [])
if not posts:
    print("⚠️ No hay publicaciones en LU17.")
    exit(0)

# Comparar con el último compartido
last_shared_id = get_last_shared_post_id()
new_posts = []

for post in posts:
    if post["id"] == last_shared_id:
        break
    new_posts.append(post)

if not new_posts:
    print("🟡 No hay publicaciones nuevas para compartir.")
    exit(0)

# Publicar de más antiguas a más nuevas
for post in reversed(new_posts):
    post_id = post["id"]
    link = f"https://www.facebook.com/{post_id}"
    
    payload = {
        "link": link,
        "access_token": TRELEW_ACCESS_TOKEN
    }

    post_url = f"https://graph.facebook.com/v19.0/{TRELEW_PAGE_ID}/feed"
    res = requests.post(post_url, data=payload)

    if res.status_code == 200:
        print(f"✅ Publicado: {link}")
        save_last_shared_post_id(post_id)
    else:
        print(f"❌ Error publicando {link} → {res.text}")
