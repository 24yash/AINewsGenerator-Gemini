from flask import Flask, render_template, redirect, request, flash, session, url_for
from sqlalchemy.sql.expression import desc

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

model = genai.GenerativeModel('gemini-pro')

from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datablog.sqlite3"
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
app.app_context().push()
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if "api_key" in session:
      print(session['api_key'])
    if request.method == "POST":
            response = request.form
            if response['prompt']:
                prompt = response['prompt']
                new_prompt = f"""Turn the following into an article in the style of The Hindu: {prompt}

                  Your response should be structured exactly like this:
                  Headline:
                  Subheading:
                  Summary:
                  Article:
                  Prompt for thumbnail image:
                  """
                response = model.generate_content(new_prompt)
                try:
                    response.text
                
                
                    print(response.text)

                    response = response.text

                    indices = {"Headline:": None, "Subheading:": None, "Summary:": None, "Article:": None}

                    for key in indices.keys():
                        try:
                            indices[key] = response.index(key) + len(key)
                        except ValueError:
                            print(f"'{key}' not found in response")

                    start_headline = response.index("Headline:") + len("Headline:")
                    end_headline = response.index("Subheading:")
                    start_subheading = response.index("Subheading:") + len("Subheading:")
                    end_subheading = response.index("Summary:")
                    start_summary = response.index("Summary:") + len("Summary:")
                    end_summary = response.index("Article:")
                    start_article = response.index("Article:") + len("Article:")
                    end_article = response.lower().index("prompt for thumbnail image:")

                    headline = response[start_headline:end_headline].strip()
                    subheading = response[start_subheading:end_subheading].strip()
                    summary = response[start_summary:end_summary].strip()
                    article = response[start_article:end_article].strip()

                    headline = str(headline)
                    subheading = str(subheading)
                    summary = str(summary)
                    article = str(article)
                    
                    new_article = Article(prompt=prompt, headline=headline, subheading=subheading, summary=summary, article=article)
                    try:
                        db.session.add(new_article)
                        db.session.commit()
                        return redirect("/")
                    except:
                        return "There was a problem processing. Please go Back!"
                except Exception as e:
                    print("Response object:")
                    print(response)
                    # print(response.prompt_feedback)
                    # print(response.candidates)
                    print(f'{type(e).__name__}: {e}')
                    errstr = f'{type(e).__name__}: {e} API Error. Please go Back!'
                    return errstr
    else:
        return render_template('all.html', articles=Article.query.order_by(desc('id')).all())

@app.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    article = Article.query.get(id)
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template('article.html', article=article)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
