from googletrans import Translator

translator = Translator()

text = '我爱你'
res = translator.translate(text)
print(text, res)