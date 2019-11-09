import os
import base64
import html

from flask import Flask, request
from model import Message 

html_escape_table = {
                    "&": "&amp;",
                    '"': "&quot;",
                    "'": "&apos;",
                    ">": "&gt;",
                    "<": "&lt;",
                    }

def html_escape(text):
  """Produce entities within text."""
  return "".join(html_escape_table.get(c,c) for c in text)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        m = Message(content=request.form['content'])
        m.save()

    body = """
<html>
<body>
<h1>Class Message Board</h1>
<h2>Contribute to the Knowledge of Others</h2>
<form method="POST">
    <textarea name="content"></textarea>
    <input type="submit" value="Submit">
</form>

<h2>Wisdom From Your Fellow Classmates</h2>
"""
    
    for m in Message.select():
        body += """
<div class="message">
{}
</div>
""".format(html_escape(m.content))
    return body 

# <script>
# alert('Hello Everybody!');
# </script>
# '<' and '>' are html control characters specifying tags, used in the message above to insert a javascript
# after above modification messages loaded from database:
# '&lt' and '&gt' are shown as '<' and '>' in the browsser in in the webpage body remains '&lt' and '&gt' 
# <div class="message">
# &lt;script&gt;
# alert('Hello Everybody!');
# &lt;/script&gt;
# </div>

#  hello
# second message
# <script> alert('Hello Everybody!'); </script> 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

