from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from forms import Form
import math
import os
import numpy as np
from PIL import Image
import colorgram
import glob

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = os.environ.get("key")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = "./static"



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/", methods=["GET","POST"])
def upload_file():
    form = Form()
    if request.method=="POST":
        # color_list = []
        # color_dict = {}
        # color_rank_list = []
        file = form.FileName.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #filepath = os.path.join(app.config['UPLOAD_FOLDER']+"/"+filename)
            filepath_tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
            if not os.path.exists(filepath_tmp):
                os.mkdir(filepath_tmp)
            filepath = os.path.join(filepath_tmp, filename)
            file.save(filepath)

            # img = Image.open(filepath)
            # pix = np.array(img.getdata()).reshape(img.size[0], img.size[1], 3)
            # for i in range(img.size[0]):
            #     for j in range(img.size[1]):
            #         color_list.append([pix[i][j][0], pix[i][j][1], pix[i][j][2]])
            # for i in color_list:
            #     if tuple(i) not in color_dict:
            #         color_dict[tuple(i)] = 1
            #     else:
            #         color_dict[tuple(i)] += 1
            #
            # color_dict_sort_keys = sorted(color_dict, key=color_dict.get, reverse=True)
            # for i in range(20):
            #     color_rank_list.append([color_dict_sort_keys[i], color_dict[color_dict_sort_keys[i]]/(img.size[0]*img.size[1])])
            img = filepath
            main_color = form.MainColor.data
            try:
                int(main_color)
            except:
                flash("Please enter an integer")
                return redirect(url_for("upload_file"))

            colors = colorgram.extract(img, main_color)
            color_rank_list = [[(color.rgb[0], color.rgb[1], color.rgb[2]), float("{:.2f}".format(color.proportion*100))] for color in colors]
            return render_template("index.html", Is_IMG=True, file=os.path.join(filepath) ,form=form, ranking=color_rank_list)

        else:
            flash("Please upload an image file")
            return redirect(url_for("upload_file"))

    return render_template("index.html", Is_IMG=False, form=form)


if __name__ == "__main__":
    app.run(debug=True)