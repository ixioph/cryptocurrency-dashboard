'''
    net.py
        This module defines the recursive neural net with LSTM
'''

import torch.nn.functional as F
import torch.nn as nn
import torch

# TODO: 

class Net(nn.Module):
    batch_size = 2
    epochs = 15
    seq_len = 30

    def __init__(self):
        super(Net, self).__init__()
        # 1 kernal image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # an affine operation: y = wx + b
        self.fc1 = nn.Linear(16 * 6 * 6, 120) # 6x6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2,2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension (0)
        num_features = 1
        for s in size:
            num_features *= s
        return num_features











# EOF
