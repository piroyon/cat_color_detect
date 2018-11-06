# cat_color_detect
#### Detection of cats coat color with Keras + Tensorflow
- Python 3.6.6
- Tensorflow 1.9.0
- Keras 2.2.0

### Collect images for learning

- bing_image_collector.py
- excite_image_collector.py

Keyword 'cat' is already included. Please give a keyword of cat coat color.

`$ python3 bing_image_collector.py redtabby`

### Detect cat's face

- cat_detect.py

You need 'cascade.xml' from https://github.com/wellflat/cat-fancier

`$ python3 cat_detect.py -c cascade.xml`

### Learning...

- data_create.py

`$ python3 data_create.py cat_image`

```
cat_image
├── abyssinian
│   ├── 0007d22a55cfc57324d016c79cd0187633a82a87b488c53e9b6a2f353b6df3ef_1.jpg
│   ├── 00d8fd2354399f392092591bf6b318b92fe9a6ff47a0c8ed007feca94984d2e3_0.jpg
│   ├── 01dd09d760342a8cbce6c123dfe47fb5b99091c9041361b4fd4348135920455d_0.jpg
│   ├── 01f8334dd373aa3ff0f1098f13f9482f9af9850ee9938ca57d2036ee72da951c_0.jpg...
├── black
├── browntabby
├── browntabbywhite
├── calico
├── cream
├── lynxpoint
├── mask
├── redtabby
├── russianblue
├── sealpoint
├── silvertabby
├── tortie
└── white
```

- training.py

data_create.py makes "cat_color.np"

` $ pytyon3 training.py cat_image cat_color.np`

### Testing...

- test.py
