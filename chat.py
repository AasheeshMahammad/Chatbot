import random, json, torch
from model import NeuralNet
from utils import bag_of_words, tokenize


device = torch.device('cuda' if torch.cuda.is_available()  else 'cpu')
with open("questions.json",'r') as f:
    intents = json.load(f)

file = "data.pth"
data = torch.load(file)
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
d1={}
bot_name = "Mr.Rebot"
all_prev_tags=[]
quits=False
print("type quit to exit")
while True and ded==False:
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
    if(tag=="disagree" and len(all_prev_tags)>0):
        predicted=all_prev_tags[-1]
        tag=tags[predicted.item()]
    elif(tag=="agree" or tag=="thanks"):
        all_prev_tags=[]
    else:
        all_prev_tags.append(predicted)
    #print(all_prev_tags)
    #print(d1)
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                if(tag not in d1):
                    picks=random.choice(intent['responses'])
                    d1[tag]=[picks]
                    print(f"{bot_name}: {picks}")
                else:                    
                    if(len(d1[tag])==5):
                        print(f"{bot_name}: All possible solutions have been tried would like you to visit a service center")
                        ded=True
                    else:
                        picks=random.choice(intent['responses'])
                        while(len(d1[tag])<5 and picks in d1[tag]):
                            picks=random.choice(intent['responses'])
                        d1[tag].append(picks)
                        print(f"{bot_name}: {picks}")
    else:
        print(f"{bot_name}: No solution found for your query would like you to visit a service center")
        ded=True
if(quits==False):
    print("Hi Welcome to appointment Booking Section")
    print("Here you find a idiot by the name of SVSC Santosh")


