# -*- coding: utf-8 -*-
"""Entrega final_chatbot FHLEO.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-4cQ6IlEPQV6fyzbxjIE9CmcLYoN2I-G
"""

# Instalación de librerías necesarias
!pip install openai twilio

import openai
import json

# Configuración de credenciales OpenAI
openai.api_key = "TU_API_KEY_OPENAI"

# Base de datos de preguntas frecuentes
preguntas_frecuentes = {
    "inscripcion_materias": """
    Los alumnos deberán inscribirse a las materias a través del portal de servicios https://servicios.usal.edu.ar
    o de forma personal en la sede. La inscripción se realiza en marzo y julio.
    Requisitos:
    - Estar al día con aranceles
    - Haber presentado toda la documentación requerida
    - No tener materias con superposición horaria
    - Primer año: la inscripción la realiza la Secretaría Administrativa
    """,

    "faltas_permitidas": """
    Los alumnos deben cumplir con el 75% de asistencia.
    Cantidad de faltas según horas semanales:
    - 2 horas semanales (anual): 4 faltas
    - 3 horas semanales (anual): 6 faltas
    - 3 horas semanales (cuatrimestral): 3 faltas
    - 4 horas semanales (anual): 8 faltas
    - 5 horas semanales (anual): 10 faltas
    - 6 horas semanales (anual): 12 faltas
    """,

    "prorroga_final": """
    Para solicitar prórroga para rendir un final con escolaridad vencida:
    1. Solicitar formulario en Secretaría Administrativa (abril)
    2. Pedir al docente un tema de evaluación
    3. Si apruebas la evaluación, quedas habilitado
    4. Entregar formulario en Secretaría
    Plazo máximo: 24 meses desde finalización del cursado
    """,

    "inscripcion_finales": """
    Inscripción a exámenes finales:
    - Por web en servicios.usal.edu.ar
    - Hasta 72 hs hábiles antes del examen
    - Requiere:
      * 75% de asistencia
      * Parciales aprobados
      * Materias correlativas aprobadas
      * Pagos al día
    Turnos: Julio, Noviembre/Diciembre, Febrero/Marzo
    """,

    "final_sin_titulo_secundario": """
    Para rendir en turno Julio sin título secundario:
    1. Enviar mail a fhleo@usal.edu.ar
    2. Asunto: Solicitar Excepción para rendir final
    3. Adjuntar:
       - Formulario de solicitud
       - Foto/escaneo de certificado de título en trámite
    Plazo límite: 18 de Junio
    """
}

def generar_respuesta_ia(pregunta):
    """
    Genera respuesta usando GPT para preguntas no cubiertas directamente
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente de la Universidad del Salvador especializado en responder preguntas de estudiantes de la Facultad de Filosofía, Historia, Letras y Estudios Orientales."},
                {"role": "user", "content": pregunta}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Lo siento, hubo un error: {str(e)}"

def chatbot_usal(mensaje):
    """
    Función principal del chatbot
    """
    mensaje = mensaje.lower()

    # Mapeo de palabras clave a respuestas
    mapeo = {
        "materias": "inscripcion_materias",
        "inscripción": "inscripcion_materias",
        "faltas": "faltas_permitidas",
        "inasistencias": "faltas_permitidas",
        "prórroga": "prorroga_final",
        "final vencido": "prorroga_final",
        "exámenes": "inscripcion_finales",
        "finales": "inscripcion_finales",
        "título secundario": "final_sin_titulo_secundario"
    }

    # Buscar respuesta en mapeo de preguntas
    for palabra, categoria in mapeo.items():
        if palabra in mensaje:
            return preguntas_frecuentes[categoria]

    # Si no encuentra respuesta directa, usar IA
    return generar_respuesta_ia(mensaje)

# Ejemplo de uso
print(chatbot_usal("¿Cómo me inscribo a materias?"))
print(chatbot_usal("Cuántas faltas puedo tener"))