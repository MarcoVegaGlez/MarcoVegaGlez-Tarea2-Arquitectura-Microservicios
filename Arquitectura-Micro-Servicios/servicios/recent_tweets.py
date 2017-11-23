# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: recent_tweets.py
# Tarea: Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco, Yonathan Mtz y Marco Vega.
# Version: 1.3 Noviembre
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en un objeto JSON
#   comentarios recientes acerca de una pelicula o serie de television haciendo uso de la API de Tweeter
#   con la ayuda de la libreria twython.
#   API Twitter: https://developer.twitter.com/en/docs
#   API twython: https://github.com/ryanmcgrath/twython
#
#
#
#                                        recent_tweets.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Ofrecer un JSON que  | - Utiliza el API de    |
#           |    Procesador de      |    contenga tweets      |   Twython.             |
#           |     comentarios       |    recientes de pelí-   | - Devuelve un JSON con |
#           |      de Twitter       |    culas o series en    |   tweets de la serie o |
#           |                       |    particular.          |   pelicula en cuestión.|
#           +-----------------------+-------------------------+------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8085/api/v1/information?t=matrix
#
import os
from flask import Flask, abort, render_template, request
from twython import Twython
import urllib, json

app = Flask(__name__)




@app.route("/api/v1/information")
def get_tweets():
    """
    Este método obtiene información acerca de un tweet de una película o serie
    específica.
    :return: JSON con la información del tweet de la película o serie
    """
    # Se lee el parámetro 't' que contiene el título de la película o serie que se va a consultar
    title = request.args.get("t")    
    # Se crean las llaves (keys) para poder obtener los tweets de Twitter
    consumerkey = "4NSUdUvAh5zVofUgoPTpLAWIR"
    consumerSecretKey = "9QCWVUexXwZWMlFucJzw0aT4e092OQkKp1Au7j1JqIobxrVeXA"
    accesToken = "399643418-7zUPZXiglJweB2yfYJN9WlBdVwyDxKYWC0hpKYKf"
    accesSecretToken = "Up4YyniBoZRf7in2YroFhJgXAFky9I0XRthVLFY2BNbXS"
    # Se instancia la libreria de twython, con las llaves como argumentos
    twitter = Twython(consumerkey, consumerSecretKey, accesToken, accesSecretToken)

    # Se hace una busqueda de tweets de una serie o una pelicula, y twython responde con un objeto JSON
    result = twitter.search(q=title, lang = "en", result_type = "recent")
    # Se crea un diccionario vacio donde se guardaran los tweets obtenidos
    comments = {}
    # Es un identificador de cada tweet dentro del diccionario
    userid = 0
    # Se crea un diccionario vacio donde se guardaran los datos que conforman a el tweet de un usuario
    user = {}
    # Se crea una lista con los componentes que se quieren obtener de un tweet
    names = ('name','text','image','user')
    
    # Se recorre el objeto JSON obtenido anteriormente en busca de los elementos de la lista "names"
    for status in result["statuses"]:
        # Se agregan como "llaves" del diccionario los elementos de la lista "names"
        user = user.fromkeys(names)
        # El identificador del tweet incrementa en 1
        userid +=1
        # Se asigna el valor para la llave "name" del tweet en cuestion
        user['name'] = status["user"]["name"]
        # Se asigna el valor para la llave "text" del tweet en cuestion
        user["text"] = status["text"]
        # Se asigna el valor para la llave "image" del tweet en cuestion
        user["image"] = status["user"]["profile_image_url"]
        # Se asigna el valor para la llave "user" del tweet en cuestion
        user["user"] = status["user"]["screen_name"]
        # Se asigna el identificador del tweet
        comments[userid] = user
        
    return json.dumps(comments), 200


if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el servicio
    port = int(os.environ.get('PORT', 8085))
    # Se habilita la opción de 'debug' para visualizar los errores
    app.debug = True
    # Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port=port)
