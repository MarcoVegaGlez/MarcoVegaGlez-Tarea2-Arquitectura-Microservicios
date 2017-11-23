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
#           |    Procesador de      |    contenga información |   IMDb.                |
#           |     comentarios       |    detallada de pelí-   | - Devuelve un JSON con |
#           |      de Twitter       |    culas o series en    |   datos de la serie o  |
#           |                       |    particular.          |   pelicula en cuestión.|
#           +-----------------------+-------------------------+------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8084/api/v1/information?t=matrix
#
import os
from flask import Flask, abort, render_template, request
from twython import Twython
import urllib, json

app = Flask(__name__)




@app.route("/api/v1/information")
def get_tweets():
    """
    Este método obtiene información acerca de una película o serie
    específica.
    :return: JSON con la información de la película o serie
    """
    # Se lee el parámetro 't' que contiene el título de la película o serie que se va a consultar
    title = request.args.get("t")
    #api_key = '7aed8d98'
    consumerkey = "4NSUdUvAh5zVofUgoPTpLAWIR"
    consumerSecretKey = "9QCWVUexXwZWMlFucJzw0aT4e092OQkKp1Au7j1JqIobxrVeXA"
    accesToken = "399643418-7zUPZXiglJweB2yfYJN9WlBdVwyDxKYWC0hpKYKf"
    accesSecretToken = "Up4YyniBoZRf7in2YroFhJgXAFky9I0XRthVLFY2BNbXS"

    twitter = Twython(consumerkey, consumerSecretKey, accesToken, accesSecretToken)

    result = twitter.search(q=title, lang = "en", result_type = "mixed")
    comments = {}
    userid = 0
    user = {}
    names = ('name','text','image','user')
    for status in result["statuses"]:
        user = user.fromkeys(names)
        userid +=1
        user['name'] = status["user"]["name"]
        user["text"] = status["text"]
        user["image"] = status["user"]["profile_image_url"]
        user["user"] = status["user"]["screen_name"]
        comments[userid] = user

    #url_base = 'https://api.twitter.com/1.1/search/tweets.json' + '&t=' + '&result_type=recent' #'http://www.omdbapi.com/?apikey=' + api_key + '&t='
    # Se conecta con el servicio de IMDb a través de su API
    #url_comments = urllib.urlopen(url_base + title + "&plot=full&r=json")
    # Se lee la respuesta de IMDb
    #json_comment = comment.read()
    # Se convierte en un JSON la respuesta recibida
    #comment = json.loads(comments)
    # Se regresa el JSON de la respuesta
    return json.dumps(comments), 200


if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el servicio
    port = int(os.environ.get('PORT', 8085))
    # Se habilita la opción de 'debug' para visualizar los errores
    app.debug = True
    # Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port=port)
