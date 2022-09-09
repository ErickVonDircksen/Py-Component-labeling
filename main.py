#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu       cd viltualAmbiente / cd scripts /  .\activate
# Universidade Tecnológica Federal do Paraná
#===============================================================================
# Alunos Erick H. Dircksen e André L. Gomes 
from msilib.schema import Component
from pickle import TRUE
import sys
import timeit
import numpy as np
import cv2

sys.setrecursionlimit(10**6)
#===============================================================================

INPUT_IMAGE =  'arroz.bmp'
#INPUT_IMAGE =  'teste small.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.8
ALTURA_MIN = 1
LARGURA_MIN = 1
N_PIXELS_MIN = 1

#===============================================================================

def binariza (img, threshold):
    
    initial_conv = np.where((img <= threshold), img, 255)
    final_conv = np.where((initial_conv > threshold), initial_conv, 0)
    return final_conv

    ''' Binarização simples por limiarização.
Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
Valor de retorno: versão binarizada da img_in.'''

    # TODO: escreva o código desta função.
    # Dica/desafio: usando a função np.where, dá para fazer a binarização muito
    # rapidamente, e com apenas uma linha de código!

#-------------------------------------------------------------------------------
def novoComp(label,height,length,y,x):
   return {
        "label": label,
        "n_pixels": 0,
        "T": height,
        "L": length,
        "B": y,
        "R": x,
    }
  
def rotula (img, largura_min, altura_min, n_pixels_min):
 label = 1
 height = len(img)
 length = len(img[0])
 componenteSet = []
 if len(img)< altura_min or len(img[0])< largura_min or  (len(img)*len(img[0]) < 1 ):
    return  #Faz a checagem se é uma imagem válida.


 for y in range(height):
     for x in range(length):
        
         if img[y,x] == 255: # 255 foi escolhido arbitrariamente como label,uma opção melhor seria usar flaot e neste if estabelecer uma tolerancia aceitavel  
          
          componente = novoComp(label,height,length,y,x) #Inicia um novo componente caso encontre um componente
          
          fill(img,x,y,label, componente)
          
          if componente["n_pixels"] > n_pixels_min +10  and componente["T"] > ALTURA_MIN  and componente["L"] > LARGURA_MIN:
           componenteSet.append(componente) # Filtra os componentes de acordo com algumas regras, o ideal seria fazer a média do nº 
           label +=1                        # de pixel dos componentes e só aceitar de acordo com uma tolerância.
 
 return componenteSet 



def fill(img,x,y,label,componente):
  if img[y][x] != 255: # Volta na recursão cada saia do componente
    return
  
  img[y][x] = label  
  
  if x < componente["L"]:componente["L"] = x  #  observa vizinhança 4  
  if x > componente["R"]:componente["R"] = x
  if y < componente["T"]:componente["T"] = y
  if y > componente["B"]:componente["B"] = y
  componente["n_pixels"] += 1
  
  if y < img.shape[0] and x < img.shape[1] and x >= 0 and y >= 0 : # Verificação das boundaries da imagem
    fill(img,x-1,y,label,componente)
    fill(img,x+1,y,label,componente)
    fill(img,x,y-1,label,componente)
    fill(img,x,y+1,label,componente)

'''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # guaradar os extremos de cada componente no dicionário, definir a função recursiva de floodfill. 
#===============================================================================
def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()
#===============================================================================