import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from pdf_generator import create_pdf

# Función que actualizará la barra de progreso
def update_progress(current, total):
    progress_bar["value"] = (current / total) * 100
    root.update_idletasks()

def on_generate_pdf():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Advertencia", "Por favor, ingrese una URL válida.")
    else:
        try:
            if not 'readallcomics.com' in url:
                messagebox.showwarning("Advertencia", "Por favor, ingrese una URL válida.")
            else:
                # Configurar barra de progreso
                progress_bar["value"] = 0
                progress_bar["maximum"] = 100
                progress_label.config(text="Generando PDF...")

                # Llamar a la función para crear el PDF y pasar la barra de progreso para actualizarla
                pdf_file = create_pdf(url, progress_callback=update_progress)
                
                # Mensaje de éxito al terminar
                progress_label.config(text=f"PDF generado exitosamente.")
                messagebox.showinfo("Éxito", f"PDF generado exitosamente.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            progress_label.config(text="Error al generar PDF.")

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de PDF de Comics")

# Establecer el tamaño de la ventana
root.geometry("400x200")

# Crear componentes de la GUI
url_label = tk.Label(root, text="Ingresa la URL de la página Readallcomics.com:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

# Barra de progreso
progress_label = tk.Label(root, text="Progreso de la tarea:")
progress_label.pack(pady=5)

progress_bar = Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10)

# Botón para generar el PDF
generate_button = tk.Button(root, text="Generar PDF", command=on_generate_pdf)
generate_button.pack(pady=20)

# Iniciar la aplicación GUI
root.mainloop()