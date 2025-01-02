import os
import requests
from bs4 import BeautifulSoup
from PIL import Image

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



# Carpeta donde están las imágenes descargadas
input_dir = "imagenes"
# Nombre del archivo PDF de salida
output_pdf = "imagenes.pdf"

# Listar los archivos de imagen en la carpeta
image_files = [f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Verificar si hay imágenes
if not image_files:
    print("No se encontraron imágenes en la carpeta.")
else:
    # Ordenar las imágenes por nombre (opcional)
    image_files.sort()
    
    # Abrir las imágenes
    images = []
    for file in image_files:
        filepath = os.path.join(input_dir, file)
        try:
            img = Image.open(filepath)
            # Convertir a modo RGB (necesario para PDF)
            img = img.convert('RGB')
            images.append(img)
        except Exception as e:
            print(f"Error procesando {file}: {e}")

    if images:
        # Guardar todas las imágenes en un único archivo PDF
        images[0].save(
            output_pdf,
            save_all=True,
            append_images=images[1:]  # Las demás páginas
        )
        print(f"PDF generado exitosamente: {output_pdf}")
    else:
        print("No se pudieron procesar imágenes para generar el PDF.")