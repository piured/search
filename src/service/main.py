# flask app for inference

from flask import Flask, request, jsonify
from transformers import DistilBertForTokenClassification, AutoTokenizer
from transformers import pipeline
import sys
# get first argument as checkpoint path
checkPoint = sys.argv[1]

model_cpu = DistilBertForTokenClassification.from_pretrained(
    checkPoint
)
tokenizer = AutoTokenizer.from_pretrained(checkPoint)
token_classifier = pipeline(
    "token-classification", model=model_cpu, tokenizer=tokenizer, aggregation_strategy="simple"
)

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    pred = token_classifier(data['text'])
    # get query from json requestjsonify(token_classifier(data['text']))
    ret = [{"class": p['entity_group'], "word": p['word'],
            "start": str(p['start']), "end": str(p['end'])} for p in pred]
    return jsonify(ret)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
