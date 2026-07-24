# Code2PDF

**Code2PDF** es una herramienta en Python diseñada para escanear directorios de proyectos de software y compilar los archivos de código fuente, scripts y archivos de configuración en un único archivo PDF formateado y estructurado.

---

## 🚀 Características

- **Página de portada personalizada:** Incluye el título del proyecto, la fecha de generación y la ruta del directorio analizado.
- **Tabla de contenidos (TOC):** Genera automáticamente una tabla de contenidos cuando el proyecto contiene más de 5 archivos.
- **Soporte multilingüe y de extensiones:** Detecta y procesa automáticamente una gran variedad de formatos:
  - **Lenguajes de programación:** Python, Java, JavaScript, TypeScript, C, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala, R, etc.
  - **Web:** HTML, CSS, SCSS, SASS, LESS.
  - **Configuración y datos:** JSON, YAML, TOML, XML, INI, ENV, SQL.
  - **Documentación y scripts:** Markdown, TXT, Bash (`.sh`), Batch (`.bat`), PowerShell (`.ps1`), Dockerfile, Makefile, etc.
- **Exclusión inteligente:** Ignora automáticamente carpetas de entorno, dependencias y control de versiones como `.git`, `node_modules`, `venv`, `__pycache__`, `dist`, `build`, etc.
- **Manejo robusto de codificación:** Intenta múltiples codificaciones (`utf-8`, `latin-1`, `cp1252`, etc.) para prevenir errores al leer archivos.
- **Protección de tamaño:** Trunca suavemente archivos extremadamente grandes para mantener la legibilidad y un tamaño aceptable en el archivo PDF de salida.

---

## 📋 Requisitos Previos

- **Python 3.6+**
- Biblioteca **ReportLab** para la generación de documentos PDF.

### Instalación de dependencias

```bash
pip install reportlab
```

---

## 🛠️ Uso

### Ejecución directa con Python

```bash
python code2pdf.py [opciones]
```

### Ejecución en Windows (usando el archivo Batch)

Si estás en Windows, puedes ejecutar directamente:

```cmd
code2pdf.bat [opciones]
```

---

## ⚙️ Parámetros de la Línea de Comandos

| Parámetro | Opción corta | Descripción | Valor por defecto |
| :--- | :--- | :--- | :--- |
| `--output` | `-o` | Nombre del archivo PDF de salida | `codigo_proyecto.pdf` |
| `--directory` | `-d` | Ruta del directorio a escanear | `.` (Directorio actual) |
| `--title` | `-t` | Título para la portada del PDF | `"Documentación de Código"` |

---

## 💡 Ejemplos de Uso

1. **Generar PDF con los parámetros por defecto:**
   ```bash
   python code2pdf.py
   ```

2. **Especificar nombre de salida:**
   ```bash
   python code2pdf.py -o mi_proyecto_codigo.pdf
   ```

3. **Escanear un directorio específico y añadir un título personalizado:**
   ```bash
   python code2pdf.py -d C:\proyectos\mi_app -t "Mi Proyecto v1.0" -o doc_mi_app.pdf
   ```

---

## 📂 Estructura del Proyecto

```text
code2pdf/
├── code2pdf.py    # Script principal en Python
├── code2pdf.bat   # Script ejecutable para consola de Windows
└── README.md      # Documentación del proyecto
```

---

## 📄 Licencia

Este proyecto está disponible para su libre uso y modificación.
