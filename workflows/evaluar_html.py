import requests
from bs4 import BeautifulSoup

# ----------------------------
# CONFIGURACIÓN
# ----------------------------

urls = {
    "index.html": "https://raw.githubusercontent.com/jbonmun/curso-25-26/main/index.html",
    "miprimerhtml.html": "https://raw.githubusercontent.com/jbonmun/curso-25-26/main/miprimerhtml.html",
    "tabla simple.html": "https://raw.githubusercontent.com/jbonmun/curso-25-26/main/tabla%20simple.html",
    "tablas2.html": "https://raw.githubusercontent.com/jbonmun/curso-25-26/main/tablas2.html"
}

# ----------------------------
# FUNCIONES AUXILIARES
# ----------------------------

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return ""

def count_links(soup):
    return len(soup.find_all("a"))

def has_comments(soup):
    return bool(soup.find_all(string=lambda text: isinstance(text, type(soup.Comment))))

def check_head(soup, filename):
    points = 0
    details = []
    title = soup.title.string if soup.title else ""
    if filename.split(".")[0].lower() in title.lower():
        points += 0.33
        details.append("Título correcto (+0.33)")
    else:
        details.append("Título incorrecto (+0)")

    if soup.find("meta", attrs={"name": "viewport"}):
        points += 0.33
        details.append("Meta viewport presente (+0.33)")
    else:
        details.append("Meta viewport ausente (+0)")

    if soup.find("link", rel="stylesheet"):
        points += 0.33
        details.append("Hoja de estilos CSS vinculada (+0.33)")
    else:
        details.append("Hoja de estilos CSS no vinculada (+0)")

    return min(points, 1), details

def check_paragraph(soup):
    for p in soup.find_all("p"):
        style = p.get("style", "")
        if "text-align:center" in style.replace(" ", "").lower() and "color:" in style.lower():
            return 0.5, "Párrafo centrado y con color (+0.5)"
    return 0, "No hay párrafo centrado y con color (+0)"

def check_basic_elements(soup):
    points = 0
    details = []
    if soup.find_all("pre") and soup.find_all("br") and soup.find_all("hr") and soup.find_all("a"):
        lists = soup.find_all(["ul", "ol"])
        if len(lists) >= 4:
            points = 1
            details.append("Uso correcto de pre, br, hr, enlaces y 4 listas (+1)")
        else:
            details.append("Menos de 4 listas (+0)")
    else:
        details.append("Faltan elementos pre, br, hr o enlaces (+0)")
    return points, details

def check_images(soup):
    if len(soup.find_all("img")) >= 2:
        return 1, "2 o más imágenes presentes (+1)"
    return 0, "Menos de 2 imágenes (+0)"

def check_tables(soup):
    points = 0
    details = []
    tables = soup.find_all("table")
    if tables:
        points += 1
        details.append("Archivo contiene tabla(s) (+1)")
        for t in tables:
            style = t.get("style", "")
            if "border" in style.lower() or t.get("border"):
                points += 0.5
                details.append("Tabla con bordes (+0.5)")
                break
        else:
            details.append("Tablas sin bordes (+0)")
    else:
        details.append("No hay tablas (+0)")
    return points, details

# ----------------------------
# PROCESO PRINCIPAL
# ----------------------------

total_points = 0
reporte = []

for filename, url in urls.items():
    html_content = fetch_html(url)
    if not html_content:
        continue
    soup = BeautifulSoup(html_content, "html.parser")
    
    reporte.append(f"\n--- Evaluando {filename} ---")
    
    # 1. index.html enlaces
    if filename.lower() == "index.html":
        links = count_links(soup)
        if links == 3:
            total_points += 1
            reporte.append("index.html: 3 enlaces (+1)")
        elif links >= 4:
            total_points += 2
            reporte.append(f"index.html: {links} enlaces (+2)")
        else:
            reporte.append(f"index.html: {links} enlaces (+0)")

    # 2. miprimerhtml.html correcto
    if filename.lower() == "miprimerhtml.html":
        total_points += 2
        reporte.append("miprimerhtml.html es correcto (+2)")

    # 3. Comentarios
    if has_comments(soup):
        total_points += 1
        reporte.append("Comentarios presentes (+1)")
    else:
        reporte.append("No hay comentarios (+0)")

    # 4. Cabecera
    points, details = check_head(soup, filename)
    total_points += points
    reporte.extend(details)

    # 5. Párrafo centrado y con color
    points, detail = check_paragraph(soup)
    total_points += points
    reporte.append(detail)

    # 6. Uso de pre, br, hr, enlaces, 4 listas
    points, details = check_basic_elements(soup)
    total_points += points
    reporte.extend(details)

    # 7. 2 imágenes
    points, detail = check_images(soup)
    total_points += points
    reporte.append(detail)

    # 8 y 9. Tablas y bordes (solo archivos de tablas)
    if filename.lower() in ["tabla simple.html", "tablas2.html"]:
        points, details = check_tables(soup)
        total_points += points
        reporte.extend(details)

# ----------------------------
# RESULTADO FINAL
# ----------------------------

reporte.append(f"\nPuntuación total del proyecto: {total_points:.1f} / 10")

# Imprimir el reporte completo
print("\n".join(reporte))
