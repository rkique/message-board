from flask import Flask, render_template, request, url_for, redirect
from waitress import serve
import json
import datetime
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():

    with open("posts.json", "r") as infile:
        posts = json.load(infile)

    time = datetime.datetime.now()
    raw_time = time.timestamp()
    display_time = str(time.replace(microsecond=0))

    if request.method == 'POST':

        img_path = ""
        if request.files.get('uploaded-file', None):
            img = request.files['uploaded-file']
            img_path = 'static/' + img.filename
            img.save(img_path)

            with Image.open(img_path) as img:
                img.thumbnail((256,256))
                img.save(img_path)

        posts.append({'raw_time': raw_time, 
                      'display_time': display_time, 
                      'title': request.form['title'], 
                      'content': request.form['content'], 'img_path': img_path})
        posts.sort(reverse=True, key= lambda x: x['raw_time'])
        json_obj = json.dumps(posts)
        with open("posts.json", "w") as outfile:
            outfile.write(json_obj)

    return render_template('index.html', posts=posts)

@app.route('/delete/<id>', methods=('GET',))
def delete(id):
    with open("posts.json", "r") as infile:
        posts = json.load(infile)
        posts = [post for post in posts if post['raw_time'] != float(id)]
    
    with open("posts.json", "w") as outfile:
        json_obj = json.dumps(posts)
        outfile.write(json_obj)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

