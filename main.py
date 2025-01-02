import os
import requests
from bs4 import BeautifulSoup

url = "https://readallcomics.com/daring-mystery-comics-2/"

output_dir = "imagenes"
os.makedirs(output_dir, exist_ok=True)

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Buscar todas las etiquetas <img>
    img_tags = soup.find_all('img')
    for index, img_tag in enumerate(img_tags):
        img_url = img_tag.get('src')
        if not img_url or 'logo' in img_url:
            continue

        if not img_url.startswith("http"):
            img_url = f"{url}/{img_url}"

        try:
            img_data = requests.get(img_url).content
            img_name = f"{index}.png"

            with open(os.path.join(output_dir, img_name), 'wb') as img_file:
                img_file.write(img_data)
                print(f"Descargada: {img_name}")
        except Exception as e:
            print(f"Error descargando {img_url}: {e}")
else:
    print(f"Error al acceder a la página: {response.status_code}")