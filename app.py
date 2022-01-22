from tkinter import *
import find_path
import validator
root = Tk()


w = Canvas(root, width=300, height=300)
w.pack()

filenameLabel = Label(root, text="Enter filename: ")
filenameLabel.place(x=0, y=0)

filename = Entry(root, width=40)
filename.place(x=0, y=20)
#filename.insert(0, 'Enter the filename')

w1label = Label(root, text="Enter value of a: ")
w1label.place(x=0, y=60)

weight1 = Entry(root, width=40)
weight1.place(x=0, y=80)
# weight1.insert(0, 'Enter value for a')  # for placeholder

w2label = Label(root, text="Enter value of b: ")
w2label.place(x=0, y=120)

weight2 = Entry(root, width=40)
weight2.place(x=0, y=140)

evaluate = Button(root, text="Evaluate",
                  command=lambda: find_path.run(filename.get()))
evaluate.place(x=100, y=180)


def show_answer():
    qor = validator.validator(filename.get()+".csv",
                              "solution.csv", w1label.get(), w2label.get())
    qorE = Label(root,  text="%s" % (qor))
    qorE.place(0, 260)


qor = Label(root, text="Quality of Result is: ")
qor.place(x=0, y=220)

qorEntry = Button(root, text="Show",
                  command=show_answer)
qorEntry.place(x=100, y=240)


root.mainloop()
