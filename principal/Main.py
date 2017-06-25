#Vitor Daynno 16/06/2017

from trello import TrelloApi
from Config import Config

config = Config()
trello = TrelloApi(config.get_Api_Key(),'none')  #API Key
trello.set_token(config.get_Token()) #Token
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
           if str(card_Detalhes[0]["data"]["text"]) == "u":
                mudar = trello.cards.update_idList(card["id"],lista[len(lista)-1]["id"])
                print '     Computado com sucesso'
        except KeyError:
             print '     Falha ao computar'
