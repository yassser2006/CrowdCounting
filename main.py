from flask import Flask, render_template, request
from matplotlib import pyplot as plt

from Prediction import predict
app = Flask(__name__)


@app.route('/', methods=['GET'])
def start():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict_count():
    imagefile = request.files['imagefile']
    image_path = './static/images/' + imagefile.filename
    imagefile.save(image_path)
    img, count = predict(image_path)
    image_path = image_path[2:]

    plt.imshow(img)  # Needs to be in row,col order
    plt.axis('off')
    plt.tight_layout()
    dens_path = 'static/density/'+ 'density' + imagefile.filename
    plt.savefig(dens_path)
    return render_template('index.html', prediction=count, realimg=image_path, densityimg=dens_path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port=3000, debug=True)

# app
if __name__ == '__main__':
    print('hiPyCharm')
