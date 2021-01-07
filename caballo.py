import cv2
import glob
import numpy as np
import random


blink = 50 # Tiempo de parpadeo en milisegundos
num_parpadeos = 3
base_imagenes = "images/"
pruebas = ["1.png", "2.png"]
imgs_1_5 = ["1.5/1,5-0,3.png","1.5/1,5-0,6.png","1.5/1,5-0,8.png","1.5/1,5-0,15.png","1.5/1,5-0,075.png","1.5/1,5-0,0375.png","1.5/1,5-0,009375.png","1.5/1,5-0,00446875.png","1.5/1.5-0,01875.png"]
imgs_6 = ["6/6-0.3.png","6/6-0.6.png","6/6-0.15.png","6/6-0.075.png","6/6-0.0375.png","6/6-0.01875.png","6/6-0.009375.png","6/6-0.0046875.png","6/6-0.00703125.png"]
imgs_18 = ["18/18-0.3.png","18/18-0.6.png","18/18-0.8.png","18/18-0.15.png","18/18-0.075.png","18/18-0.0375.png","18/18-0.01875.png","18/18-1.png"]
caballo = cv2.imread(f'{base_imagenes}mascara.png', 0)
caballo = cv2.resize(caballo, (500,500))
gris = cv2.imread(f'{base_imagenes}gris.png', 0)
gris = cv2.resize(caballo, (500,500))
grisperodeverdadnomas = cv2.imread(f'{base_imagenes}todogris.png', 0)
grisperodeverdadnomas = cv2.resize(grisperodeverdadnomas, (500,500))


def imagenes(frecuencia):
    """
    frecuencia: cv2.imread con el patron de ruido adecuado
    """
    im2, im3, im4 = grisperodeverdadnomas,grisperodeverdadnomas,grisperodeverdadnomas
    frecuencia = cv2.imread(frecuencia, 0)
    frecuencia = cv2.resize(frecuencia, (500,500))
    masked_horse = cv2.bitwise_and(frecuencia, gris)
    masked_horse = np.where(masked_horse==0, 161, masked_horse)
    imagenes = [im2, im2, im3, im4] # Falta cambiar uno por la cebra pero no tengo la imagen
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
    aux = np.zeros((1000,1000))
    for i in range(num_parpadeos):
        cv2.imshow('Res',aux)
        cv2.waitKey(blink)
        cv2.imshow('Res',res)
        cv2.waitKey(blink)
    cv2.imshow('Res',res)
    respuesta = input("Introduzca posicion de la cebra [1,2,3,4]: ")
    if int(respuesta) - 1 == correcta:
            return True
    else:
        return False
    #cv2.waitKey(0)


if __name__ == "__main__":
    ant = ''
    for frecuencia in imgs_1_5:
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
    for frecuencia in imgs_18:
        freq = f'{base_imagenes}{frecuencia}'
        imgs, cebra = imagenes(freq)
        barajadas, correcta = baraja(imgs, cebra)
        acierto = parpadeo(barajadas, correcta)
        if not acierto:
            print(ant)
            break
        ant = frecuencia
