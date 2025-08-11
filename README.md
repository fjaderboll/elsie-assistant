# Elsie - voice assistant
**NOTE**, development in progress, not yet fully functional.

## About
Realtime AI voice assistant, or just your friendly chat bot.
It's fully open source and offline and runs local on your computer.

End goal is to integrate this in a physical robot, like the *Elsie*
assistant from the movie *M3GAN*, hence the name.

## Setup
First time only.

```shell
# required system packages
sudo apt install python3 python3-pip python3-venv portaudio19-dev

# setup virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# begin with default settings
cp settings.default.json settings.json
```

## Run
```shell
# start ollama server
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama             # only CPU
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama --gpus=all ollama/ollama  # with GPUs

# start assistant
source .venv/bin/activate
python3 app/assistant.py [--help]

# workaround for cleaner output until I find a way to fix that
python3 app/assistant.py 2> /dev/null
```

## Optional models
Depending on your needs and computer performance, you may want to tweak this.

### Speech-to-text model
Download an alternative [model](https://alphacephei.com/vosk/models) and then update `voskModelPath` in `settings.json`.
The larger English model seems to be slightly more accurate, though also slower.
It's also possible to switch input language by doing this (assuming the other models support it).

```shell
mkdir -p models
curl https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip -o /tmp/vosk-model-en-us-0.22.zip
unzip /tmp/vosk-model-en-us-0.22.zip -d models/
jq '.voskModelPath = "models/vosk-model-en-us-0.22"' settings.default.json > settings.json
```

### Response model (Ollama)
Default model is `llama3`, but for this case there are better [libraries](https://ollama.com/library),
like [mistral](https://ollama.com/library/mistral).
Start a chat to pre-load another model: `docker exec -it ollama ollama run mistral`.
Then update property `ollamaModel` in `settings.json`.

## Related projects
* https://github.com/PromtEngineer/Verbi/ (another voice assistant)
* https://alphacephei.com/vosk (speech-to-text)
* https://ollama.com
