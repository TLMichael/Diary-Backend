from __future__ import print_function, division, unicode_literals
# import example_helper
import json
import csv
import argparse

import numpy as np
import emoji

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)

import time


app = Flask(__name__)

# Emoji map in emoji_overview.png
EMOJIS = ":joy: :unamused: :weary: :sob: :heart_eyes: \
:pensive: :ok_hand: :blush: :heart: :smirk: \
:grin: :notes: :flushed: :100: :sleeping: \
:relieved: :relaxed: :raised_hands: :two_hearts: :expressionless: \
:sweat_smile: :pray: :confused: :kissing_heart: :heartbeat: \
:neutral_face: :information_desk_person: :disappointed: :see_no_evil: :tired_face: \
:v: :sunglasses: :rage: :thumbsup: :cry: \
:sleepy: :yum: :triumph: :hand: :mask: \
:clap: :eyes: :gun: :persevere: :smiling_imp: \
:sweat: :broken_heart: :yellow_heart: :musical_note: :speak_no_evil: \
:wink: :skull: :confounded: :smile: :stuck_out_tongue_winking_eye: \
:angry: :no_good: :muscle: :facepunch: :purple_heart: \
:sparkling_heart: :blue_heart: :grimacing: :sparkles:".split(' ')

# Tokenizing using dictionary
with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)

st = SentenceTokenizer(vocabulary, 50)

# Loading model
model = torchmoji_emojis(PRETRAINED_PATH)

def get_emotion(text):
    def top_elements(array, k):
        ind = np.argpartition(array, -k)[-k:]
        return ind[np.argsort(array[ind])][::-1]
    # Running predictions
    tokenized, _, _ = st.tokenize_sentences([text])
    # Get sentence probability
    prob = model(tokenized)[0]
    # Top emoji id
    emoji_ids = top_elements(prob, 5)

    return emoji_ids


# 用 log 函数把所有输出写入到文件，这样就能很方便地掌控全局了
# 即便你关掉程序，也能再次打开来查看，这就是个时光机
def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    
    with open('log.lue.txt', 'a', encoding='utf-8') as f:
        # 通过 file 参数可以把输出写入到文件 f 中
        # 需要注意的是 **kwargs 必须是最后一个参数
        print(dt, *args, file=f, **kwargs)


@app.route('/', methods=['GET'])
def hello_world():
    return '<h1>Hello Lue</h1>'

@app.route('/emotion', methods=['GET'])
def emotion():

    log('请求方法', request.method)

    # request.args 是 flask 保存 URL 中的参数的属性
    # 访问 http://127.0.0.1:2000/emotion?text=hhh
    # 会打印如下输出 (ImmutableMultiDict 是 flask 的自定义类型, 意思是不可以改变的字典)
    # request ImmutableMultiDict([('text', 'hhh')])
    log('request, query 参数', request.args)
    
    try:
        text = request.args['text']
        emoji_ids = get_emotion(text)

        emojis = map(lambda x: EMOJIS[x], emoji_ids)
        
        res = emoji.emojize("{} {}".format(text,' '.join(emojis)), use_aliases=True)

        log('分析结果：', res)
        print(res)
        return res
    except:
        return 'hhh'




# 运行服务器
if __name__ == '__main__':

    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)