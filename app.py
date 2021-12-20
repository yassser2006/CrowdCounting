from flask import Flask, render_template, request
from matplotlib import pyplot as plt
import numpy as np
import cv2


from Prediction import predict, get_density_gt
app = Flask(__name__)


@app.route('/', methods=['GET'])
def start():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict_count():
    if request.method == 'POST':
        files = request.files.getlist('files[]')


        if len(files) == 1:
            imagefile = files[0]
            image_path = './static/images/' + imagefile.filename
            imagefile.save(image_path)
            img, count = predict(image_path)
            image_path = image_path[2:]
            plt.imshow(img)  # Needs to be in row,col order
            plt.axis('off')
            plt.tight_layout()
            dens_path = 'static/density/' + 'density' + imagefile.filename
            plt.savefig(dens_path, bbox_inches='tight', pad_inches=0)
            density_path_gt = dens_path
            #print("this is the path", imagefile.name)


            img = img * 255
            img = img.astype(np.uint8)
            real_img = cv2.imread('./static/images/' + imagefile.filename)
            width = real_img.shape[1]
            height = real_img.shape[0]
            dsize = (width, height)
            output = cv2.resize(img, dsize)
            masked = real_img + (output.reshape(real_img.shape[0], real_img.shape[1], 1) * 10)
            masked_path = 'static/masked/' + 'masked' + imagefile.filename
            cv2.imwrite(masked_path, masked)

            count = int(count)

            return render_template('index.html', prediction=count, realimg=image_path, densityimg=dens_path, maskedimg=masked_path)
        elif len(files) == 0:
            return "No file Selected"
        elif len(files) == 2:
            real_img = None
            density_img = None
            for file in files:
                if 'jpg' in file.filename:
                    real_img = file
                elif 'h5' in file.filename:
                    density_img = file
                else:
                    return 'you choosed wrong images'

            # print("real img", real_img.filename)
            # print("dens img", density_img.filename)
            real_img_filename = real_img.filename
            realimg_path = './static/images/' + real_img.filename
            real_img.save(realimg_path)

            density_path = './static/density_gt/' + density_img.filename
            density_img.save(density_path)

            img_density_gt, count_gt = get_density_gt(density_path)
            plt.imshow(img_density_gt)  # Needs to be in row,col order
            plt.axis('off')
            plt.tight_layout()
            density_path_gt = 'static/density_gt/' + 'temp.jpg'
            plt.savefig(density_path_gt,  bbox_inches='tight', pad_inches=0)

            img, count = predict(realimg_path)
            image_path = realimg_path[2:]
            plt.imshow(img)  # Needs to be in row,col order
            plt.axis('off')
            plt.tight_layout()
            dens_path = 'static/density/' + 'density' + real_img.filename
            plt.savefig(dens_path, bbox_inches='tight', pad_inches=0)
            # density_path_gt = dens_path
            #print("this is the path", real_img.name)

            img = img * 255
            img = img.astype(np.uint8)
            real_img_ = cv2.imread('./static/images/' + real_img.filename)
            width = real_img_.shape[1]
            height = real_img_.shape[0]
            dsize = (width, height)
            output = cv2.resize(img, dsize)
            masked = real_img_ + (output.reshape(real_img_.shape[0], real_img_.shape[1], 1) * 1 )
            masked_path = 'static/masked/' + 'masked' + real_img.filename
            cv2.imwrite(masked_path, masked)

            count = int(count)
            count_gt = int(count_gt)

            return render_template('index.html', prediction=count, realimg=realimg_path, densityimg=dens_path,
                                   showDensity_gt=density_path_gt, count_gt=count_gt, maskedimg=masked_path)

        else:
            return 'you choosed wrong images'

    return render_template('index.html')

# @app.route('/showDensity', methods=['POST'])
# def showDensity():
#     density_path = "static/density/densityIMG_1.jpg"
#     return render_template('index.html', showDensity=density_path)


# Press the green button in the gutter to run the script.
if __name__ == '__app__':
    app.run(port=3000, debug=True)

# # app
# if __name__ == '__main__':
#     print('hiPyCharm')
