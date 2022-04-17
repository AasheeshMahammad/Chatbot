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

bot_name = "Mr.Rebot"

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
    #fix this
    limit = 2
    while(True):
        data=show_locs(latitude,longitude,limit)
        print(f"{bot_name}: Enter choice between 1-{len(data)} to confirm your appoinment at that service center any other number to show 2 more centers which might be closer to your location")
        print("U: ",end=' ')
        choice=int(input())
        if(choice>0 and choice<=len(data)):
            return data[choice-1]            
        else:
            limit+=2
            clear_screen(2)
            print(f"{bot_name}: Hi Welcome to appointment Booking Section")
            loc = Nominatim(user_agent="GetLoc")
            print(f"{bot_name}: Please enter an area where you would like to search the nearby service centers")
            print("U: ",lc)
    

def book_appointment():
    clear_screen(2)
    print(f"{bot_name}: Hi Welcome to appointment Booking Section")
    loc = Nominatim(user_agent="GetLoc")
    print(f"{bot_name}: Please enter an area where you would like to search the nearby service centers. enter quit to quit")
    print("U: ",end=' ')
    lc = input()
    if lc.lower()=="quit": exit(0)
    getLoc = loc.geocode(lc)
    latitude = getLoc.latitude
    longitude = getLoc.longitude
    choosen=locations(latitude,longitude,lc)
    print(f"{bot_name}: Appointment confirmed at",choosen["title"])
    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")
    lapname = input("Enter Laptop name and model: ")
    insertdb(fname,lname,lapname,choosen['title'],choosen['address']['label'])
    print(f"{bot_name}: Thanks for the info, your issue has been reported.\nYour appointment is booked for tomorrow.")
    exit(0)

if __name__=="__main__":
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    d1={}
    all_prev_tags=[]
    all_prev_probs=[]
    quits=False
    print(f"{bot_name}: Hi!\nI'm {bot_name}!\nI might be able to solve your problem with your laptop.\nAsk a question or type 'quit' to exit")
    autCorrect = AutoCorrect()

    asked = False

    while quits==False:
        print()
        #start
        sentence = input("U: ").lower()
        if sentence == "quit":
            quits=True
            print(f"{bot_name}: Thank You! Have a great day!")
            break

        #calculate tag
        sentence = tokenize(sentence)
        sentence = [autCorrect.correct_word(word) for word in sentence]
        x = bag_of_words(sentence,all_words)
        x = x.reshape(1,x.shape[0])
        x = torch.from_numpy(x).to(device)
        output = model(x)
        _, predicted = torch.max(output, dim=1)   
        tag = tags[predicted.item()]        #predicted tag
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted]
        fina_prob=prob.item()       #final probability of predicted tag

        print(tag)

        if fina_prob > 0.44:

            if tag=="appointment":
                print(f"{bot_name}: Looks like you need an appointment. Type yes to confirm, anything else to retry.")
                ap = input("U: ").lower()
                if(ap=="yes"):
                    print(f"{bot_name}: Taking you to a service center appointment part...")                                                      
                    book_appointment()
                else:
                    print(f"{bot_name}: Ask me a question.")
                    continue

            #if answer not accepted or question is repeated
            elif asked==True and (tag=="disagree" or (len(all_prev_tags)>0 and tag==tags[all_prev_tags[-1].item()] and tag in d1)):
                
                predicted=all_prev_tags[-1]
                tag=tags[predicted.item()]
                fina_prob=all_prev_probs[-1]
                if(len(d1[tag])==5):
                #if all responses are exhausted then do this:
                    quit=True
                    print(f"{bot_name}: All possible solutions have been tried.\nType 'yes' to go ahead to book an appoinment, anything else to continue.")
                    print("U :",end=' ')
                    ch=input().lower()
                    if(ch=="yes"):
                        print(f"{bot_name}: Taking you to a service center appointment part...")                                                      
                        book_appointment()
                    else:
                        print(f"{bot_name}: Maybe I can help you with any other problem that your laptop is facing. Ask your query.")
                        quit = False
                        continue

            else:
                if tag not in ["greeting","goodbye","funny","thanks","filler","agree","disagree","appointment","none"]:
                    all_prev_tags.append(predicted)
                    all_prev_probs.append(fina_prob)

                #search for responses for a given tag
                for intent in intents["intents"]:
                    if tag == intent["tag"]: 
                        #if the question isn't asked before
                        picks=random.choice(intent['responses'])
                        if(tag not in d1 ):
                            if(tag=="agree" or tag=="thanks") and asked==True:
                                asked = False
                                all_prev_tags=[]
                                all_prev_probs=[]
                                d1={}
                            elif(tag not in ["greeting","goodbye","funny","thanks","filler","agree","disagree","appointment","none"]):
                                d1[tag]=[picks] #add to previously given responses
                                asked = True

                        else: #if question is repeated
                            if(tag not in ["greeting","goodbye","funny","thanks","filler","agree","disagree","appointment","none"]):
                                while(len(d1[tag])<5 and picks in d1[tag]):
                                    picks=random.choice(intent['responses'])
                                d1[tag].append(picks)

                        print(f"{bot_name}: {picks}")
                        if(tag=="goodbye"):
                            quits=True
                        break
                    else: continue
        else:
            quits = True
            #if query isnt strictly matching with any tag then do this:
            print(f"{bot_name}: No solution found for your query.\nType 'yes' to go ahead to book an appoinment, anything else to continue.")
            print("U :",end=' ')
            ch=input().lower()
            if(ch=="yes"):
                print(f"{bot_name}: Taking you to a service center appointment part...")                                                      
                book_appointment() 
            else:
                quits = False
                continue      
