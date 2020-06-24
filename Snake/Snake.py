import turtle
import random
import time
retraso=0.1
nombre="Edgar"
segments = []
# score
score = 0
high_score = 0
comida=False

#Atributos de la ventana de juego
win = turtle.Screen()
win.title(nombre+"'s snake game")
win.bgcolor("black")
win.setup(width=600,height=600)
win.tracer(0)

# Cabeza de la vibora
head = turtle.Turtle()
head.speed(0)
head.shape("arrow")
head.color("grey")
head.penup()
head.goto(0, 100)
# Creamos el atributo direction
head.direction = "stop"

# Funciones para mover la vibora
def move():
    '''
    La función move manejará 5 estados:
    1. stop: No hay movimiento
    2. up: Se desplazará hacia arriba 20 unidades
    3. down: Se desplazará hacia abajo 20 unidades
    4. right: Se desplazará hacia la derecha 20 unidades
    5. left: Se desplazará hacia la izquierda 20 unidades
    '''
    if head.direction == "up":
        y = head.ycor() #Coordenada en y de la cabeza de la serpiente
        head.sety(y + 20)
 
    if head.direction == "down":
        y = head.ycor() #Coordenada en y de la cabeza de la serpiente
        head.sety(y - 20)
 
    if head.direction == "right":
        x = head.xcor() #Coordenada en x de la cabeza de la serpiente
        head.setx(x + 20)
 
    if head.direction == "left":
        x = head.xcor() #Coordenada en x de la cabeza de la serpiente
        head.setx(x - 20)

# Funciones para modificar el estado de direction
# Estas funciones consideran evitar que los movimientos
# opuestos se puedan usar; i.e. si va hacia arriba,
# no puede ir hacia abajo.

def go_up():
    if head.direction != "down":
        head.direction = "up"
        head.setheading(90)

def go_down():
    if head.direction != "up":
        head.direction = "down"
        head.setheading(270)

def go_right():
    if head.direction != "left":
        head.direction = "right"
        head.setheading(0)

def go_left():
    if head.direction != "right":
        head.direction = "left"
        head.setheading(180)
        
        
# keyboard bindings
win.listen()
win.onkey(go_up, "Up")
win.onkey(go_down, "Down")
win.onkey(go_right, "Right")
win.onkey(go_left, "Left")


# Primer manzana
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.shapesize(0.50, 0.50)
food.goto(0, 0)

# Marcador
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: {} High Score: {}".format(score,high_score), align="center", font=("Courier", 24, "normal"))

def score_add():
    global score
    global high_score
    score = score+10
    if score > high_score:
        high_score = score
    pen.clear()
    pen.write("Score: {} High Score: {}".format(score,high_score), align="center", font=("Courier", 24, "normal"))
    
    
def score_end():
    global score
    global high_score
    # reset score
    score = 0
    # update score
    pen.clear()
    pen.write("score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    
    
# Cuerpo de la vibora
def body_collision():
    pass

# add a segment
def body():
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape("square")
    new_segment.color("grey")
    new_segment.penup()
    segments.append(new_segment)
    
def move_body():
    if segments!=[]:
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)
        body_collision()
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
        segments[0].shape("arrow")
        
        
# Función para crear manzanas aleatoriamente
def new_food():
    global retraso
    global comida
    if head.distance(food) <15:
        # Movemos la comida a una posición aleatoria en la pantalla
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        score_add()
        body()
        retraso=retraso*0.95
        comida=True
        
# Colisión con el borde de la pantalla
def border_collision():
    global retraso
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        # Pausa el juego por 1 segundo, indicando el final del mismo
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"
        # Quitamos el cuerpo de la víbora de la pantalla
        for segment in segments:
            segment.goto(1000, 1000)
        # Eliminamos el cuerpo de la víbora
        segments.clear()
        # Se registra el score
        score_end()
        # Se reinicia la velocidad del juego
        retraso=0.1
        
# Colisión con el cuerpo    
def body_collision():
    '''
    Función que determina si la cabeza entra en contacto con
    el cuerpo de la serpiente. Esta función se desactiva por
    1 segundo, cada que la serpiente come una manzana, para 
    evitar conflicto con las otras funciones.
    '''
    global retraso
    global comida
    if comida==False:
        # Check for head collision
        for segment in segments:
            if segment.distance(head) == 0:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"
                # Hide the segments
                for segment in segments:
                    segment.goto(1000, 1000)
                # clear segment list
                segments.clear()
                score_end()
                retraso=0.1
                
                
# Loop que permite tener la ventana activa del juego
while True:
    win.update()
    move()
    new_food()
    move_body()
    time.sleep(retraso)
    border_collision()
    comida=False