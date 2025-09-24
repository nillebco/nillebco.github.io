---
tags:
  - stt
  - whisper
  - virtual-audio-devices
date: 2025-09-24
published: true
---


## Create your own transcription software - on MacOS
⚠️ Legally speaking - you must have collected consent before recording other people's voices.

## BlackHole - configure virtual sound devices
(If you pick the -2ch the recording command line will be easier, in hindsight)

```
brew install blackhole-16ch
```

Use the `Audio MIDI Setup` app to configure your input/output audio sources.

[Define a multi-output device](https://github.com/ExistentialAudio/BlackHole?tab=readme-ov-file) (optional - that showed the path to use Audio MIDI Setup)

Define a new `Aggregate Device`
![[Pasted image 20250924075542.png]]
**IMPORTANT**: pick the microphone as the clock source; avoid selecting blackhole as the primary source

## Recording and mixing
Record the sound from the aggregate device - c1 and 2 are the first two channels on the blackhole audio device, c16 is the microphone (17th channel)
```sh
ffmpeg -f avfoundation -thread_queue_size 2048 \
	-i ":aggregate-device-headset" \
	-filter:a "pan=3c|c0=c0|c1=c1|c2=c16,aresample=async=1:min_hard_comp=0.100:first_pts=0" \
	-ar 16000 -c:a pcm_s16le recording.wav
```

Now that we have a recording over three channels... what next?
1. split the three channels into three mono
```sh
ffmpeg -i input.wav \
-map_channel 0.0.0 ch1.wav \
-map_channel 0.0.1 ch2.wav \
-map_channel 0.0.2 ch3.wav
```
2. merge them into a mono file
```sh
ffmpeg -i input.wav \
-filter:a "pan=mono|c0=0.33*c0+0.33*c1+0.33*c2" \
-c:a pcm_s16le merged.wav
```
3. (for the sake of testing) play it with ffplay
```sh
ffplay -nodisp -autoexit -af "pan=stereo|FL=0.33*c0+0.33*c1+0.33*c2|FR=0.33*c0+0.33*c1+0.33*c2" input.wav
```

## Transcribe
Last, transcribe!
(whisper-ane is an optimized version of whisper.cpp, built for the Apple Neural Engine - [find it on GitHub](https://github.com/nillebco/fast-openai-like-transcription-server))

🇺🇸 English
```sh
WHISPER_CPP_DIR=/Users/nilleb/dev/nillebco/whisper-ane/whisper.cpp
$WHISPER_CPP_DIR/build/bin/whisper-cli -m $WHISPER_CPP_DIR/models/ggml-medium.en.bin -f merged.wav -ojf -of outputs/out-1806e5f1-3b03-4413-83c2-0ed2155dc7fd -l en
```

🇫🇷 French
```sh
WHISPER_CPP_DIR=/Users/nilleb/dev/nillebco/whisper-ane/whisper.cpp
$WHISPER_CPP_DIR/build/bin/whisper-cli -m $WHISPER_CPP_DIR/models/ggml-medium.bin -f merged.wav -ojf -of outputs/out-1806e5f1-3b03-4413-83c2-0ed2155dc7fd -l fr
```
