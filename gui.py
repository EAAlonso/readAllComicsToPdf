import tkinter as tk
from tkinter import messagebox
from pdf_generator import create_pdf

def on_generate_pdf():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Advertencia", "Por favor, ingrese una URL válida.")
    else:
        try:
            # Llamar a la función para crear el PDF
            pdf_file = create_pdf(url)
            messagebox.showinfo("Éxito", f"PDF generado exitosamente.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("ReadAllComics to PDF")

# Establecer el tamaño de la ventana
root.geometry("400x200")

# Crear componentes de la GUI
url_label = tk.Label(root, text="Ingresa la URL de la página:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generar PDF", command=on_generate_pdf)
generate_button.pack(pady=20)

# Iniciar la aplicación GUI
root.mainloop()