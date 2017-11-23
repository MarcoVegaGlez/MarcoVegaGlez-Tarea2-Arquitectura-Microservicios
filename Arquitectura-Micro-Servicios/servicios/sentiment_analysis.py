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
import tweepy
from textblob import TextBlob

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

    auth = tweepy.OAuthHandler(consumerkey, consumerSecretKey)
    auth.set_access_token(accesToken, accesSecretToken)

    api = tweepy.API(auth)

    public_tweets = api.search(q=title, count=200)


    parsed_tweet = {}
    tendencia = 0

    for tweet in public_tweets:



     parsed_tweet['text'] = tweet.text
     parsed_tweet['user'] = tweet.user.screen_name
     parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
     if parsed_tweet['sentiment'] == "positive":
        tendencia = tendencia + 1
     elif parsed_tweet['sentiment'] == "negative":
        tendencia = tendencia - 1

    str_tendencia = " "
    if tendencia > 0:
        str_tendencia = "Positive"
    elif tendencia == 0:
        str_tendencia = "Neutral"
    else:
        str_tendencia = "Negative"


    print tendencia

    json_final = {"Trend" : str_tendencia, "num_tweets" : len(public_tweets)}




    return json.dumps(json_final), 200




def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'





if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el servicio
    port = int(os.environ.get('PORT', 8086))
    # Se habilita la opción de 'debug' para visualizar los errores

    app.debug = True
    # Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port=port)
