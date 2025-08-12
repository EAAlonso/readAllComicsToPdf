import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import shutil
import re

def create_pdf(url, progress_callback=None):            
    output_dir = "imagenes"
    cant_imgs = 0
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        page_title = soup.title.string
        # Buscar todas las etiquetas <img>
        img_tags = soup.find_all('img')

        for img_tag in enumerate(img_tags):
                cant_imgs += 1

        cant_imgs -= 1
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

                if progress_callback:
                    progress_callback(index + 1, cant_imgs)
            except Exception as e:
                print(f"Error descargando {img_url}: {e}")
    else:
        print(f"Error al acceder a la página: {response.status_code}")



    # Carpeta donde están las imágenes descargadas
    input_dir = "imagenes"
    # Nombre del archivo PDF de salida
    page_title = page_title.split('|')[0].strip()
    pdf_dir = "Comics"
    output_pdf = os.path.join(pdf_dir,f"{page_title}.pdf")

    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        print("Carpeta creada")

    image_files = [f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0

    if not image_files:
        print("No se encontraron imágenes en la carpeta.")
    else:
        image_files.sort(key=extract_number)

        if len(image_files) > 2:
            image_files = image_files[:-2]
        else:
            print("Hay menos de 3 imágenes; no se quitarán las últimas 2.")
        
        images = []
        for file in image_files:
            filepath = os.path.join(input_dir, file)
            try:
                img = Image.open(filepath)
                img = img.convert('RGB')
                images.append(img)
            except Exception as e:
                print(f"Error procesando {file}: {e}")

        if images:
            images[0].save(
                output_pdf,
                save_all=True,
                append_images=images[1:]
            )
            print(f"PDF generado exitosamente: {output_pdf}")
            try:
                shutil.rmtree(input_dir)
                print(f"Carpeta '{input_dir}' eliminada.")
            except Exception as ex:
                print(f"Error eliminado la carpeta {input_dir}: {e}")

        else:
            print("No se pudieron procesar imágenes para generar el PDF.")