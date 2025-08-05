import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde el entorno de ejecución o archivo .env
load_dotenv()

LU17_ACCESS_TOKEN = os.getenv("LU17_ACCESS_TOKEN")
TRELEW_ACCESS_TOKEN = os.getenv("TRELEW_ACCESS_TOKEN")
LU17_PAGE_ID = os.getenv("LU17_PAGE_ID")
TRELEW_PAGE_ID = os.getenv("TRELEW_PAGE_ID")
POSTED_FILE = "last_posts.txt"

# Validar
if not all([LU17_ACCESS_TOKEN, TRELEW_ACCESS_TOKEN, LU17_PAGE_ID, TRELEW_PAGE_ID]):
    print("❌ Faltan variables de entorno.")
    exit(1)

# Cargar IDs ya compartidos
def load_posted_ids():
    if not os.path.exists(POSTED_FILE):
        print("📄 Archivo last_posts.txt no existe, se usará una lista vacía.")
        return set()
    try:
        with open(POSTED_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except Exception as e:
        print(f"⚠️ Error al leer {POSTED_FILE}: {e}")
        return set()

# Guardar nuevos IDs compartidos
def save_posted_ids(ids):
    try:
        with open(POSTED_FILE, "a") as f:
            for pid in ids:
                f.write(pid + "\n")
    except Exception as e:
        print(f"⚠️ Error al guardar IDs en {POSTED_FILE}: {e}")

# Obtener posts desde LU17
def get_lu17_posts():
    url = f"https://graph.facebook.com/v19.0/{LU17_PAGE_ID}/posts?access_token={LU17_ACCESS_TOKEN}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("data", [])
    else:
        print("❌ Error al obtener posts:", res.text)
        return []

# Publicar en Trelew Noticias
def publish_to_trelew(post_id):
    original_url = f"https://www.facebook.com/{post_id}"
    post_url = f"https://graph.facebook.com/v19.0/{TRELEW_PAGE_ID}/feed"
    res = requests.post(post_url, data={"link": original_url, "access_token": TRELEW_ACCESS_TOKEN})
    if res.status_code == 200:
        print(f"✅ Publicado correctamente con link: {original_url}")
        return True
    else:
        print(f"❌ Error al publicar {post_id}:", res.text)
        return False

# Lógica principal
def main():
    publicados = load_posted_ids()
    nuevos = []
    for post in get_lu17_posts():
        pid = post["id"]
        if pid not in publicados:
            if publish_to_trelew(pid):
                nuevos.append(pid)

    if nuevos:
        save_posted_ids(nuevos)
        print(f"📥 {len(nuevos)} nuevas publicaciones compartidas.")
    else:
        print("📟 No hay publicaciones nuevas.")

if __name__ == "__main__":
    main()
