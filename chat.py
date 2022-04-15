import random, json, torch
from AutoCorrect import AutoCorrect
from model import NeuralNet
from utils import bag_of_words, tokenize, insertdb
from geopy.geocoders import Nominatim
import requests
import os
from time import sleep

device = torch.device('cuda' if torch.cuda.is_available()  else 'cpu')
with open("intents.json",'r') as f:
    intents = json.load(f)
file = "data.pth"
data = torch.load(file)

def clear_screen(duration):
    sleep(duration)
    os.system('cls')
def show_locs(latitude,longitude,limit):
    URL = "https://discover.search.hereapi.com/v1/discover"
    api_key = "d6-oHLamtfluzYmMSL86mPgCa6QQrVu7-zfzexMgNKk" 
    query = 'Laptop Service'
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
    return data

def locations(latitude,longitude,lc): 
    limit = 2
    while(True):
        data=show_locs(latitude,longitude,limit)
        print(f"{bot_name}: Enter choice between 1-{limit} to confirm your appoinment at that service center any other number to show 2 more centers which might be closer to your location")
        print("User:",end=' ')
        choice=int(input())
        if(choice>=0 and choice<=limit):
            return data[choice-1]            
        else:
            limit+=2
            clear_screen(1)
            print(f"{bot_name}: Hi Welcome to appointment Booking Section")
            loc = Nominatim(user_agent="GetLoc")
            print(f"{bot_name}: Please enter an area where you would like to search the nearby service centers")
            print("User:",lc)
    

def book_appointment():
    clear_screen(5)
    print(f"{bot_name}: Hi Welcome to appointment Booking Section")
    loc = Nominatim(user_agent="GetLoc")
    print(f"{bot_name}: Please enter an area where you would like to search the nearby service centers")
    print("User:",end=' ')
    lc = input()
    getLoc = loc.geocode(lc)
    latitude = getLoc.latitude
    longitude = getLoc.longitude
    choosen=locations(latitude,longitude,lc)
    print("Appointment confirmed at",choosen["title"])
    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")
    lapname = input("Enter Laptop name and model: ")
    insertdb(fname,lname,lapname,choosen['title'],choosen['address']['label'])
    exit(0)

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
    autCorrect = AutoCorrect(all_words)
    while ded==False and quits==False:
        print()
        sentence = input("U : ").lower()
        if sentence == "quit":
            quits=True
            break
        sentence = tokenize(sentence)
        sentence = [autCorrect.correctWord(word) for word in sentence]
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
            d1={}
        else:
            all_prev_tags.append(predicted)
            all_prev_probs.append(fina_prob) 
        print("Tag decided now is :",tag,"Prob of which is :",fina_prob)    
        if fina_prob > 0.7:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    if(tag not in d1 ):
                        picks=random.choice(intent['responses'])
                        if(tag not in ["greeting","goodbye","funny","thanks","filler","agree","disagree","appointment"]):
                            d1[tag]=[picks]
                        print(f"{bot_name}: {picks}")
                    else:                    
                        if(len(d1[tag])==5):
                            ded=True
                            print(f"{bot_name}: All possible solutions have been tried. Would You Like to go ahead to book an appointment at a Service Centre")
                            print(f"{bot_name}: Enter Yes or No only")
                            print("U :",end=' ')
                            ch=input().lower()
                            if(ch=="yes"):
                                print("So taking you to a service center appointment part in 5 seconds")                                                      
                                book_appointment()
                            else:
                                exit(0)
                        else:
                            picks=random.choice(intent['responses'])
                            if(tag not in ["greeting","goodbye","funny","thanks","filler","agree","disagree","appointment"]):
                                while(len(d1[tag])<5 and picks in d1[tag]):
                                    picks=random.choice(intent['responses'])
                                d1[tag].append(picks)
                            print(f"{bot_name}: {picks}")
                    if(tag in ["goodbye","thanks"]):
                        quits=True
                else: continue
        else:
            ded=True
            print(f"{bot_name}: No solution found for your query. Type Yes to go ahead to book an appoinment No to stop")
            print("U :",end=' ')
            ch=input().lower()
            if(ch=="yes"):
                print("So taking you to a service center appointment part in 5 seconds")                                                      
                book_appointment() 
            else:
                exit(0)      

    if(quits==False):
        book_appointment()


