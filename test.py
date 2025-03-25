from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap

import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def create_pdf_with_text(output_pdf_path, data):
    # Crear el PDF
    pdf_canvas = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4

    # Definir márgenes
    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50
    max_text_width = width - left_margin - right_margin

    # Función para verificar si necesitamos una nueva página
    def check_page_space(y_position, line_height=14):
        if y_position < bottom_margin + line_height:  # Si estamos cerca del final de la página
            pdf_canvas.showPage()
            pdf_canvas.setFont("Helvetica", 10)  # Reiniciar la fuente después de nueva página
            return height - top_margin  # Resetear y_position en la nueva página
        return y_position

    # Título principal
    pdf_canvas.setFont("Helvetica-Bold", 24)
    pdf_canvas.drawCentredString(width / 2, height - top_margin, data.get("name", "NOMBRE COMPLETO"))

    # Información de contacto
    pdf_canvas.setFont("Helvetica", 10)
    pdf_canvas.drawString(left_margin, height - top_margin - 30, data.get("location", "Ubicación"))
    pdf_canvas.drawRightString(width - right_margin, height - top_margin - 30, data.get("phone", "Teléfono"))
    pdf_canvas.drawRightString(width - right_margin, height - top_margin - 45, data.get("email", "Correo electrónico"))
    pdf_canvas.drawRightString(width - right_margin, height - top_margin - 60, data.get("website", "Sitio web"))
    pdf_canvas.drawString(left_margin, height - top_margin - 55, data.get("github", "GitHub"))

# Sección de Experiencia
    y_position = height - top_margin - 90
    pdf_canvas.setFont("Helvetica-Bold", 13)
    pdf_canvas.drawString(left_margin, y_position, "EXPERIENCIA")
    pdf_canvas.line(left_margin, y_position - 5, width - right_margin, y_position - 5)
    y_position -= 25

    pdf_canvas.setFont("Helvetica", 10)
    for job in data.get("employment", []):
        y_position = check_page_space(y_position)
        pdf_canvas.setFont("Helvetica-Bold", 12)
        combined_text = f"{job['position']} - {job['company']}"
        pdf_canvas.drawString(left_margin, y_position, combined_text)
        pdf_canvas.drawRightString(width - right_margin, y_position, job["dates"])

        y_position -= 15
        text_object = pdf_canvas.beginText(left_margin + 10, y_position)  # Indentación de la descripción
        text_object.setFont("Helvetica", 10)
        text_object.setLeading(14)
        for line in job["details"]:
            wrapped_lines = wrap(line, width=int(max_text_width / 5))  # Ajustar el divisor aquí
            for wrapped_line in wrapped_lines:
                text_object.textLine(wrapped_line)
                y_position -= 14
                y_position = check_page_space(y_position)
        pdf_canvas.drawText(text_object)
        y_position -= 10


    # Sección de Proyectos
    y_position -= 10
    y_position = check_page_space(y_position)
    pdf_canvas.setFont("Helvetica-Bold", 13)
    pdf_canvas.drawString(left_margin, y_position, "PROYECTOS")
    pdf_canvas.line(left_margin, y_position - 5, width - right_margin, y_position - 5)
    y_position -= 25

    for project in data.get("projects", []):
        y_position = check_page_space(y_position)

        # Título del proyecto en negrita
        pdf_canvas.setFont("Helvetica-Bold", 12)
        pdf_canvas.drawString(left_margin, y_position, project['title'])
        y_position -= 15

        # Descripción del proyecto como una lista de puntos
        pdf_canvas.setFont("Helvetica", 10)
        for description in project["description"]:
            wrapped_lines = wrap(description, width=int(max_text_width / 5))  # Ajustar el divisor aquí
            for wrapped_line in wrapped_lines:
                pdf_canvas.drawString(left_margin + 10, y_position, f"{wrapped_line}")
                y_position -= 14
                y_position = check_page_space(y_position)
        y_position -= 5

        # Tecnologías utilizadas con ajuste automático
        pdf_canvas.setFont("Helvetica-Bold", 10)
        utilized_text = f"Tecnologías: {', '.join(project['technologies'])}"

        wrapped_utilized = wrap(utilized_text, width=int(max_text_width / 5))  # Ajustar el divisor aquí
        for line in wrapped_utilized:
            pdf_canvas.drawString(left_margin + 10, y_position, line)
            y_position -= 12
            y_position = check_page_space(y_position)

        y_position -= 15

    # Sección de Habilidades
    y_position -= 10
    y_position = check_page_space(y_position)
    pdf_canvas.setFont("Helvetica-Bold", 13)
    pdf_canvas.drawString(left_margin, y_position, "SKILLS")
    pdf_canvas.line(left_margin, y_position - 5, width - right_margin, y_position - 5)
    y_position -= 20

    # Ajustar las habilidades para que se dividan en líneas si es necesario
    pdf_canvas.setFont("Helvetica", 11)
    skills_text = ", ".join(data.get("skills", []))
    wrapped_skills = wrap(skills_text, width=int(max_text_width / 5))  # Ajustar el divisor aquí
    for line in wrapped_skills:
        pdf_canvas.drawString(left_margin, y_position, line)
        y_position -= 14
        y_position = check_page_space(y_position)

    # Guardar el PDF
    pdf_canvas.save()

# Ejemplo de uso con JSON
output_pdf_path = "output_final_adjusted_projects_skills.pdf"

create_pdf_with_text(output_pdf_path, data)
