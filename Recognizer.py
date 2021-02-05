from PIL import ImageTk,Image
import PIL.Image
import io
from tkinter import *
import tkinter as tk
import numpy as np
from keras.models import load_model


# Definimos la ventana del Tkinter y el título de ésta.
windo = Tk()
windo.configure(background='white')
windo.title("Analizador de Digitos")
windo.geometry('820x520')
windo.resizable(0,0)


# Cargamos el modelo. El archivo de donde obtendremos los datos analizados por
# la red.
model = load_model('MNIST.h5')


# Método para una posible actualización con widgets de uso más dinamico.
def destroy_widget(widget):
    widget.destroy()

# Obtenemos los cuadros dibujados, reescalamos la imagen a 28x28 pixeles y
# codificamos. La convertimos el RGB a escala de grises y finalmente le damos
# la dimensión necesaria y la normalizamos (dividir por 255).
# Después de eso usamos el método predict de keras con que tiene como entrada
# el arreglo de los datos del dibujo. Finalmente, obtenemos el indice del valor
# máximo (el que más chance tiene de coincidir) y lo regresaremos como posible
# valor, y el valor que hay en ese indice corresponderá al porcentaje de acertar.
def pred_digit():
    global no,no1
    ps = canvas.postscript(colormode='color')
    # use PIL to convert to PNG
    im1 = PIL.Image.open(io.BytesIO(ps.encode('utf-8')))
    img = im1.resize((28,28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(1,28,28,1)
    img = img/255
    # Aquí tratamos de predecir la clase (0,1,...9)
    res = model.predict([img])[0]
    pred = np.argmax(res)
    acc = max(res)
    print(res)
    print(np.argmax(res))
    print(acc)



    # Dibuja Resultado
    no = tk.Label(windo, text='El dígito predecido es: ' +str(pred),
                  width=24, height=2,
                  fg="white", bg="hot pink",
                  font=('times', 16, ' bold '))
    no.place(x=500, y=200)

    no1 = tk.Label(windo, text='Porcentaje de exactitud: ' + str(int(acc*100)) + "%",
                   width=24, height=2,
                   fg="white", bg="MediumPurple1",
                   font=('times', 16, ' bold '))
    no1.place(x=500, y=280)



def dibuja_digito(evento):
    x = evento.x
    y = evento.y
    r=15
    canvas.create_oval(x-r, y-r, x + r, y + r, fill='black')
    panel5.configure(state=NORMAL)


# Limpiamos la ventana donde dibujamos
def borra_digito():
    panel5.configure(state=DISABLED)
    canvas.delete("all")
    try:
        no.destroy()
        no1.destroy()
    except:
        pass



# Contrucción de los botones de la interfaz.
panel5 = Button(windo,text = 'Predecir',state=DISABLED,command = pred_digit,
                width = 15,borderwidth=0,bg = 'midnightblue',fg = 'white',
                font = ('times',18,'bold'))
panel5.place(x=60, y=390)


panel6 = Button(windo,text = 'Borrar',width = 15,borderwidth=0,command = borra_digito,
                bg ='red',fg = 'white',font = ('times',18,'bold'))
panel6.place(x=280, y=390)

canvas = tk.Canvas(windo, width=420, height=290,highlightthickness=1,
                    highlightbackground="midnightblue", cursor="pencil")
canvas.grid(row=0, column=0, pady=2, sticky=W,)
canvas.place(x=70,y=90)
canvas.bind("<B1-Motion>", dibuja_digito)

lab = tk.Label(windo, text="Dibuja un Dígito", width=18, height=1, fg="white",
                bg="midnightblue", font=('times', 16, ' bold '))
lab.place(x=155, y=50)

# Mantenemos la ventana funcionando
windo.mainloop()
