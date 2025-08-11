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
```

## Run
```shell
# start ollama server
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama             # only CPU
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama --gpus=all ollama/ollama  # with GPUs

# start assistant
source .venv/bin/activate
python3 app/assistant.py               

# variants
python3 app/assistant.py --debug       # view more stuff
python3 app/assistant.py 2> /dev/null  # cleaner output
python3 app/assistant.py --help        # view all options
```

## Optional models

### Speech-to-text model
Download an alternative [model](https://alphacephei.com/vosk/models) and then use flag `--vosk-model` to specify its path.

```shell
mkdir -p models
curl https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip -o temp/vosk-model-en-us-0.22.zip
unzip temp/vosk-model-en-us-0.22.zip -d models/
```

### Response model (Ollama)
Default model is `llama3`, but for this case there are better options, like `mistral` 
Start a chat to pre-load another model: `docker exec -it ollama ollama run mistral`.
Then run the assistant with `--ollama-model mistral`

## Related projects
* https://github.com/PromtEngineer/Verbi/ (another voice assistant)
* https://alphacephei.com/vosk (speech-to-text)
