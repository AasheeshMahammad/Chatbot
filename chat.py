import random, json, torch
from model import NeuralNet
from utils import bag_of_words, tokenize
from geopy.geocoders import Nominatim
import requests
import os
from time import sleep
device = torch.device('cuda' if torch.cuda.is_available()  else 'cpu')
with open("intents.json",'r') as f:
    intents = json.load(f)
file = "data.pth"
data = torch.load(file)

def clear_screen():
    sleep(5)
    os.system('cls')

def locations():    
    loc = Nominatim(user_agent="GetLoc")
    print(f"{bot_name}: Please enter an area where you would like to search the nearby service centers")
    print("User:",end=' ')
    lc = input()
    getLoc = loc.geocode(lc)
    latitude = getLoc.latitude
    longitude = getLoc.longitude
    URL = "https://discover.search.hereapi.com/v1/discover"
    api_key = "d6-oHLamtfluzYmMSL86mPgCa6QQrVu7-zfzexMgNKk" 
    query = 'Laptop Service'
    limit = 10
    PARAMS = {'apikey':api_key,'q':query,'limit': limit,'at':'{},{}'.format(latitude,longitude)}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    data = list(data["items"])
    data.sort(key=lambda x:int(x["distance"]))
    print("---------------------------------------------")
    for i in data:
        # print(i)
        if "contacts" in i:
            if "mobile" in i["contacts"][0]:
                print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m\nContact:{i['contacts'][0]['mobile'][0]['value']}")
            elif "phone" in i["contacts"][0]:
                print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m\nContact:{i['contacts'][0]['phone'][0]['value']}")
            else:	print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m")
        else:	print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m")
        print("---------------------------------------------")

def book_appointment():
    clear_screen()
    print(f"{bot_name}: Hi Welcome to appointment Booking Section")
    locations()

if __name__=="__main__":
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]
    ded=False
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    bot_name = "Mr.Rebot"
    d1={}
    all_prev_tags=[]
    all_prev_probs=[]
    quits=False
    print("type quit to exit")
    while ded==False and quits==False:
        print()
        sentence = input("request : ").lower()
        if sentence == "quit":
            quits=True
            break
        sentence = tokenize(sentence)
        x = bag_of_words(sentence,all_words)
        x = x.reshape(1,x.shape[0])
        x = torch.from_numpy(x).to(device)
        output = model(x)
        _, predicted = torch.max(output, dim=1)   
        tag = tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted]
        fina_prob=prob.item()
        print(tag)
        if(tag=="disagree" and len(all_prev_tags)>0):
            predicted=all_prev_tags[-1]
            tag=tags[predicted.item()] 
            fina_prob=all_prev_probs[-1]           
        elif(tag=="agree" or tag=="thanks"):
            all_prev_tags=[]
            all_prev_probs=[]
        else:
            all_prev_tags.append(predicted)
            all_prev_probs.append(fina_prob) 
        print("Tag decided now is :",tag,"Prob of which is :",fina_prob)    
        if fina_prob > 0.95:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    if(tag not in d1):
                        picks=random.choice(intent['responses'])
                        d1[tag]=[picks]
                        print(f"{bot_name}: {picks}")
                    else:                    
                        if(len(d1[tag])==5):
                            print(f"{bot_name}: All possible solutions have been tried So taking you to a service center appointment part in 5 seconds")
                            ded=True
                            book_appointment()
                        else:
                            picks=random.choice(intent['responses'])
                            while(len(d1[tag])<5 and picks in d1[tag]):
                                picks=random.choice(intent['responses'])
                            d1[tag].append(picks)
                            print(f"{bot_name}: {picks}")
                    if(tag in ["goodbye","thanks"]):
                        quits=True
                else: continue
        else:
            print(f"{bot_name}: No solution found for your query So taking you to a service center appointment part in 5 seconds")
            ded=True
    if(quits==False):
        book_appointment()


