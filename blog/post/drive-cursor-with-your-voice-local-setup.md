# Drive cursor with your voice - local setup

Tags: AI, Cursor, whisper, speech to text
Publish Date: March 29, 2025

I found an interesting extension for VSCode that allows you to use a local whisper server to transcribe your thoughts into cursor chat commands

Launch a local whisper server

```sh
cd ~/dev
git clone https://github.com/martin-opensky/whisper-assistant-vscode
cd whisper-assistant-vscode
docker build -t whisper-assistant-server .  
docker run --restart unless-stopped -d -p 4444:4444 --name whisper-assistant whisper-assistant-server
```

There is a missing module openai in the extension startup
but now I have a local instance of the whisper transcribe api
solution was to `npm install` in the install folder `~/.cursor/extensions/martinopensky.whisper-assistant-1.1.0`
https://github.com/martin-opensky/whisper-assistant-vscode/issues/12

Last, modify the shortcut "Whisper: Toogle Recording" shortcut to use alt+cmd+\ instead of cmd+m (otherwise it won't record in the cursor chat).

Bonus: the whisper server hosts a openai compatible stt API, so you can re-use this everywhere.
