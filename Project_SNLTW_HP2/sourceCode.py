import turtle
import time
import random
import winsound

# Khởi tạo màn hình trò chơi
wn = turtle.Screen()
wn.title("Trò chơi rắn săn mồi")
wn.bgpic("bgimg.png")
wn.tracer(0)
wn.setup(width=1700, height=800)

# Vẽ các bức tường giới hạn không gian di chuyển
edge = turtle.Turtle()
edge.hideturtle()
edge.penup()
edge.goto(-290,290)
edge.pensize(10)
edge.pendown()
for i in range(4): 
    edge.forward(580)
    edge.right(90)

# In các dòng hướng dẫn
guide = turtle.Turtle()
guide.penup()
guide.hideturtle()
guide.color("white")
x_guide = 450
y_guide = 200
guide.goto(x_guide,y_guide)
guide.write("Hướng dẫn:", align="left", font=("candara", 20, "bold"))
y_guide -= 25
guide.goto(x_guide,y_guide)
guide.write("\u2190 Di chuyển sang trái", align="left", font=("candara", 14, "bold"))
y_guide -= 25
guide.goto(x_guide,y_guide)
guide.write("\u2191   Di chuyển lên", align="left", font=("candara", 14, "bold"))
y_guide -= 25
guide.goto(x_guide,y_guide)
guide.write("\u2192 Di chuyển sang phải", align="left", font=("candara", 14, "bold"))
y_guide -= 25
guide.goto(x_guide,y_guide)
guide.write("\u2193   Di chuyển xuống", align="left", font=("candara", 14, "bold"))

# Khởi tạo các tham số
delay = 0.1
score = 0
high_score = 0
segments = []

# Khởi tạo biến turtle đại diện cho đầu của con rắn
head = turtle.Turtle()
head.shape("circle")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Hàm tạo các con mồi
def createNewFood(food):
    x = random.randint(-270, 270)
    y = random.randint(-270, 270)
    colors = random.choice(['yellow', 'green', 'red'])
    food.color(colors)
    food.goto(x, y)

# Khởi tạo biến turtle đại diện cho con mồi
food = turtle.Turtle()
food.shape('turtle')
food.speed(0)
food.penup()
createNewFood(food)

# Khởi tạo biến turtle giúp in điểm số trò chơi
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 350)
pen.write("Điểm : 0 Kỷ lục: 0", align="center",
        font=("candara", 24, "bold"))

# Khởi tạo biến turtle đại diện cho logo Game Over
g = turtle.Turtle()
g.penup()
image = "gameOver.gif"
wn.addshape(image)
g.shape(image)
g.hideturtle()

# Các hàm giúp điều khiển con rắn thông qua các phím mũi tên
def goUp():
    if head.direction != "down":
        head.direction = "up"
    winsound.PlaySound("move.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

def goDown():
    if head.direction != "up":
        head.direction = "down"
    winsound.PlaySound("move.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

def goLeft():
    if head.direction != "right":
        head.direction = "left"
    winsound.PlaySound("move.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

def goRight():
    if head.direction != "left":
        head.direction = "right"
    winsound.PlaySound("move.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

def move():
    if head.direction != 'Stop':
        g.hideturtle()
        head.showturtle()
        food.showturtle()
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)

wn.listen()
wn.onkeypress(goUp, "Up")
wn.onkeypress(goDown, "Down")
wn.onkeypress(goLeft, "Left")
wn.onkeypress(goRight, "Right")

# Vòng lặp chính của trò chơi
while True:
    wn.update()
    # Kiểm tra đầu con rắn có chạm vào các bức tường xung quanh hay không?
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        delay = 0.1
        winsound.PlaySound("gameOver.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
        g.showturtle()
        head.hideturtle()
        food.hideturtle()
        head.goto(0, 0)
        head.direction = "Stop"
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        score = 0
        pen.clear()
        pen.write("Điểm : {} Kỷ lục : {} ".format(
            score, high_score), align="center", font=("candara", 24, "bold"))

    # Kiểm tra đầu con rắn có chạm vào con mồi
    if head.distance(food) < 20:
        createNewFood(food)
        winsound.PlaySound("score.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle")
        new_segment.color("orange")
        new_segment.penup()
        segments.append(new_segment)
        delay -= 0.001
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write("Điểm : {} Kỷ lục : {} ".format(
            score, high_score), align="center", font=("candara", 24, "bold"))
    
    # Cập nhật vị trí của thân con rắn
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    
    # Cập nhật đầu con rắn theo điều khiển của người dùng
    move()
    
    # Kiểm tra đầu con rắn có chạm vào thân của nó hay không?
    for segment in segments:
        if segment.distance(head) < 20:
            delay = 0.1
            winsound.PlaySound("gameOver.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
            g.showturtle()
            head.hideturtle()
            food.hideturtle()
            head.goto(0, 0)
            head.direction = "Stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            pen.clear()
            pen.write("Điểm : {} Kỷ lục : {} ".format(
                score, high_score), align="center", font=("candara", 24, "bold"))
    time.sleep(delay)
