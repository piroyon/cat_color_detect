# cat_color_detect
#### detection of cats color with Keras + Tensorflow
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
- training.py

### Testing...

- test.py
