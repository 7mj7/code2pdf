#!/usr/bin/env python3
# code2pdf.py - Convierte código fuente a PDF con resaltado de sintaxis

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class Code2PDF:
    def __init__(self, output_file="codigo_proyecto.pdf", title=None):
        self.output_file = output_file
        self.title = title or "Documentación de Código"
        self.story = []
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        self.base_directory = None  # Se establecerá al escanear
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        # Estilo para código
        self.code_style = ParagraphStyle(
            'CodeStyle',
            parent=self.styles['Code'],
            fontSize=7,
            leftIndent=10,
            fontName='Courier',
            textColor=colors.HexColor('#2b2b2b'),
            backColor=colors.HexColor('#f5f5f5')
        )
        
        # Estilo para títulos de archivo
        self.file_title_style = ParagraphStyle(
            'FileTitle',
            parent=self.styles['Heading2'],
            fontSize=10,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=6
        )
        
    def get_file_extensions(self):
        """Retorna las extensiones de archivo a incluir"""
        return {
            # Lenguajes de programación
            '.java', '.py', '.js', '.ts', '.cpp', '.c', '.h', '.cs', '.php',
            '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r', '.m',
            
            # Scripts y configuración
            '.sh', '.bash', '.bat', '.ps1', '.cmd',
            
            # Markup y documentación
            '.md', '.txt', '.rst', '.adoc',
            
            # Configuración y datos
            '.xml', '.json', '.yml', '.yaml', '.toml', '.ini', '.env',
            '.properties', '.conf', '.config',
            
            # Web
            '.html', '.css', '.scss', '.sass', '.less',
            
            # SQL
            '.sql',
            
            # Otros
            '.dockerfile', '.gitignore', '.editorconfig'
        }
    
    def should_include_file(self, file_path):
        """Determina si un archivo debe ser incluido"""
        file_name = file_path.name.lower()
        
        # Incluir README sin importar la extensión
        if file_name.startswith('readme'):
            return True
        
        # Incluir LICENSE
        if file_name in ['license', 'license.txt', 'license.md']:
            return True
            
        # Incluir Dockerfile
        if file_name == 'dockerfile':
            return True
            
        # Incluir Makefile
        if file_name in ['makefile', 'makefile.am']:
            return True
            
        # Verificar extensiones
        return file_path.suffix.lower() in self.get_file_extensions()
    
    def add_title_page(self):
        """Añade una página de título"""
        self.story.append(Spacer(1, 2*inch))
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=TA_CENTER
        )
        
        self.story.append(Paragraph(self.title, title_style))
        self.story.append(Spacer(1, 0.5*inch))
        
        date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER
        )
        
        current_date = datetime.now().strftime("%d de %B de %Y")
        self.story.append(Paragraph(f"Generado el {current_date}", date_style))
        
        # Añadir información del directorio
        dir_style = ParagraphStyle(
            'DirStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        )
        
        if self.base_directory:
            self.story.append(Spacer(1, 0.2*inch))
            self.story.append(Paragraph(f"Directorio: {self.base_directory}", dir_style))
        
        self.story.append(PageBreak())
    
    def add_table_of_contents(self, files):
        """Añade una tabla de contenidos"""
        self.story.append(Paragraph("Tabla de Contenidos", self.styles['Heading1']))
        self.story.append(Spacer(1, 0.2*inch))
        
        toc_data = [["Archivo", "Ruta"]]
        
        for file_path in files:
            try:
                # Obtener ruta relativa de forma segura
                if self.base_directory:
                    rel_path = file_path.relative_to(self.base_directory)
                    parent_dir = str(rel_path.parent) if str(rel_path.parent) != '.' else 'Raíz'
                else:
                    parent_dir = str(file_path.parent)
                
                toc_data.append([file_path.name, parent_dir])
            except ValueError:
                # Si no se puede obtener ruta relativa, usar absoluta
                toc_data.append([file_path.name, str(file_path.parent)])
        
        # Limitar la tabla a las primeras 50 entradas
        if len(toc_data) > 51:
            toc_data = toc_data[:51]
            toc_data.append(["...", f"y {len(files)-50} archivos más"])
        
        table = Table(toc_data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        self.story.append(table)
        self.story.append(PageBreak())
    
    def process_file(self, file_path):
        """Procesa un archivo individual"""
        print(f"  → Procesando: {file_path.name}")
        
        # Obtener ruta relativa de forma segura
        try:
            if self.base_directory:
                relative_path = file_path.relative_to(self.base_directory)
            else:
                relative_path = file_path.name
        except ValueError:
            relative_path = file_path.name
        
        # Añadir título del archivo
        self.story.append(Paragraph(f"<b>📄 {relative_path}</b>", self.file_title_style))
        self.story.append(Spacer(1, 0.1*inch))
        
        try:
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except (UnicodeDecodeError, UnicodeError):
                    continue
            
            if content is None:
                # Si ningún encoding funciona, leer como binario y decodificar con errores='ignore'
                with open(file_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
            
            # Limitar el contenido para archivos muy grandes
            lines = content.split('\n')
            max_lines = 500  # Máximo de líneas por archivo
            
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                lines.append(f"\n... [Archivo truncado - mostrando primeras {max_lines} líneas] ...")
            
            # Formatear contenido
            formatted_content = '\n'.join(lines)
            
            # Limitar caracteres totales
            max_chars = 50000
            if len(formatted_content) > max_chars:
                formatted_content = formatted_content[:max_chars] + "\n... [Contenido truncado] ..."
            
            # Escapar caracteres especiales para ReportLab
            formatted_content = formatted_content.replace('&', '&amp;')
            formatted_content = formatted_content.replace('<', '&lt;')
            formatted_content = formatted_content.replace('>', '&gt;')
            
            # Añadir contenido como texto preformateado
            pre = Preformatted(formatted_content, self.code_style, maxLineLength=100)
            self.story.append(pre)
            
        except Exception as e:
            error_style = ParagraphStyle(
                'ErrorStyle',
                parent=self.styles['Normal'],
                textColor=colors.red,
                fontSize=8
            )
            self.story.append(Paragraph(f"⚠️ Error leyendo archivo: {str(e)}", error_style))
        
        self.story.append(PageBreak())
    
    def scan_directory(self, directory, ignore_dirs=None):
        """Escanea el directorio y retorna los archivos a procesar"""
        if ignore_dirs is None:
            ignore_dirs = {'.git', '__pycache__', 'node_modules', 'target', 
                          'build', 'dist', '.idea', '.vscode', 'venv', 
                          'env', '.env', 'bin', 'obj', '.pytest_cache',
                          '.mypy_cache', 'coverage', '.coverage'}
        
        files_to_process = []
        
        # Convertir directorio a Path absoluto
        base_path = Path(directory).resolve()
        self.base_directory = base_path
        
        for root, dirs, files in os.walk(base_path):
            # Filtrar directorios a ignorar
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
            
            for file in sorted(files):
                # Crear Path absoluto del archivo
                file_path = Path(root).resolve() / file
                
                if self.should_include_file(file_path):
                    files_to_process.append(file_path)
        
        return files_to_process
    
    def generate_pdf(self, directory="."):
        """Genera el PDF completo"""
        print(f"\n🔍 Escaneando directorio: {os.path.abspath(directory)}")
        
        # Escanear archivos
        files = self.scan_directory(directory)
        
        if not files:
            print("❌ No se encontraron archivos de código para procesar")
            return False
        
        print(f"📊 Encontrados {len(files)} archivos para procesar\n")
        
        # Crear documento
        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Añadir página de título
        self.add_title_page()
        
        # Añadir tabla de contenidos si hay muchos archivos
        if len(files) > 5:
            self.add_table_of_contents(files)
        
        # Procesar cada archivo
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}]", end=" ")
            try:
                self.process_file(file_path)
            except Exception as e:
                print(f"\n  ⚠️ Error procesando {file_path.name}: {str(e)}")
                continue
        
        # Generar PDF
        try:
            doc.build(self.story)
            print(f"\n✅ PDF generado exitosamente: {self.output_file}")
            print(f"📁 Ubicación: {os.path.abspath(self.output_file)}")
            print(f"📄 Total de archivos procesados: {len(files)}")
            return True
        except Exception as e:
            print(f"\n❌ Error generando PDF: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Convierte código fuente a PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  code2pdf                           # Genera codigo_proyecto.pdf en el directorio actual
  code2pdf -o mi_codigo.pdf          # Especifica nombre del archivo de salida
  code2pdf -d C:\\mi_proyecto         # Escanea un directorio específico
  code2pdf -t "Mi Proyecto v1.0"     # Añade un título personalizado
        """
    )
    
    parser.add_argument('-o', '--output', 
                       default='codigo_proyecto.pdf',
                       help='Nombre del archivo PDF de salida')
    
    parser.add_argument('-d', '--directory',
                       default='.',
                       help='Directorio a escanear (por defecto: directorio actual)')
    
    parser.add_argument('-t', '--title',
                       help='Título para la página de portada')
    
    args = parser.parse_args()
    
    # Crear instancia y generar PDF
    converter = Code2PDF(args.output, args.title)
    success = converter.generate_pdf(args.directory)
    
    # Retornar código de salida apropiado
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
