import torch
import torchvision
import torch.nn as nn  
import torch.optim as optim 
import torch.nn.functional as F   
from torch.utils.data import (DataLoader,)  
import torchvision.datasets as datasets  
import torchvision.transforms as transforms  
from dataset import CatsAndDogsDataset
import os
import pandas as pd

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def get_mean_std(loader):
    channel_sum, channel_squared_sum, num_batches = 0,0,0
    print(loader)
    for data, _ in loader:
        print('enter')
        channel_sum += torch.mean(data,dim= [ 0,2,3])
        channel_squared_sum = torch.mean(data**2,dim= [ 0,2,3])
        num_batches += 1

    mean = channel_sum/num_batches
    std = (channel_squared_sum/num_batches - mean**2)**0.5

    return  mean,std

class Identity(nn.Module):
    def __init__(self):
        super(Identity, self).__init__()

    def forward(self, x):
        return x

def train(model,device,train_loader,criterion, optimizer,epoch):
    model.train()
    for i ,(data,targets) in enumerate(train_loader):
        data,targets = data.to(device), targets.to(device)
        outputs = model(data)
        loss = criterion(outputs,targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if i%20 ==0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(epoch, i * len(data), len(train_loader.dataset),
                                            100. * i / len(train_loader), loss.item()))
def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item() # sum up batch loss
            pred = output.max(1, keepdim=True)[1] # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(test_loss, correct, len(test_loader.dataset),
                                                         100. * correct / len(test_loader.dataset)))

def main():
# Hyperparameters
    num_classes = 2
    learning_rate = 1e-3
    batch_size = 32
    num_epochs = 6
    my_transform = transforms.Compose([ transforms.ToPILImage(),
                                        transforms.Resize((224,224)),
                                       transforms.ToTensor()])

    path = os.getcwd()
    label_path = 'label.csv'
    data_path = path + '/Dataset/train'
    datasets = CatsAndDogsDataset(label_path,data_path,
                             transform= my_transform)
    print(len(datasets))
    train_set,test_set = torch.utils.data.random_split(datasets,[2,0])
    train_loader = DataLoader(dataset = train_set, batch_size = batch_size,shuffle= True)
    test_loader = DataLoader(dataset = test_set, batch_size = batch_size,shuffle= True)

 #   mean,std = get_mean_std(train_loader)
 #   print(mean,std)
    model = torchvision.models.resnet18(pretrained=True)

    for param in model.parameters():
        param.requires_grad = False

    # changing last year 
    model.avgpool = Identity()
    model.classifier = nn.Sequential(
        nn.Linear(512, 100), nn.ReLU(), nn.Linear(100, num_classes)
    )

    model.to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # after every 4 epoch we change our learning rate by factor 0.1
    schedular = optim.lr_scheduler.StepLR(optimizer,step_size= 4, gamma = 0.1)

    # traning model and finding it accuracy after each epoch
    for epoch in range(num_epochs):
        print("traning model")
        train(model,device,train_loader,criterion,optimizer,schedular)
        schedular.step()
        test(model,device,test_loader)

if __name__ == '__main__':
    main()
