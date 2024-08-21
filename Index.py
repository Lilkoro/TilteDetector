import requests
import keyboard
from datetime import datetime
import json


def Critère(gameb, player, g, kda, deco, win, enemyMissingPings): # A est pour Avarage : Moyenne
    LooseStreak = []
    Akda = 0
    Apings = 0
    print("ca marche la")
    for r in range(10):
        try:
            Akda = kda[r] + Akda
            if r == 9:
                Akda = Akda /10
                print(round(Akda))
        except:
            continue
    for s in range(10):
        try:
            Apings = enemyMissingPings[s] + Apings
            if s == 9:
                Akda = Akda /10
                print(round(Apings))
        except:
            continue
    if g == 5 : # mettre dans le json
        d ='' # pas finis

#50 request
def MatchFilterDate():

    poubelle = []
    for y in range(10): # récup les puuid des Bleu
        if y >= 5:
            y = y-5
            real_puuid = Summoners_Puuid_Red[y]
            name = Red_Team[y]
            print(y,'rouges')
        else :
            name = Blue_Team[y]
            real_puuid = Summoners_Puuid_Blue[y]
            print(y, 'bleus') # récup le puuid du joueur en index y
        gamep = 0 # compteur de game poubelle de y a 0
        gameb = 0 # compteur de game bonne de y a 0
        print("Les 5 games de : ", name," se font analyser") # info
        summoner_gameid = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{real_puuid}/ids?count=5&api_key={ak}" # requests : recup toute les games de y
        r2 = requests.get(summoner_gameid).json() #requests
        for g in range(5): # pour chaque game de y on a la gameid g
            gameid = r2[g] # id de la partie g sur 5
            summoner_gameinfo = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameid}?api_key={ak}" # requests pour avoir les infos de la partie
            r4 = requests.get(summoner_gameinfo).json() # requests
            #######################################################################
            gameday = r4["info"]["gameCreation"] / 1000 # jour de la partie en timestamp
            now = datetime.now() # moment ou le script est lancé
            timestamp = datetime.timestamp(now) # conversion en timestamp
            diff_time = timestamp - gameday # différence d'heure entre les games et le script launch
            if diff_time > 18000 : # vérifie si la game date de + de 5 heures
                gamep = gamep + 1 # si c'est le cas elle va a la poubelle, non exploitable
                print(gamep, "game à la poubelle")
                poubelle.append(gameid)
            else : # si elle est pas poubelle => 1691.5774776281676 1691 1289.879913675552 1288
                gameb = gameb + 1
                Listkda = []
                ListDeco = []
                ListEnemyMissingPings = []
                Listwin = []
                x = 0
                for h in range(10): # Cherche le player dans les 10 joueurs
                    player = r4["info"]["participants"][h]["summonerName"] # cherche le Nom du joueur y 
                    if player == summoner_name : # si le nom est trouvé  =>
                        ListPositionPlayer = h #trouve la position du joueur dans la liste
                        kda = round(r4["info"]["participants"][ListPositionPlayer]["challenges"]["kda"])
                        Listkda.append(kda)
                        time = r4["info"]["participants"][ListPositionPlayer]["challenges"]["gameLength"]
                        time_play = r4["info"]["participants"][ListPositionPlayer]["timePlayed"]
                        deco = time - time_play
                        if deco > 3 :
                            ListDeco.append(deco, time)
                        win = r4["info"]["participants"][ListPositionPlayer]["win"]
                        if win == False: 
                            Listwin.append(x+1)
                        enemyMissingPings = r4["info"]["participants"][ListPositionPlayer]["enemyMissingPings"]
                        ListEnemyMissingPings.append(enemyMissingPings)

                        Critère(gameb, player, g, Listkda, ListDeco, Listwin, ListEnemyMissingPings)
                        continue
                    else :
                        continue
        #print("La game : ", gameid , "\n a durée : ", round(r4["info"]["gameDuration"] / 60), " minute")
        #print("|------------------------------------------------------------------------------------------------------------------------------------------------------|")


#1 request
def IsInGame():
    summoner_data_spec = f"https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={ak}"
    while True:
        r1 = requests.get(summoner_data_spec).json()
        if "Data not found" in str(r1):
            print("Tu n'est pas en game")
            exit()
        elif "gameId" in str(r1):
            print("tu es en game parfait !")
            break
            


summoner_name0 = input("Pseudo in-game: ")
ak = "RGAPI-XXXXX-XXXXX-XXXX"

#1 request
summoner_data_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name0}?api_key={ak}"
r0 = requests.get(summoner_data_url).json()
if "Data not found - summoner not found" in str(r0):
    print("Joueur pas trouvé.")
    exit()
else:
    summoner_puuid = r0["puuid"]
    summoner_name = r0["name"]
    summoner_id = r0["id"]
    print(f"Information récuperé de {summoner_name} : \n puuid : {summoner_puuid}, \n id : {summoner_id}")

'''while True:
    if keyboard.is_pressed("ctrl+1"):
        IsInGame()
        notification.notify(
            title= "Tiltomète",
            message= "Script activé calcul !",
            app_icon= None,
            timeout= 5
        )
        break'''
#1 request
summoner_data_spec = f"https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={ak}"
r1 = requests.get(summoner_data_spec).json()

#10 request
if "Data not found" in str(r1):
    print("La personne recherché n'est pas en game (hormis championnat).")
    exit()
else:
    i= -1
    player_list= []
    Blue_Team= []
    Red_Team= []
    Summoners_Puuid_Red = []
    Summoners_Puuid_Blue = []
    
    while i <= 10 : 
        try:
            i=i+1
            Team = r1["participants"][i]["teamId"]
            summoners_name = r1["participants"][i]["summonerName"]
            summoner_data_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoners_name}?api_key={ak}"
            r3 = requests.get(summoner_data_url).json()
            puuid_gameplayer = r3["puuid"]
            player_list.append(summoners_name)
            if Team == 200:
                Summoners_Puuid_Red.append(puuid_gameplayer)
                Red_Team.append(summoners_name)
            elif Team == 100:
                Summoners_Puuid_Blue.append(puuid_gameplayer)
                Blue_Team.append(summoners_name)
        except:
            continue


print("|--------------------------------------------------|")
print(f"L'équipe blue side : {Blue_Team} \nL'équipe red side : {Red_Team}")
print("|--------------------------------------------------|")

#try :
MatchFilterDate()
#except :
