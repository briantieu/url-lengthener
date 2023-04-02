from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for
from db import insert_db, read_db, init_db
from textwrap import wrap

from hashlib import sha3_512

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"serviceAccountToken.json" # /etc/secrets/serviceAccountToken.json

app = Flask(__name__)

def hash(message):
    return sha3_512(str(message).encode('utf-8')).hexdigest()

@app.route('/', methods =["GET", "POST"])
def urlengthen():
    if request.method == "POST":
        # parse form
        original_url = request.form['url']
        num_iters = int(request.form['slider'])

        # hash url
        hashed_url = hash(original_url)

        # store in database
        insert_db(original_url, hashed_url)

        # serve to js
        html = render_template('urlengthen.html', original_url=original_url, hashed_url=str(request.host_url) + (str(hashed_url) * num_iters), num_iters=num_iters)
        response = make_response(html)
        return response
    html = render_template('urlengthen.html', original_url="", hashed_url="", num_iters=1)
    response = make_response(html)
    return response

@app.route('/<hash>')
def url_redirect(hash):

    # condense url to just sha512 hash (key)
    split_hash = wrap(hash, 128)
    unique_split_hash = list(set(split_hash))
    single_iter_hash = unique_split_hash[0]

    # if hash is invalid, return error page
    if len(unique_split_hash) > 1 or read_db(single_iter_hash) == '':
        html = render_template('error.html')
        response = make_response(html)
        return response

    original_url = read_db(single_iter_hash)
    return redirect(original_url)

if __name__ == '__main__':
    init_db()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)