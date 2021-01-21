import cv2
import glob
import numpy as np
import pandas as pd
import random
import paramiko
import h5py
from datetime import datetime
import keyboard
from screeninfo import get_monitors
from scipy.interpolate import make_interp_spline
import paramiko
import os
import PySimpleGUI as sg

sg.theme('DarkAmber')

path_images = "build/caballo2gui/images/"

# Parte del test

new_dim = int(0.75*get_monitors()[0].height)

freq_x = [1.5, 3, 6, 12, 18]
contrastes =[[0.8,0.6,0.3,0.15,0.075,0.0375,0.009375,0.01875,0.00446875],
[0.6,0.3,0.15,0.075,0.0375,0.01875,0.009375,0.0046875],
[0.6,0.3,0.15,0.075,0.0375,0.01875,0.009375,0.00703125,0.0046875],
[0.8,0.6,0.3,0.15,0.075,0.0375,0.01875,0.009375],
[1,0.8,0.6,0.3,0.15,0.075,0.0375,0.01875]]

hf = h5py.File("build/caballo2gui/mask.h5", "r")
mask = np.array(hf.get("mask"))
hf.close()

imgs_1_5 = ["1.5/1,5-0,8.png","1.5/1,5-0,6.png","1.5/1,5-0,3.png","1.5/1,5-0,15.png","1.5/1,5-0,075.png","1.5/1,5-0,0375.png","1.5/1,5-0,009375.png","1.5/1.5-0,01875.png","1.5/1,5-0,00446875.png"]
imgs_3 = ["3/3-0.6.png","3/3-0.3.png","3/3-0.15.png","3/3-0.075.png","3/3-0.0375.png","3/3-0.01875.png","3/3-0.009375.png","3/3-0.0046875.png"]
imgs_6 = ["6/6-0.6.png","6/6-0.3.png","6/6-0.15.png","6/6-0.075.png","6/6-0.0375.png","6/6-0.01875.png","6/6-0.009375.png","6/6-0.00703125.png","6/6-0.0046875.png"]
imgs_12 = ["12/12-0.8.png","12/12-0.6.png","12/12-0.3.png","12/12-0.15.png","12/12-0.075.png","12/12-0.0375.png","12/12-0.01875.png","12/12-0.009375.png"]
imgs_18 = ["18/18-1.png","18/18-0.8.png","18/18-0.6.png","18/18-0.3.png","18/18-0.15.png","18/18-0.075.png","18/18-0.0375.png","18/18-0.01875.png"]

caballo = np.zeros((539, 539, 3))

for i in range(mask.shape[0]):
    for j in range(mask.shape[1]):
        if mask[i,j] == 2:
            caballo[i,j] = [163, 147, 149]
        else:
            caballo[i,j] = [170, 154, 156]

caballo = caballo.astype("uint32")

fondoGris_r = np.ones((539*2, 539*2))*170
fondoGris_g = np.ones((539*2, 539*2))*154
fondoGris_b = np.ones((539*2, 539*2))*156

fondoGris = np.stack([fondoGris_r, fondoGris_g, fondoGris_b], axis = -1).astype("float32")

def imagenes(frecuencia):
    """
    frecuencia: cv2.imread con el patron de ruido adecuado
    """
    im1, im2, im3 = caballo, caballo, caballo
    cebra = caballo.copy()
    f_fondo = cv2.cvtColor(cv2.imread(frecuencia), cv2.COLOR_BGR2RGB)
    for i in range(caballo.shape[0]):
        for j in range(caballo.shape[1]):
            if mask[i,j] == 1:
                cebra[i,j] = f_fondo[i,j]
    cebra = cebra
    imagenes = [im1, im2, im3, cebra]
    return imagenes

