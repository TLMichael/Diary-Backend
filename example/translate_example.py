# from googletrans import Translator

# translator = Translator()

text = '我爱你'

# res = translator.translate(text)
# print(text, res)


print('调用translate命令')

import os

command = 'proxychains translate ' + text

res = os.popen(command, 'r')
print(text)
print('\n\n')
print(res.read())