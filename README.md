# Elsie - voice assistant
**NOTE**, development in progress, not yet fully functional.

## About
Realtime AI voice assistant, or just your friendly chat bot.
It's fully open source and offline and runs local on your computer.

End goal is to integrate this in a physical robot, like the *Elsie*
assistant from the movie *M3GAN*.

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
source .venv/bin/activate
python3 app/assistant.py [--help]
```

## Optional models

### Speech-to-text
Download an alternative [model](https://alphacephei.com/vosk/models) and then use flag `--vosk-model` to specify its path.

```shell
mkdir -p models
curl https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip -o temp/vosk-model-en-us-0.22.zip
unzip temp/vosk-model-en-us-0.22.zip -d models/
```

## Related projects
* https://github.com/PromtEngineer/Verbi/ (another voice assistant)
* https://alphacephei.com/vosk (speech-to-text)
