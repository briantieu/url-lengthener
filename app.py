from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for
from db import insert_db, read_db, init_db

from hashlib import sha3_512

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"serviceAccountToken.json" # /etc/secrets/serviceAccountToken.json

app = Flask(__name__)


def hash(message):
    return sha3_512(str(message).encode('utf-8')).hexdigest()


# def list_languages():
#     return translate_client.get_languages()

# @app.route('/translate_and_store', methods=['POST'])
# def translate_and_store():
#     text = request.json['content']
#     translation = translate_text(get_language(), text)['translatedText']
#     insert_db(translation)
#     return {}

# @app.route('/get_text', methods=['GET'])
# def get_text():
#     texts = read_db()
#     text = texts[0]['content'] if len(texts) > 0 else ''
#     message = {'displayText': text}
#     return jsonify(message)

# def get_language():
#     lang = get_lang_db()
#     language = lang[0]['language'] if len(lang) > 0 else 'en'
#     return language

# @app.route('/change_language', methods=['POST'])
# def change_language():
#     language = request.json['language']
#     change_lang_db(language)
#     return {}

@app.route('/', methods =["GET", "POST"])
@app.route('/urlengthen', methods =["GET", "POST"])
def urlengthen():
    if request.method == "POST":
        # parse form
        original_url = request.form['url']

        # hash url
        hashed_url = hash(original_url)

        # store in database
        insert_db(original_url, hashed_url)
        print("inserted")

        # serve to js
        html = render_template('urlengthen.html', original_url=original_url, hashed_url=str(request.host_url) + str(hashed_url))
        response = make_response(html)
        return response
    html = render_template('urlengthen.html', original_url="NONE", hashed_url="NONE")
    response = make_response(html)
    return response

@app.route('/<hash>')
def url_redirect(hash):
    original_url = read_db(hash)
    print(original_url)
    return redirect(original_url)




if __name__ == '__main__':
    init_db()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)