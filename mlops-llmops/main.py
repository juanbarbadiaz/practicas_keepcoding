from fastapi import FastAPI, Query
import random

app = FastAPI(
    title="Práctica FastAPI con Hugging Face (Español)",
    description="API con 5 endpoints GET, incluyendo 2 pipelines simulados de NLP en castellano",
    version="1.0.0"
)

# ENDPOINT 1: Ruta de Bienvenida (GET)
@app.get("/", tags=["Básico"])
def read_root():
    """Retorna un mensaje de bienvenida simple para comprobar que la API funciona."""
    return {
        "mensaje": "¡Bienvenido a la API de la práctica!",
        "estado": "Activo",
        "doc_url": "/docs"
    }

# ENDPOINT 2: Saludo Personalizado (GET)
@app.get("/saludo", tags=["Básico"])
def saludar(nombre: str = "Alumno"):
    """Recibe un nombre como parámetro de consulta y devuelve un saludo."""
    return {"saludo": f"¡Hola, {nombre}! Mucho éxito con tu práctica."}

# ENDPOINT 3: Calculadora Sencilla (GET)
@app.get("/sumar", tags=["Herramientas"])
def sumar_numeros(a: float, b: float):
    """Suma dos números recibidos como parámetros y devuelve el resultado."""
    return {
        "numero_a": a,
        "numero_b": b,
        "resultado_suma": a + b
    }

# ENDPOINT 4: Hugging Face - Análisis de Sentimiento (GET)
@app.get("/hf/sentimiento", tags=["Hugging Face"])
def analizar_sentimiento(
    texto: str = Query(..., description="Escribe una frase en español para analizar su sentimiento")
):
    """
    Simula la respuesta de un pipeline de análisis de sentimiento entrenado en español.
    """
    texto_lower = texto.lower()
    
    # Palabras clave positivas en español
    positivas = ["bueno", "bien", "amor", "encanta", "excelente", "genial", "feliz", "increible", "sí", "si", "gusto", "gusta"]
    # Palabras clave negativas en español
    negativas = ["malo", "odio", "triste", "peor", "terrible", "no", "asco", "horroroso", "falla", "mal"]
    
    if any(word in texto_lower for word in positivas):
        label = "POSITIVO"
        score = random.uniform(0.85, 0.99)
    elif any(word in texto_lower for word in negativas):
        label = "NEGATIVO"
        score = random.uniform(0.85, 0.99)
    else:
        label = random.choice(["POSITIVO", "NEGATIVO"])
        score = random.uniform(0.51, 0.84)

    return {
        "texto_analizado": texto,
        "sentimiento": label,
        "confianza_score": round(score, 4)
    }


# ENDPOINT 5: Hugging Face - Clasificación Zero-Shot (GET)
@app.get("/hf/clasificar", tags=["Hugging Face"])
def clasificar_categoria(
    texto: str = Query(..., description="Texto en español a clasificar"),
    categorias: str = Query("deportes, politica, tecnologia, cultura", description="Categorías en español separadas por comas")
):
    """
    Simula la respuesta de un pipeline de clasificación Zero-Shot en español.
    """
    lista_categorias = [cat.strip() for cat in categorias.split(",")]
    
    # Generamos probabilidades aleatorias que sumen 1
    pesos_aleatorios = [random.random() for _ in lista_categorias]
    suma_total = sum(pesos_aleatorios)
    probabilidades = [w / suma_total for w in pesos_aleatorios]
    
    # Ordenamos de mayor a menor probabilidad para emular la salida original de HF
    pares = sorted(zip(lista_categorias, probabilidades), key=lambda x: x[1], reverse=True)
    
    predicciones = {cat: round(prob, 4) for cat, prob in pares}
    categoria_principal = pares[0][0]
    
    return {
        "texto": texto,
        "categoria_principal": categoria_principal,
        "todas_las_probabilidades": predicciones
    }