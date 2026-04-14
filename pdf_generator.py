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
    page_title = "comic"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer título y subtítulo
        category_tag = soup.find('a', rel='category tag')
        subtitle_tag = soup.find('h3', style=re.compile("color: #0363df"))
        
        main_title = category_tag.get_text(strip=True) if category_tag else "Comic"
        sub_title = subtitle_tag.get_text(strip=True) if subtitle_tag else ""
        
        if sub_title:
            page_title = f"{main_title} - {sub_title}"
        else:
            page_title = main_title

        # Limpiar caracteres inválidos para Windows
        page_title = re.sub(r'[\\/*?:"<>|]', "", page_title)

        # Buscar todas las etiquetas <img>
        img_tags = soup.find_all('img')

        images_to_download = []
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if not img_url or 'logo' in img_url.lower():
                continue
            images_to_download.append(img_url)

        cant_imgs = len(images_to_download)
        
        for index, img_url in enumerate(images_to_download):
            if not img_url.startswith("http"):
                img_url = f"{url}/{img_url}"

            try:
                img_data = requests.get(img_url, headers=headers).content
                img_name = f"{index:03d}.png"

                with open(os.path.join(output_dir, img_name), 'wb') as img_file:
                    img_file.write(img_data)
                    print(f"Descargada: {img_name}")

                if progress_callback:
                    progress_callback(index + 1, cant_imgs)
            except Exception as e:
                print(f"Error descargando {img_url}: {e}")
    else:
        raise Exception(f"No se pudo acceder a la página. Código de error: {response.status_code}. Es posible que el sitio esté bloqueando la petición.")



    # Carpeta donde están las imágenes descargadas
    input_dir = "imagenes"
    # Nombre del archivo PDF de salida
    # Limpiamos exceso de espacios
    page_title = page_title.strip()
    pdf_dir = "Comics"
    # Aseguramos que tenga la extensión .pdf
    output_pdf = os.path.join(pdf_dir, f"{page_title}.pdf" if not page_title.lower().endswith(".pdf") else page_title)

    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        print("Carpeta creada")

    image_files = [f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0

    if not image_files:
        raise Exception("No se encontraron imágenes descargadas para generar el PDF.")
    else:
        image_files.sort(key=extract_number)

        # Quitar las últimas 2 imágenes (generalmente publicidad/créditos de la web)
        if len(image_files) > 2:
            image_files = image_files[:-2]
        
        images = []
        for file in image_files:
            filepath = os.path.join(input_dir, file)
            try:
                img = Image.open(filepath)
                # Forzar conversión a RGB para evitar problemas con formatos específicos
                img = img.convert('RGB')
                images.append(img)
            except Exception as e:
                print(f"Error procesando {file}: {e}")

        if images:
            # Guardamos el PDF
            images[0].save(
                output_pdf,
                save_all=True,
                append_images=images[1:],
                quality=95  # Calidad para asegurar que no sea 0 bytes
            )
            print(f"PDF generado exitosamente: {output_pdf}")
            
            # Limpieza solo si se generó correctamente
            for img in images:
                img.close()
            
            try:
                shutil.rmtree(input_dir)
                print(f"Carpeta '{input_dir}' eliminada.")
            except Exception as ex:
                print(f"Error eliminado la carpeta {input_dir}: {ex}")

        else:
            raise Exception("No se pudieron procesar las imágenes tras la descarga.")