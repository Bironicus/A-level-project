from tkinter import *
import time
import math


canvas_width = 680
canvas_height = 700

root = Tk()
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

x = canvas_width / 2
top_y = 20
base_y = (canvas_height/ 2) + (10 * math.cos(0))
originbase_y = base_y

linew = 2
r = 20

originline = canvas.create_line(0, originbase_y, canvas_width, originbase_y,width=linew,fill="green")
weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r), fill="black")


def setSpring(top_y,base_y,x,r):
    b = (base_y - top_y)/6
    
    y1 = top_y + b
    x1 = x + r

    y2 = top_y + (3*b)
    x2 = x - r

    y3 = top_y + (5*b)
    x3 = x + r

    y4 = top_y + (6*b)
    x4 = x

    line1 = canvas.create_line(x, top_y, x1, y1,width=linew,fill="black")
    line2 = canvas.create_line(x1, y1, x2, y2,width=linew,fill="black")
    line3 = canvas.create_line(x2, y2, x3, y3,width=linew,fill="black")
    line4 = canvas.create_line(x3, y3, x4, y4,width=linew,fill="black")
    return line1, line2, line3, line4


timeperiod = 2
t = timeperiod/200

line1, line2, line3, line4 = setSpring(top_y,base_y,x,r)
counter = 0
init_displacement = 200

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



##while 1:
##    for banana in range(20):
##        base_y = base_y + 3
##        
##        canvas.delete(line)
##        canvas.delete(weight)
##        line = canvas.create_line(x, top_y, x, base_y,width=linew, fill="red")
##        weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r),outline="red", fill="red")
##        
##        time.sleep(t)
##        canvas.update()
##
##
##    for banana in range(20):
##        base_y = base_y - 3
##        
##        canvas.delete(line)
##        canvas.delete(weight)
##        line = canvas.create_line(x, top_y, x, base_y,width=linew, fill="red")
##        weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r),outline="red",  fill="red")
##        
##        
##        time.sleep(t)
##        canvas.update()
##
##
##    for banana in range(20):
##        base_y = base_y - 3
##        
##        canvas.delete(line)
##        canvas.delete(weight)
##        line = canvas.create_line(x, top_y, x, base_y,width=linew, fill="blue")
##        weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r),outline="blue",  fill="blue")
##        
##        
##        time.sleep(t)
##        canvas.update()
##
##
##    for banana in range(20):
##        base_y = base_y + 3
##        
##        canvas.delete(line)
##        canvas.delete(weight)
##        line = canvas.create_line(x, top_y, x, base_y,width=linew, fill="blue")
##        weight = canvas.create_rectangle(x-r, base_y, x+r, base_y+(2*r),outline="blue",  fill="blue")
##        
##        time.sleep(t)
##        canvas.update()




### https://www.python-course.eu/tkinter_canvas.php








