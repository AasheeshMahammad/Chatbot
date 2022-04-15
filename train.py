import json
from utils import bag_of_words, tokenize, stem, init_db
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet

df = "intents.json"
init_db()
with open(df) as file:
    intents = json.load(file)

all_words = []
tags = []
train_data = []
for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        train_data.append((w,tag))

punctuations = {'?','!','.',','}
all_words = [stem(w).lower() for w in all_words if w not in punctuations]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []
Y_train = []

for pattern_sentence,tag in train_data:
    bag = bag_of_words(pattern_sentence,all_words)
    X_train.append(bag)
    label = tags.index(tag)
    Y_train.append(label)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

class ChatDataset(Dataset):
    
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_train

    def __getitem__(self,index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples
    
batch_size = 8
input_size = len(all_words)
hidden_size = 8
output_size = len(tags)
learning_rate = 0.001
epochs = 1000

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(epochs):
    for words, labels in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        output = model(words)
        loss = criterion(output, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if (epoch+1)%100 == 0:
        print(f"epoch {epoch+1}/{epochs}, loss = {loss.item():.4f}")
print(f"final loss, loss = {loss.item():.4f}")

data = {
    "model_state":model.state_dict(),
    "input_size":input_size,
    "output_size":output_size,
    "hidden_size":hidden_size,
    "all_words":all_words,
    "tags":tags
}

file = "data.pth"
torch.save(data,file)
print(f"training is complete and model saved to {file}")

