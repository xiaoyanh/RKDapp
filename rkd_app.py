import json
import torch
from PIL import Image
import streamlit as st
from clf import predict
from torchvision import transforms
from load_model_app import load_model

# Create Titles Etc.
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("RKD Image Classification App")
st.write("")

file_up = st.file_uploader("Upload an image", type="jpg")

# load json file
with open('ind_to_label.json') as f:
    ind_to_label = json.load(f)
    # convert keys to int
    ind_to_label = {int(k): v for k, v in ind_to_label.items()}

# create dictionary
info = {
    'checkpoint': 'dataset=RKDMuseum-net=ResNet50-lr=0p01-examples_per_class=None-num_classes=499-train_seed=0-forward_class=Classification-epoch=96.pth',
    'net': 'ResNet50',
    'num_classes': len(ind_to_label.keys()),
    'resnet_type': 'big',
    'pretrained': False,
    'input_ch': 3,
    'device': torch.device("cuda:0" if torch.cuda.is_available() else "cpu"), }

# convert dictionary to object
info = type('obj', (object,), info)

# load model and transform
model = load_model(info)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])

if file_up is not None:
    image = Image.open(file_up)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Top 10 Predictions:")

    # TO DO: Move the model loading outside the file uploader
    labels = predict(file_up, model, transform, ind_to_label)

    # print out the top 5 prediction labels with scores
    for i in labels:
        bold_lab = st.markdown("PREDICTION: "+'**'+i[0]+'**'+" || SCORE (Out of 100): *"+str(i[1])+"*")