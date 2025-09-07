import turtle
import math

# Curva de Koch completa
def koch_curve(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        koch_curve(t, length, depth-1)
        t.left(60)
        koch_curve(t, length, depth-1)
        t.right(120)
        koch_curve(t, length, depth-1)
        t.left(60)
        koch_curve(t, length, depth-1)

# Curva de Koch parcial: dibuja una fracción p ∈ [0,1] del CONTORNO
def koch_curve_partial(t, length, depth, p):
    if p <= 0:
        return
    if depth == 0:
        t.forward(length * p)
        return

    length3 = length / 3.0
    # Cada curva de Koch se compone de 4 subcurvas con exactamente 1/4 del perímetro
    parts = [max(0.0, min(1.0, p*4 - i)) for i in range(4)]

    # 1ª subcurva
    koch_curve_partial(t, length3, depth-1, parts[0])
    if parts[1] <= 0: return

    t.left(60)
    # 2ª subcurva
    koch_curve_partial(t, length3, depth-1, parts[1])
    if parts[2] <= 0: return

    t.right(120)
    # 3ª subcurva
    koch_curve_partial(t, length3, depth-1, parts[2])
    if parts[3] <= 0: return

    t.left(60)
    # 4ª subcurva
    koch_curve_partial(t, length3, depth-1, parts[3])

# Mitad EXACTA del copo (por perímetro): 1 lado completo + 1/2 del siguiente
def koch_half_snowflake_exact(t, side, depth):
    h = side * math.sqrt(3) / 2
    t.penup()
    t.goto(-side/2, -h/3)  # centrado aproximado
    t.setheading(60)
    t.pendown()

    # 1 lado completo
    koch_curve(t, side, depth)
    # + 0.5 del siguiente lado (mitad exacta del perímetro)
    t.right(120)
    koch_curve_partial(t, side, depth, 0.5)

# --- Configuración y ejecución ---
screen = turtle.Screen()
screen.bgcolor("black")

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(2)
t.color("pink")

koch_half_snowflake_exact(t, side=300, depth=4)

turtle.done()
