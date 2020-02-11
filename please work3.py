from tkinter import *
import time
import math


canvas_width = 600
canvas_height = 800

root = Tk()
root.resizable(width=False, height=False)


##button1 = Button(root, text="AAAAAAAAAA")
##button2 = Button(root, text="AAAAAAAAAA")
##button3 = Button(root, text="AAAAAAAAAA")
##button4 = Button(root, text="AAAAAAAAAA")
##button1.grid(row=1,column=1)
##button2.grid(row=2,column=1)
##button3.grid(row=3,column=1)
##button4.grid(row=4,column=1)

canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.grid(row=1,column=2)

##string0 = "Displacement = " + 

def setSpring(top_y,base_y,x,r):
    banana = (base_y - top_y)/6
    
    y1 = top_y + banana
    x1 = x + r

    y2 = top_y + (3*banana)
    x2 = x - r

    y3 = top_y + (5*banana)
    x3 = x + r

    y4 = top_y + (6*banana)
    x4 = x

    line1 = canvas.create_line(x, top_y, x1, y1,width=linew,fill="black")
    line2 = canvas.create_line(x1, y1, x2, y2,width=linew,fill="black")
    line3 = canvas.create_line(x2, y2, x3, y3,width=linew,fill="black")
    line4 = canvas.create_line(x3, y3, x4, y4,width=linew,fill="black")
    return line1, line2, line3, line4



x = canvas_width / 2
top_y = 20
base_y = (canvas_height/ 2) + (10 * math.cos(0))
originbase_y = base_y

linew = 2
r = 20

init_displacement = 300
string0 = "Displacement = " 

originline = canvas.create_line(0, originbase_y, canvas_width, originbase_y,width=linew,fill="green")
weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r), fill="black")

timeperiod = 2
t = timeperiod/200
print(t)

line1, line2, line3, line4 = setSpring(top_y,base_y,x,r)
counter = 0

while 1:
    time.sleep(t)
##    print(counter)
    state = init_displacement * math.cos(counter * (math.pi/64))

    
##    print(state)

    base_y = originbase_y + state

##    print(base_y)
    canvas.delete(weight)
    canvas.delete(line1)
    canvas.delete(line2)
    canvas.delete(line3)
    canvas.delete(line4)
    line1, line2, line3, line4 = setSpring(top_y,base_y,x,r)
    
    if base_y <= originbase_y:
        weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r),outline="red", fill="red")
    elif base_y > originbase_y:
        weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r),outline="blue", fill="blue")
        
    canvas.update()
    counter = counter+1




root.mainloop()


### https://www.python-course.eu/tkinter_canvas.php








