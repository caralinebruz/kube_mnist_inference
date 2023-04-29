#!/usr/bin/env python3

# model
from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

import os
from mnist import Net
from PIL import Image


def get_model():
	# loads model file from disk
	device = 'cpu'
	model = Net().to(device)

	model_dir = os.environ.get('MODEL_DIR')
	dir_list = os.listdir(model_dir)
	file = dir_list[0]
	print("File in directory is ", file)
	fullpath = model_dir + "/" + file

	model.load_state_dict(torch.load(fullpath))
	model.eval()

	# Print model's state_dict
	print("Model's state_dict:")
	for param_tensor in model.state_dict():
		print(param_tensor, "\t", model.state_dict()[param_tensor].size())

	return model



def load_image(filepath: str) -> torch.Tensor:
	# converts image to PIL which is required
	image = Image.open(filepath).convert("L")
	preprocess = transforms.Compose([
		transforms.Resize(28),
		transforms.CenterCrop(28),
		transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485], std=[0.229])  # for grayscale image
        transforms.Normalize((0.1307,), (0.3081,))
	])
	return preprocess(image).unsqueeze(0)



def run_inference(filepath: str, model_path: str) -> int:
	# runs inference
	device = 'cpu'
	image_tensor = load_image(filepath).to(device)

	model = Net().to(device)
	model.load_state_dict(torch.load(model_path))
	model.eval()

	print(model)

	with torch.no_grad():
		output = model(image_tensor)
		_, predicted_class = torch.max(output, 1)

	return predicted_class.item()



def inference(image_path):

	# load the model from storage
	# model = get_model()
	model_dir = os.environ.get('MODEL_DIR')
	model_file = os.listdir(model_dir)[0]
	model_path = model_dir + "/" + model_file

	predicted_class = run_inference(image_path, model_path)
	outstring = (f"Its predicted class is: {predicted_class}")
	print(outstring)

	return outstring