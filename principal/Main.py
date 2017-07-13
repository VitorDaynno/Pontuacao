#Vitor Daynno 16/06/2017
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from trello import TrelloApi
from Config import Config

cliente = MongoClient('localhost',27017)
banco = cliente['Pontuacao']
tabela = banco['tarefas']

config = Config()
trello = TrelloApi(config.get_Api_Key(),'none')  #API Key
trello.set_token(config.get_Token()) #Token
id = 0

for quadro in config.get_Quadros():
    board = trello.boards.get(str(quadro))
    print "\nQuadro: " + board["name"]
    lista = trello.boards.get_list(quadro)
    print '  Lista: '+lista[len(lista)-2]["name"]
    cards = trello.lists.get_card(lista[len(lista)-2]["id"])
    for card in cards:
        print '   Card: '+card["name"]
        card_Detalhes = trello.cards.get_action(card["id"])
        try:
           if card_Detalhes[0]["data"]["text"][:11] == "Dificuldade":
                print card_Detalhes[0]["data"]["text"][13:]
                if card_Detalhes[0]["data"]["text"][13:].encode('utf-8') == "Fácil":
                    tabela.insert_one({"_id":id,"nome": card["name"], "pontos": 1})

                elif card_Detalhes[0]["data"]["text"][13:].encode('utf-8') == "Média":
                    tabela.insert_one({"_id":id,"nome" : card["name"], "pontos":  2 }) 

                elif card_Detalhes[0]["data"]["text"][13:].encode('utf-8') == "Difícil":
                    tabela.insert_one({"_id":id,"nome" : card["name"], "pontos":  3 }) 
                #mudar = trello.cards.update_idList(card["id"],lista[len(lista)-1]["id"])
                print '     Computado com sucesso'
           elif card_Detalhes[0]["data"]["text"][:6] == "Pontos":
                print int(card_Detalhes[0]["data"]["text"][8:])
                tabela.insert_one({"_id":id,"nome" : card["name"], "pontos": int(card_Detalhes[0]["data"]["text"][8:])})
           id = id + 1
        except KeyError:
             print '     Falha ao computar'
