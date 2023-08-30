# Search

A service for searching songs in piured using natural language.

## Corpus generation

The data to generate the corpus is based on the database of mixes, songs and artists of piured, and can be found in `data/raw`.
In order to generate the corpus, use the script in `src/corpus/main.py`. Check the help `-h` for more information.

## Training

Training is done through the notebook `notebooks/train.ipynb`. Currently DistilBERT is used as the model, provided by huggingface. The model is fine tuned for the downstream task of learning entities useful for the search.

## Deployment

The service is deployed using docker-compose.

Prior to running the service, modify `Dockerfile` with the correct path to your fine-tuned model (not provided in this repo).
Then, run `docker-compose up -d` to deploy the service as usual.

## API

The API is a simple REST API, with a single endpoint `/predict` that accepts a POST request with a JSON body. The port to make the request to is `5000`.

```ts
{
  text: string;
}
```

The body should contain a single key `text` with the text to search.

The reply is a JSON with the following structure:

```ts
{
    class: Entity;
    start: number;
    end: number;
    word: string;
}[]
```

where `Entity` is one of the following:

```ts
Entity =
  "tune" |
  "mix" |
  "stepstype" |
  "meter" |
  "bpm_lower_than" |
  "credit" |
  "bpm_greater_than" |
  "meter_greater_than" |
  "artist" |
  "bpm" |
  "warps" |
  "scrolls" |
  "fakes" |
  "speeds" |
  "stops" |
  "meter_lower_than" |
  "pump-single" |
  "pump-double" |
  "pump-halfdouble" |
  "pump-routine" |
  "pump-couple";
```

The `start` and `end` fields indicate the start and end position of the entity in the text, and `word` is the word that was matched.
