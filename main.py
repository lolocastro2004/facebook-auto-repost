import os
import requests

# Cargar entorno local (solo si estás usando .env)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Variables
LU17_ACCESS_TOKEN = os.getenv("LU17_ACCESS_TOKEN")
TRELEW_ACCESS_TOKEN = os.getenv("TRELEW_ACCESS_TOKEN")
LU17_PAGE_ID = os.getenv("LU17_PAGE_ID")
TRELEW_PAGE_ID = os.getenv("TRELEW_PAGE_ID")

LAST_POST_FILE = "last_post.txt"

# Validación
if not all([LU17_ACCESS_TOKEN, TRELEW_ACCESS_TOKEN, LU17_PAGE_ID, TRELEW_PAGE_ID]):
    print("❌ Faltan variables de entorno.")
    exit(1)

# Leer último post compartido
def get_last_post_id():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r") as f:
            return f.read().strip()
    return None

# Guardar nuevo último post
def set_last_post_id(post_id):
    with open(LAST_POST_FILE, "w") as f:
        f.write(post_id)

# Obtener posts de LU17
url = f"https://graph.facebook.com/v19.0/{LU17_PAGE_ID}/posts?access_token={LU17_ACCESS_TOKEN}"
res = requests.get(url)

if res.status_code != 200:
    print("❌ Error al obtener posts:", res.text)
    exit(1)

posts = res.json().get("data", [])
if not posts:
    print("⚠️ No hay publicaciones en LU17.")
    exit(0)

# Identificar nuevos posts
last_id = get_last_post_id()
new_posts = []

for post in posts:
    if post["id"] == last_id:
        break
    new_posts.append(post)

if not new_posts:
    print("🟡 No hay nuevos posts para compartir.")
    exit(0)

# Publicar en orden cronológico
for post in reversed(new_posts):
    post_id = post["id"]
    link = f"https://www.facebook.com/{post_id}"

    payload = {
        "link": link,
        "access_token": TRELEW_ACCESS_TOKEN
    }

    res_post = requests.post(
        f"https://graph.facebook.com/v19.0/{TRELEW_PAGE_ID}/feed", data=payload)

    if res_post.status_code == 200:
        print(f"✅ Publicado: {link}")
    else:
        print(f"❌ Error al publicar {link}: {res_post.text}")

# Guardar el ID más reciente (solo después de publicar todos)
set_last_post_id(new_posts[0]["id"])
