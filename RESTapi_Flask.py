import os
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = r'C:\Users\Ahmed-wafa\Desktop\Deploying\upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def flask_app():
    app = Flask(__name__, template_folder='templates')

    @app.route('/server', methods=['GET'])
    def server_is_up():
        return 'server is up'

    @app.route('/start')
    def start():
        return render_template('start.html')

    # @app.route("/getimage", methods=['GET'])
    # def get_img():
    #     return "IMG_1.jpg"
    #
    # # @app.route('/predict_price', methods=['POST'])
    # # def start():
    # #     to_predict = request.json
    # #
    # #     print(to_predict)
    # #     pred = predict(to_predict)
    # #     return jsonify({"predict cost":pred})

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in {"jpg"}

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                print(file.filename)
                filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return filename
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <div id="ImageContainer">
        <form runat="server">
            <input accept="image/*" type='file' id="imgInp" /> <br />
            
                <img id="blah" src="#" alt="your image" />
            
        </form>
        <div>
        
        <style>
                h1 {color: maroon;margin-left: 40px;} 
                div#ImageContainer { width: 600px; }
        </style>
        
        <script>
              imgInp.onchange = evt => {
              const [file] = imgInp.files
              if (file) {
                    blah.src = URL.createObjectURL(file)
                    }
                                            }
                                            
                                            
              
        </script>
        '''

    return app


if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0')
