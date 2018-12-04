import sys
import request
import re

def translate(text):
    from google.cloud import translate
    target = "ja"
    src = "en"
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target, source_language=src, format_="text")
    return translation['translatedText']

if __name__ == '__main__':
    text = ""
    is_code = False
    for line in sys.stdin:
        if re.match(r'^```', line):
            print(line, end="")
            is_code = not(is_code)
        elif is_code:
            print(line, end="")
        else:
            r = translate(line)

            r = re.sub(r'＃', '#', r)
            r = re.sub(r'＊', '*', r)
            r = re.sub(r'＋', '+', r)
            r = re.sub(r'−', '-', r)
            r = re.sub(r'＞', '>', r)
            r = re.sub(r'^(#+)([^ #])', r'\1 \2', r)
            r = re.sub(r'^(\*+)([^ \*])', r'\1 \2', r)
            r = re.sub(r'^(-+)([^ -])', r'\1 \2', r)
            r = re.sub(r'^(>+)([^ >])', r'\1 \2', r)
            r = re.sub(r'^([0-9]+\.)([^ ])', r'\1 \2', r)
            r = re.sub(r"`[ ]+([^`]+)[`']", r'`\1`', r)

            print(r, end="")

