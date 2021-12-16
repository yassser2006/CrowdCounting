# from keras.initializers import glorot_uniform
from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Reading the model from JSON file
with open('Model_AKL_700_epochs_Adadelta.json', 'r') as json_file:
    json_savedModel = json_file.read()

# load the model architecture
model = tf.keras.models.model_from_json(json_savedModel)
# model.summary()

model.load_weights("model_700_epochs_Adadelta_weights.h5")


# showing loaded weights
# for layer in model.layers:
#     print(layer.get_weights())
#     break

# we will get this as a parameter


def test_image_generator(img_path):
    while True:
        batch_input = []
        inputt = get_input(img_path)
        batch_input += [inputt]
        batch_x = np.array(batch_input)
        yield batch_x
        return


def get_input(path):
    # path = path[0]
    img = create_img(path)
    return img


def create_img(path):
    # Function to load,normalize and return image
    im = Image.open(path).convert('RGB')
    im = np.array(im)
    im = im / 255.0
    im[:, :, 0] = (im[:, :, 0] - 0.485) / 0.229
    im[:, :, 1] = (im[:, :, 1] - 0.456) / 0.224
    im[:, :, 2] = (im[:, :, 2] - 0.406) / 0.225
    # print(im.shape)
    # im = np.expand_dims(im,axis  = 0)
    return im


def predict(img_path):
    print(img_path)
    img_generator = test_image_generator(img_path)
    predicted_density = model.predict(img_generator)
    predicted_img = predicted_density[0]
    count = np.sum(predicted_density[0])
    return predicted_img, count








# img_generator = test_image_generator('static/images/IMG_1.jpg')
# predicted_density = model.predict(img_generator)
# print(type(predicted_density[0]))
# print(predicted_density[0].shape)
#
#
#
#
# import matplotlib.pyplot as plt
# plt.imshow(predicted_density[0]) #Needs to be in row,col order
# plt.axis('off')
# plt.tight_layout()
# plt.savefig("static/density/IMG_1_density.jpg")
#


#
# import cv2
# import numpy as np
# img = predicted_density[0] * 255
# cv2.imwrite("filename.png", img)
# plt.imshow(predicted_density[0])
# plt.show()
# print(predicted_density.shape)
# print(np.sum(predicted_density[0]))
