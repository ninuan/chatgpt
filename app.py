from flask import Flask, render_template, request
import os
from markupsafe import Markup
import openai
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

# 从github的secret里面获得提前设置好的密钥，使用flask进行框架的搭建
openai.api_key = os.environ['api']
app = Flask(__name__)
messages = []
@app.route('/')
def home():

    return render_template('index.html')

# 这一部分是对前端的输入进行获取以及对chatgpt的答复向前端进行发送
@app.route('/get_response', methods=['POST'])

def get_bot_response():
    user_input = request.form['user_input']
    # print(user_input)
    messages.append({'role': 'user', 'content': user_input})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ai_response = completion.choices[0].message['content']
    # print(ai_response)
    messages.append({'role': 'assistant', 'content': ai_response})
    print(messages)
    return  Markup(markdown.markdown(ai_response, extensions=['fenced_code', 'codehilite']))
@app.route('/reset')
def reset():
    global messages
    messages = []
    return "Conversation history has been reset."
if __name__ == '__main__':
    app.run(debug=True)
