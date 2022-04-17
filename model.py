import torch.nn as nn

class NeuralNet(nn.Module):

    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, hidden_size)
        self.l4 = nn.Linear(hidden_size, num_classes)
        self.leakyRelu = nn.LeakyReLU()

    def forward(self, x):
        out = self.leakyRelu(self.l1(x))
        out = self.leakyRelu(self.l2(out))
        out = self.leakyRelu(self.l3(out))
        out = self.l4(out)
        return out