def fadeIn (img1, img2, long=10):
    for IN in range(0,long):
        fadein = IN/float(long)
        dst = cv2.addWeighted( img1, 1-fadein, img2, fadein, 0)
        dst = cv2.blur(dst, (10, 10))
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        dst = cv2.resize(dst, (new_dim,new_dim), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Test", dst.astype("uint8"))
        cv2.waitKey(3)

indices = []

# GUI

insertar_datos_columna = [

    [
        sg.Text("", font = ("Helvetica", 20)),
    ],

    [

        sg.Text("Nombre paciente:", font = ("Helvetica", 10)),

        sg.In(size=(25, 1), enable_events=True, key="-NOMBRE-")

    ],

    [

        sg.Text("Apellidos paciente:", font = ("Helvetica", 10)),

        sg.In(size=(25, 1), enable_events=True, key="-APELLIDOS-"),

    ],

    [
        sg.Text("", font = ("Helvetica", 20)),
    ],

    [
        sg.Text("Instrucciones:", font = ("Helvetica", 15)),
    ],

    [
        sg.Text("Este test se ha diseñado con el objetivo de medir la CSF del paciente.", font = ("Helvetica", 10)),
    ],

    [
        sg.Text("Para ello, éste visualizará una serie de imágenes constituidas cada", font = ("Helvetica", 10))
    ],

    [
        sg.Text("una de ellas por cuatro animales: tres caballos y una cebra,", font = ("Helvetica", 10))
    ],

    [
        sg.Text("numerados del 1 al 4 empezando por la imagen de la esquina superior", font = ("Helvetica", 10))
    ],

    [
        sg.Text("izquierda. El objetivo es detectar cuál de ellos es la cebra y para ello", font = ("Helvetica", 10))
    ],

    [
        sg.Text("se ha de pulsar el número correspondiente a la que el paciente clasifique", font = ("Helvetica", 10))
    ],

    [
        sg.Text("como tal.", font = ("Helvetica", 10))
    ],

    [
        sg.Text("", font = ("Helvetica", 20)),
    ],

    [

        sg.Button("Comenzar", size=(10, 1))

    ],

    [

        sg.Button("Salir", size=(10, 1))

    ],

]

image_viewer_column = [

    [sg.Image(key="-IMAGE-")],

]

# ----- Full layout -----

layout = [

    [

        sg.Column(insertar_datos_columna),
        sg.VSeperator(),
        sg.Column(image_viewer_column),

    ]

]

window = sg.Window("Test", layout)

while True:
    event, values = window.read()
    
    if event == "Salir" or event == sg.WIN_CLOSED:
        break
    
    nombre = values["-NOMBRE-"]
    apellidos = values["-APELLIDOS-"]

    if event == "Comenzar":
        ant = ''
        j = 0
        for frecuencia in imgs_1_5:
            print("Estamos en un contraste de 1.5")
            print("Frecuencia: ", frecuencia)
            imagenes_4 = imagenes(path_images + frecuencia)
            indexes = np.array(random.sample(range(0, 4), 4))
            new_imagenes = [imagenes_4[i] for i in indexes]
            im_list_2d = [[new_imagenes[0].astype("float32"), new_imagenes[1].astype("float32")], [new_imagenes[2].astype("float32"), new_imagenes[3].astype("float32")]]
            imagen_total = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

            fadeIn(fondoGris, imagen_total, 100)

            respuesta = int(keyboard.read_key())
            respuesta = respuesta - 1

            index_cebra = int(np.where(indexes == 3)[0])
            if index_cebra == respuesta:
                acierto = True
                print(acierto)
            else:
                acierto = False
            j = j + 1
            if not acierto:
                print("Fallo")
                print(ant)
                break
            ant = frecuencia
        indices.append(j-2)
        j = 0
        for frecuencia in imgs_3:
            print("Estamos en un contraste de 3")
            print("Frecuencia: ", frecuencia)
            imagenes_4 = imagenes(path_images + frecuencia)
            indexes = np.array(random.sample(range(0, 4), 4))
            new_imagenes = [imagenes_4[i] for i in indexes]
            im_list_2d = [[new_imagenes[0].astype("float32"), new_imagenes[1].astype("float32")], [new_imagenes[2].astype("float32"), new_imagenes[3].astype("float32")]]
            imagen_total = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

            fadeIn(fondoGris, imagen_total, 100)

            respuesta = int(keyboard.read_key())
            respuesta = respuesta - 1

            index_cebra = int(np.where(indexes == 3)[0])
            if index_cebra == respuesta:
                acierto = True
                print(acierto)
            else:
                acierto = False
            j = j + 1
            if not acierto:
                print("Fallo")
                print(ant)
                break
            ant = frecuencia
        indices.append(j-2)
        j = 0
        for frecuencia in imgs_6:
            print("Estamos en un contraste de 6")
            print("Frecuencia: ", frecuencia)
            imagenes_4 = imagenes(path_images + frecuencia)
            indexes = np.array(random.sample(range(0, 4), 4))
            new_imagenes = [imagenes_4[i] for i in indexes]
            im_list_2d = [[new_imagenes[0].astype("float32"), new_imagenes[1].astype("float32")], [new_imagenes[2].astype("float32"), new_imagenes[3].astype("float32")]]
            imagen_total = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

            fadeIn(fondoGris, imagen_total, 100)

            respuesta = int(keyboard.read_key())
            respuesta = respuesta - 1

            index_cebra = int(np.where(indexes == 3)[0])
            if index_cebra == respuesta:
                acierto = True
                print(acierto)
            else:
                acierto = False
            j = j + 1
            if not acierto:
                print("Fallo")
                print(ant)
                break
            ant = frecuencia
        indices.append(j-2)
        j = 0
        for frecuencia in imgs_12:
            print("Estamos en un contraste de 12")
            print("Frecuencia: ", frecuencia)
            imagenes_4 = imagenes(path_images + frecuencia)
            indexes = np.array(random.sample(range(0, 4), 4))
            new_imagenes = [imagenes_4[i] for i in indexes]
            im_list_2d = [[new_imagenes[0].astype("float32"), new_imagenes[1].astype("float32")], [new_imagenes[2].astype("float32"), new_imagenes[3].astype("float32")]]
            imagen_total = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

            fadeIn(fondoGris, imagen_total, 100)

            respuesta = int(keyboard.read_key())
            respuesta = respuesta - 1

            index_cebra = int(np.where(indexes == 3)[0])
            if index_cebra == respuesta:
                acierto = True
                print(acierto)
            else:
                acierto = False
            j = j + 1
            if not acierto:
                print("Fallo")
                print(ant)
                break
            ant = frecuencia
        indices.append(j-2)
        j = 0
        for frecuencia in imgs_18:
            print("Estamos en un contraste de 18")
            print("Frecuencia: ", frecuencia)
            imagenes_4 = imagenes(path_images + frecuencia)
            indexes = np.array(random.sample(range(0, 4), 4))
            new_imagenes = [imagenes_4[i] for i in indexes]
            im_list_2d = [[new_imagenes[0].astype("float32"), new_imagenes[1].astype("float32")], [new_imagenes[2].astype("float32"), new_imagenes[3].astype("float32")]]
            imagen_total = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

            fadeIn(fondoGris, imagen_total, 100)

            respuesta = int(keyboard.read_key())
            respuesta = respuesta - 1

            index_cebra = int(np.where(indexes == 3)[0])
            if index_cebra == respuesta:
                acierto = True
                print(acierto)
            else:
                acierto = False
            j = j + 1
            if not acierto:
                print("Fallo")
                print(ant)
                break
            ant = frecuencia
        indices.append(j-2)
        umbrales = [contrastes[i][indices[i]] if indices[i] != -1 else 1 for i in range(len(contrastes))]
        print("Umbrales: ", umbrales)

        import matplotlib.pyplot as plt
        y = 1/np.array(umbrales)
        x = np.array(freq_x)
        x_new = np.linspace(x.min(), x.max(), 300)
        a_BSpline = make_interp_spline(x, y)
        y_new = a_BSpline(x_new)
        plt.plot(x_new, y_new, ".", color = "blue")
        plt.yscale(value = "log")
        plt.grid()
        plt.xticks(freq_x, freq_x)
        plt.xlabel("Frecuencia espacial (cpg)")
        plt.ylabel("S (dB)")
        plt.savefig("resultados/" + nombre + "_" + datetime.now().strftime('%m-%d-%Y') + ".png")

        try:
            host = "188.166.150.7"
            port = 22
            username = "root"
            password = "asASkmfdmkA123!a"

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            sftp = ssh.open_sftp()
            sftp.get("/srv/shiny-server/proyecto_cebra/database.csv", "build/caballo2gui/database.csv")
            sftp.close()

            new_row = {"Nombre":nombre, "Apellidos": apellidos, "Fecha":datetime.now().strftime('%Y-%m-%d'), "F1.5":umbrales[0], "F3":umbrales[1], "F6":umbrales[2], "F12":umbrales[3], "F18":umbrales[4]}
            database = pd.read_csv("build/caballo2gui/database.csv")
            database = database.append(new_row, ignore_index = True)
            database.to_csv("build/caballo2gui/database.csv", index = False)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
            sftp = ssh.open_sftp()
            sftp.put("build/caballo2gui/database.csv", "/srv/shiny-server/proyecto_cebra/database.csv")
            sftp.close()

            os.remove("build/caballo2gui/database.csv")

            print("Base de datos actualizada y enviada a la Web.")
        except:
            print("No existe la base de datos llamada 'database.csv' o ha sucedido un error de conexión.")
        
        resultado = cv2.imread("resultados/" + nombre + "_" + datetime.now().strftime('%m-%d-%Y') + ".png")
        cv2.destroyAllWindows()
        imgbytes = cv2.imencode(".png", resultado)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

window.close()