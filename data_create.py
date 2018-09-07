from PIL import Image
import sys
import os, glob
import numpy as np
import random, math

def create(input_dir) :
    Image.LOAD_TRUNCATED_IMAGES = True
    categorys = []
    dir_list = os.listdir(input_dir)
    for index, dir_name in enumerate(dir_list):
      if dir_name == '.DS_Store' :
        continue
      categorys.append(dir_name)
    image_size = 160
    train_data = []
    for idx, category in enumerate(categorys):
      try :
        print("---", category)
        image_dir = input_dir + "/" + category
        files = glob.glob(image_dir + "/*.jpg")
        for i, f in enumerate(files):
            img = Image.open(f)
            img = img.convert("RGB")
            img = img.resize((image_size, image_size))
            data = np.asarray(img)
            train_data.append([data, idx])
      except:
        print("SKIP : " + category)

    random.shuffle(train_data)
    X, Y = [],[]
    for data in train_data:
      X.append(data[0])
      Y.append(data[1])
    print(len(X))
    test_idx = math.floor(len(X) * 0.8)
    print(test_idx)
    xy = (np.array(X[0:test_idx]), np.array(X[test_idx:]),
          np.array(Y[0:test_idx]), np.array(Y[test_idx:]))
    np.save("cat_color", xy)

if __name__ == "__main__":
  args = sys.argv
  input_dir = args[1]  #各カテゴリ画像データの上位ディレクトリ
  create(input_dir)
