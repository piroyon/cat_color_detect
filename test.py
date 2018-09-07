import training as train  #import 3.'s training.py
import sys, os
from PIL import Image
import numpy as np

if len(sys.argv) <= 1:
  quit()

image_size = 160
source_dir = "catimages"
categories = [name for name in os.listdir(source_dir) if name != ".DS_Store"]

X = []
for file_name in sys.argv[1:]:
  img = Image.open(file_name)
  img = img.convert("RGB")
  img = img.resize((image_size, image_size))
  in_data = np.asarray(img)
  X.append(in_data)
X = np.array(X)
model = train.train(X.shape[1:])
model.load_weights("./snapshot/cat-bestmodel.hdf5")
predict = model.predict(X)

for i, pre in enumerate(predict):
  y = pre.argmax()
  print(sys.argv[i+1], categories[y])
