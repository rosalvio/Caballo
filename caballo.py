import cv2
import glob
import numpy as np
import random


colorGris = 159
fondoGris = np.ones((1000,1000), np.uint8)*colorGris
base_imagenes = "images/"
pruebas = ["1.png", "2.png"]
imgs_1_5 = ["1.5/1,5-0,8.png","1.5/1,5-0,6.png","1.5/1,5-0,3.png","1.5/1,5-0,15.png","1.5/1,5-0,075.png","1.5/1,5-0,0375.png","1.5/1,5-0,009375.png","1.5/1.5-0,01875.png","1.5/1,5-0,00446875.png"]
imgs_3 = ["3/3-0.6.png","3/3-0.3.png","3/3-0.15.png","3/3-0.075.png","3/3-0.0375.png","3/3-0.01875.png","3/3-0.009375.png","3/3-0.0046875.png"]
imgs_6 = ["6/6-0.6.png","6/6-0.3.png","6/6-0.15.png","6/6-0.075.png","6/6-0.0375.png","6/6-0.01875.png","6/6-0.009375.png","6/6-0.0046875.png","6/6-0.00703125.png"]
imgs_12 = ["12/12-0.8.png","12/12-0.6.png","12/12-0.3.png","12/12-0.15.png","12/12-0.075.png","12/12-0.0375.png","12/12-0.01875.png","12/12-0.009375.png"]
imgs_18 = ["18/18-1.png","18/18-0.8.png","18/18-0.6.png","18/18-0.3.png","18/18-0.15.png","18/18-0.075.png","18/18-0.0375.png","18/18-0.01875.png"]
caballo = cv2.imread(f'{base_imagenes}mascara2.png', 0)
caballo = cv2.resize(caballo, (500,500))
gris = cv2.imread(f'{base_imagenes}gris2.png', 0)
gris = cv2.resize(caballo, (500,500))
blanco = cv2.imread(f'{base_imagenes}blanco.png', 0)
blanco = cv2.resize(blanco, (500,500))
grisperodeverdadnomas = cv2.imread(f'{base_imagenes}todogris2.png', 0)
grisperodeverdadnomas = cv2.resize(grisperodeverdadnomas, (500,500))


def imagenes(frecuencia):
    """
    frecuencia: cv2.imread con el patron de ruido adecuado
    """
    im2, im3, im4 = grisperodeverdadnomas,grisperodeverdadnomas,grisperodeverdadnomas
    frecuencia = cv2.imread(frecuencia, 0)
    frecuencia = cv2.resize(frecuencia, (500,500))
    masked_horse = cv2.bitwise_and(frecuencia, gris)
    masked_horse = np.where(masked_horse==0, colorGris, masked_horse)
    masked_horse = cv2.bitwise_and(masked_horse, blanco)
    imagenes = [im2, im2, im3, im4]
    return imagenes, masked_horse

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def baraja(imagenes, cebra):
    """
    imagenes: array con las imagenes que van a ser barajadas para que cambie la posicion de la cebra
    """
    aux = imagenes
    correcta = random.randint(0, 3)
    aux[correcta] = cebra
    res = concat_tile([[aux[0], aux[1]],
                    [aux[2], aux[3]]])
    
    return res, correcta

def parpadeo(res, correcta):
    """
    res: imagen resultante despues de barajarlas
    """
    fadeIn(fondoGris, barajadas, 1000)
    respuesta = int(input("Introduzca posicion de la cebra [1,2,3,4]: "))
    fadeIn(barajadas, fondoGris, 1000)
    if respuesta - 1 == correcta:
            return True
    else:
        return False
    #cv2.waitKey(0)

def fadeIn (img1, img2, len=10):
    for IN in range(0,len):
        fadein = IN/float(len)
        dst = cv2.addWeighted( img1, 1-fadein, img2, fadein, 0)
        cv2.imshow('Res', dst)
        cv2.waitKey(1)

if __name__ == "__main__":
    nombre = input("Introduzca el nombre del paciente: ")
    print(nombre)
    ant = ''
    for frecuencia in imgs_1_5:
        freq = f'{base_imagenes}{frecuencia}'
        imgs, cebra = imagenes(freq)
        barajadas, correcta = baraja(imgs, cebra)
        acierto = parpadeo(barajadas, correcta)
        acierto = False
        if not acierto:
            print(ant)
            break
        ant = frecuencia
    for frecuencia in imgs_3:
        freq = f'{base_imagenes}{frecuencia}'
        imgs, cebra = imagenes(freq)
        barajadas, correcta = baraja(imgs, cebra)
        acierto = parpadeo(barajadas, correcta)
        if not acierto:
            print(ant)
            break
        ant = frecuencia
    for frecuencia in imgs_6:
        freq = f'{base_imagenes}{frecuencia}'
        imgs, cebra = imagenes(freq)
        barajadas, correcta = baraja(imgs, cebra)
        acierto = parpadeo(barajadas, correcta)
        if not acierto:
            print(ant)
            break
        ant = frecuencia
    for frecuencia in imgs_12:
        freq = f'{base_imagenes}{frecuencia}'
        imgs, cebra = imagenes(freq)
        barajadas, correcta = baraja(imgs, cebra)
        acierto = parpadeo(barajadas, correcta)
        if not acierto:
            print(ant)
            break
        ant = frecuencia
    for frecuencia in imgs_18:
        freq = f'{base_imagenes}{frecuencia}'
        imgs, cebra = imagenes(freq)
        barajadas, correcta = baraja(imgs, cebra)
        acierto = parpadeo(barajadas, correcta)
        if not acierto:
            print(ant)
            break
        ant = frecuencia
