from fastapi import FastAPI #import FastAPI class 
from uuid import uuid4 #import uuid4 function, allows each game to have unique id
from datetime import datetime


app = FastAPI()

# Storage
#--------------
games = {}
players = {}
transactions = {}

@app.get("/health") #if someone pings the /health endpoint, it runs health function, which returns a json object with "ok": True, indicating the server is healthy and running
def health():
    return {"ok": True}

#Games
#---------------
@app.post("/games") #If someone sends post request to /games, it runs create_game function
def create_game(name: str):
    game_id = str(uuid4()) #creates unique id for the game using uuid4 function
    games[game_id] = {  #creates game object in the games dictionary with a dictionary containing the id as key and name as the value
        "id": game_id,
        "name":name
    }
    return games[game_id] #returns game object with id and name in json format


@app.get("/games")
def list_games():
    return list(games.values()) #returns list of all game objects

#Players
#-----------------
@app.post("/games/{game_id}/players") #for post requests made to players in a game specified by game_id
def add_player(game_id: str, name: str):
    if game_id not in games:
        return {"error": "Game not found"} #if game id not in games dictionary, error
    
    player_id = str(uuid4()) #creates unique id for player
    players[player_id] = {
        "id": player_id,
        "name": name,
        "game_id": game_id
    }    
    return players[player_id]

@app.get("/games/{game_id}/players")
def list_players(game_id: str):
    return [player for player in players.values() if player["game_id"] == game_id] 
    #returns list of player for each player in players dictionary, but only if the player's game_id matches the game_id specified 

#Transactions
#-----------------
@app.post("/games/{game_id}/transactions")
def add_transactions(game_id: str, player_id: str, type: str, amount_cents: int): #adds transcation based on game, player, buy/cash, and amount
    if game_id not in games:
        return {"error": "Game not found"}
    if player_id not in players:
        return {"error": "Player not found"}
    if players[player_id]["game_id"] != game_id:
        return {"error": "Player does not belong to this game"}
    allowed_types = ["BUY_IN", "TOP_UP", "CASH_OUT"]
    if type not in allowed_types:
        return {"error": "Invalid transaction type"}
    if amount_cents <= 0:
        return {"error": "Amount must be greater than zero"}
    #ensures game and player exist, player belongs to game, transaction is valid

    tx_id = str(uuid4()) #creates unique id for transaction
    transactions[tx_id] = {
        "tx_id": tx_id,
        "game_id": game_id,
        "player_id": player_id,
        "type": type,
        "amount_cents": amount_cents,
        "created_at": datetime.utcnow().isoformat() #stores the time the transaction was created in ISO format
    }
    return transactions[tx_id]

@app.get("/games/{game_id}/transactions")
def list_transactions(game_id: str):
    return [tx for tx in transactions.values() if tx["game_id"] == game_id] 
    #returns list of transactions for each transaction in transactions dictionary that matches game_id
    
