# Elsie - voice assistant

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
cp settings.default.ini settings.ini
```

## Run
The first time you run it, make sure to have a Internet connection.

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
Depending on your needs and computer performance, you may want tweak `settings.ini`.
See comments in that file for more details.

## Related projects
* https://github.com/PromtEngineer/Verbi/ (another voice assistant)
* https://alphacephei.com/vosk (speech-to-text)
* https://ollama.com (the ai)
* https://github.com/OHF-Voice/piper1-gpl (text-to-speech)
