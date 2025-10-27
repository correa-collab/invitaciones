"""
Generador de imágenes de pase de acceso en el backend
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import os

class PassGenerator:
    def __init__(self):
        self.width = 600
        self.height = 400
        # Colores UP
        self.gold_color = (184, 134, 11)  # #B8860B
        self.dark_gold = (218, 165, 32)  # #DAA520
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (128, 128, 128)
        
    def generate_pass_image(self, name: str, folio: str, companions: int = 0, whatsapp: str = "") -> str:
        """
        Genera la imagen del pase de acceso IDÉNTICA a la de la web
        """
        try:
            # Configuración idéntica a la web
            img_width = 711
            img_height = 950
            
            # Crear imagen con fondo blanco
            img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            # Borde dorado
            border_width = 8
            border_color = (218, 165, 32)  # Dorado
            draw.rectangle([0, 0, img_width-1, img_height-1], outline=border_color, width=border_width)
            
            # Fuentes (intentar cargar fuentes del sistema)
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                event_title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 28)
                data_title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 26)
                data_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
                qr_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
                footer_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                # Fallback
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                event_title_font = ImageFont.load_default()
                data_title_font = ImageFont.load_default()
                data_font = ImageFont.load_default()
                qr_font = ImageFont.load_default()
                footer_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Colores
            gold_color = (218, 165, 32)
            black_color = (0, 0, 0)
            green_color = (34, 197, 94)
            gray_color = (128, 128, 128)
            
            y_pos = 60
            
            # Título principal
            title = "PASE DE ACCESO"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((img_width - title_width) // 2, y_pos), title, fill=gold_color, font=title_font)
            y_pos += 60
            
            # Subtítulo
            subtitle = "Posgrado en TIC's"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            draw.text(((img_width - subtitle_width) // 2, y_pos), subtitle, fill=gold_color, font=subtitle_font)
            y_pos += 80
            
            # Información del evento
            event_title = "Fiesta de Finalización del Posgrado"
            event_bbox = draw.textbbox((0, 0), event_title, font=event_title_font)
            event_width = event_bbox[2] - event_bbox[0]
            draw.text(((img_width - event_width) // 2, y_pos), event_title, fill=gold_color, font=event_title_font)
            y_pos += 50
            
            # Fecha del evento
            date_text = "📅 Viernes 14 noviembre 2025"
            date_bbox = draw.textbbox((0, 0), date_text, font=data_font)
            date_width = date_bbox[2] - date_bbox[0]
            draw.text(((img_width - date_width) // 2, y_pos), date_text, fill=black_color, font=data_font)
            y_pos += 40
            
            # Hora del evento
            time_text = "🕐 17:00 hrs"
            time_bbox = draw.textbbox((0, 0), time_text, font=data_font)
            time_width = time_bbox[2] - time_bbox[0]
            draw.text(((img_width - time_width) // 2, y_pos), time_text, fill=black_color, font=data_font)
            y_pos += 60
            
            # Línea separadora
            line_margin = 100
            draw.line([(line_margin, y_pos), (img_width - line_margin, y_pos)], fill=gold_color, width=3)
            y_pos += 40
            
            # Título de datos de confirmación
            data_title = "DATOS DE CONFIRMACIÓN"
            data_title_bbox = draw.textbbox((0, 0), data_title, font=data_title_font)
            data_title_width = data_title_bbox[2] - data_title_bbox[0]
            draw.text(((img_width - data_title_width) // 2, y_pos), data_title, fill=gold_color, font=data_title_font)
            y_pos += 60
            
            # Datos del invitado (alineados a la izquierda)
            left_margin = 120
            line_spacing = 35
            
            # Folio
            folio_text = f"📋 Folio: {folio}"
            draw.text((left_margin, y_pos), folio_text, fill=black_color, font=data_font)
            y_pos += line_spacing
            
            # Nombre
            name_text = f"👤 Nombre: {name}"
            draw.text((left_margin, y_pos), name_text, fill=black_color, font=data_font)
            y_pos += line_spacing
            
            # Asistencia
            attendance_text = "✅ Asistencia: SÍ ASISTIRÉ"
            draw.text((left_margin, y_pos), attendance_text, fill=green_color, font=data_font)
            y_pos += line_spacing
            
            # Acompañantes
            companions_text = f"👥 Acompañantes: {companions}"
            draw.text((left_margin, y_pos), companions_text, fill=black_color, font=data_font)
            y_pos += line_spacing
            
            # WhatsApp
            if whatsapp:
                whatsapp_text = f"📱 WhatsApp: {whatsapp}"
                draw.text((left_margin, y_pos), whatsapp_text, fill=black_color, font=data_font)
                y_pos += line_spacing
            
            # Fecha de confirmación
            confirmed_text = f"🕐 Confirmado: {datetime.now().strftime('%d/%m/%Y %H:%M')} p.m."
            draw.text((left_margin, y_pos), confirmed_text, fill=gray_color, font=data_font)
            y_pos += 60
            
            # Simulación de QR Code (rectángulo negro con texto)
            qr_size = 120
            qr_x = (img_width - qr_size) // 2
            qr_y = y_pos
            
            # Dibujar un rectángulo negro simulando QR
            draw.rectangle([qr_x, qr_y, qr_x + qr_size, qr_y + qr_size], fill=black_color, outline=black_color)
            
            # Agregar algunos cuadrados blancos dentro para simular QR
            for i in range(3):
                for j in range(3):
                    if (i + j) % 2 == 0:
                        square_size = 15
                        square_x = qr_x + 20 + (i * 25)
                        square_y = qr_y + 20 + (j * 25)
                        draw.rectangle([square_x, square_y, square_x + square_size, square_y + square_size], 
                                     fill=(255, 255, 255))
            
            y_pos += qr_size + 20
            
            # Texto del QR
            qr_title = "Código QR de Acceso"
            qr_title_bbox = draw.textbbox((0, 0), qr_title, font=qr_font)
            qr_title_width = qr_title_bbox[2] - qr_title_bbox[0]
            draw.text(((img_width - qr_title_width) // 2, y_pos), qr_title, fill=black_color, font=qr_font)
            y_pos += 30
            
            # Folio del QR
            qr_folio = f"Folio: {folio}"
            qr_folio_bbox = draw.textbbox((0, 0), qr_folio, font=small_font)
            qr_folio_width = qr_folio_bbox[2] - qr_folio_bbox[0]
            draw.text(((img_width - qr_folio_width) // 2, y_pos), qr_folio, fill=gray_color, font=small_font)
            y_pos += 25
            
            # Texto de escaneo
            scan_text = "Escanea para ver confirmación online"
            scan_bbox = draw.textbbox((0, 0), scan_text, font=small_font)
            scan_width = scan_bbox[2] - scan_bbox[0]
            draw.text(((img_width - scan_width) // 2, y_pos), scan_text, fill=gray_color, font=small_font)
            y_pos += 50
            
            # Footer principal
            footer_main = "👑 PRESENTA ESTE PASE EN EL EVENTO"
            footer_bbox = draw.textbbox((0, 0), footer_main, font=footer_font)
            footer_width = footer_bbox[2] - footer_bbox[0]
            draw.text(((img_width - footer_width) // 2, y_pos), footer_main, fill=gold_color, font=footer_font)
            y_pos += 50
            
            # Footer secundario
            footer_secondary = "Sistema desarrollado por IUX - Software Jurídico"
            footer_sec_bbox = draw.textbbox((0, 0), footer_secondary, font=small_font)
            footer_sec_width = footer_sec_bbox[2] - footer_sec_bbox[0]
            draw.text(((img_width - footer_sec_width) // 2, y_pos), footer_secondary, fill=gray_color, font=small_font)
            
            # Convertir a base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Crear string base64
            img_base64 = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
            
            return img_base64
            
        except Exception as e:
            print(f"Error generando imagen del pase: {str(e)}")
            return None

# Instancia global
pass_generator = PassGenerator()