import requests

# Token y ID de LU17
lu17_access_token = 'EAAI6RTwqos0BPKYJ9DYMLgeZCtZBKQDYy1WhtQec9ZBw5c4E5pQFcOhqcClZCxEr30A8ZBcEuMo4lS88I2RVwOvPfAlTo8ZAUZBKdlJTkLya12TRLg3ZBiuREswe6N2m8ZAneciZBFsewoHmrtAK26jU8xelWOFmLu5eV8b55LZBf5V4Uux6UCcNy78lDnaqtYlmkIJroNu3r5lZBYZBerKoOC39YYZCvwRGoDHYTbCGLmYTsNjwZDZD'
lu17_page_id = '199219160505'

# Token y ID de Trelew Noticias
trelew_access_token = 'EAAI6RTwqos0BPFARCgqWhKWNcxVvOHWNu0xEPNDQZAvHlzEzeN5RmSxSrHJlcjgDjzgwbTzWlRGDU2UvVdIBtkIEjeQlyTDaeZANfRCB6yqE1eZC3NIdwnAlVnAeh3iNzALGLbMSxHdAWDWRwB8edIXeGN9kpbVLb5pM33VeppZCWipzhUB1ZCkTYOGiSOExAJ3gTHJWOlTGq78PzDmSavdI6EVWKD1w2TL2st4rCv67L'
trelew_page_id = '282243145179933'

# Obtener el último post de LU17
get_url = f'https://graph.facebook.com/v19.0/{lu17_page_id}/posts?access_token={lu17_access_token}'
response = requests.get(get_url)

if response.status_code == 200:
    data = response.json()
    posts = data['data']
    if posts:
        post_id = posts[0]['id']
        original_link = f"https://www.facebook.com/{post_id}"

        # Crear post en Trelew Noticias con vista previa enriquecida
        post_url = f"https://graph.facebook.com/v19.0/{trelew_page_id}/feed"
        post_data = {
            'link': original_link,  # CLAVE PARA LA VISTA PREVIA
            'access_token': trelew_access_token
        }

        post_response = requests.post(post_url, data=post_data)
        if post_response.status_code == 200:
            print("✅ Publicación creada correctamente con vista previa enriquecida.")
        else:
            print("❌ Error al publicar:", post_response.text)
    else:
        print("⚠️ No se encontraron publicaciones en LU17.")
else:
    print("❌ Error al obtener posts:", response.text)

