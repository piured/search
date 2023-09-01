# flask app for inference

from flask import Flask, request, jsonify
from transformers import DistilBertForTokenClassification, AutoTokenizer
from transformers import pipeline
import sys
import re
# get first argument as checkpoint path
checkPoint = sys.argv[1]

model_cpu = DistilBertForTokenClassification.from_pretrained(
    checkPoint
)
tokenizer = AutoTokenizer.from_pretrained(checkPoint)
token_classifier = pipeline(
    "token-classification", model=model_cpu, tokenizer=tokenizer, aggregation_strategy="simple"
)

pattern = re.compile(r'(\b[rdsc]|hd)(\d+)([+-]?)(?=\s|$)')


def get_char_position(input):
    matches = pattern.finditer(input)
    positions = []
    for match in matches:
        positions.append(match.span()[0] +
                         (2 if match.group(1) == 'hd' else 1))
    return positions


def replace_char_position(input):
    return pattern.sub(r'\1 \2\3', input)


def remap_positions(pred, positions):
    for item in pred:
        for position in positions:
            if item['start'] > position:
                item['start'] -= 1
                item['end'] -= 1


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    positions = get_char_position(data['text'])
    input = replace_char_position(data['text'])
    pred = token_classifier(input)
    remap_positions(pred, positions)
    # get query from json requestjsonify(token_classifier(data['text']))
    ret = [{"class": p['entity_group'], "word": p['word'],
            "start": str(p['start']), "end": str(p['end'])} for p in pred]
    return jsonify(ret)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
