from flask import Flask, render_template, jsonify
import math
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

def draw_half_koch_snowflake_exact():
    # Configuración de matplotlib para dibujar
    fig = Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)
    
    # Función recursiva para calcular puntos de la curva de Koch (completa)
    def koch_curve_points(p1, p2, depth):
        if depth == 0:
            return [p1, p2]
        
        # Dividir el segmento en 3 partes
        dx = (p2[0] - p1[0]) / 3
        dy = (p2[1] - p1[1]) / 3
        
        a = (p1[0] + dx, p1[1] + dy)
        c = (p1[0] + 2*dx, p1[1] + 2*dy)
        
        # Calcular el punto b (vértice del triángulo equilátero)
        angle = math.radians(60)
        b = (
            a[0] + dx * math.cos(angle) - dy * math.sin(angle),
            a[1] + dx * math.sin(angle) + dy * math.cos(angle)
        )
        
        # Llamadas recursivas para los 4 segmentos
        return (koch_curve_points(p1, a, depth-1)[:-1] + 
                koch_curve_points(a, b, depth-1)[:-1] + 
                koch_curve_points(b, c, depth-1)[:-1] + 
                koch_curve_points(c, p2, depth-1))
    
    # Función recursiva para calcular puntos de la curva de Koch (parcial)
    def koch_curve_partial_points(p1, p2, depth, p):
        if p <= 0:
            return []
        if depth == 0:
            return [p1, (p1[0] + (p2[0]-p1[0])*p, p1[1] + (p2[1]-p1[1])*p)]
        
        # Dividir el segmento en 3 partes
        dx = (p2[0] - p1[0]) / 3
        dy = (p2[1] - p1[1]) / 3
        
        a = (p1[0] + dx, p1[1] + dy)
        c = (p1[0] + 2*dx, p1[1] + 2*dy)
        
        # Calcular el punto b (vértice del triángulo equilátero)
        angle = math.radians(60)
        b = (
            a[0] + dx * math.cos(angle) - dy * math.sin(angle),
            a[1] + dx * math.sin(angle) + dy * math.cos(angle)
        )
        
        # Cada curva de Koch se compone de 4 subcurvas con exactamente 1/4 del perímetro
        parts = [max(0.0, min(1.0, p*4 - i)) for i in range(4)]
        
        points = []
        
        # 1ª subcurva
        if parts[0] > 0:
            points.extend(koch_curve_partial_points(p1, a, depth-1, parts[0])[:-1])
        
        # 2ª subcurva
        if parts[1] > 0:
            points.extend(koch_curve_partial_points(a, b, depth-1, parts[1])[:-1])
        
        # 3ª subcurva
        if parts[2] > 0:
            points.extend(koch_curve_partial_points(b, c, depth-1, parts[2])[:-1])
        
        # 4ª subcurva
        if parts[3] > 0:
            points.extend(koch_curve_partial_points(c, p2, depth-1, parts[3]))
        
        return points
    
    # Parámetros
    side = 300
    depth = 4
    h = side * math.sqrt(3) / 2
    
    # Puntos iniciales para el triángulo
    start = (-side/2, -h/3)
    top = (0, 2*h/3)
    end = (side/2, -h/3)
    
    # Calcular puntos para el primer lado completo
    first_side = koch_curve_points(start, top, depth)
    
    # Calcular puntos para la mitad del segundo lado
    second_side_half = koch_curve_partial_points(top, end, depth, 0.5)
    
    # Combinar todos los puntos
    all_points = first_side + second_side_half
    
    # Extraer coordenadas X e Y
    x_coords = [p[0] for p in all_points]
    y_coords = [p[1] for p in all_points]
    
    # Dibujar la mitad exacta del copo (sin línea de simetría)
    ax.plot(x_coords, y_coords, 'blue', linewidth=1.5)
    
    # Configurar el gráfico
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Mitad del Copo de Nieve de Koch')
    
    # Establecer los límites del gráfico para centrarlo mejor
    ax.set_xlim(-side/2 - 20, side/2 + 20)
    ax.set_ylim(-h/3 - 20, 2*h/3 + 20)
    
    # Convertir a imagen base64
    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return image_base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_snowflake')
def generate_snowflake():
    try:
        image_data = draw_half_koch_snowflake_exact()
        return jsonify({'image': image_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)