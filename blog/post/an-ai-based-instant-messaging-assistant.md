---
tags:
  - OpenAI
  - python
date: 2024-05-07
published: true
---

# An AI-based Instant Messaging Assistant

What I'm introducing today is the nilleb's family assistant. I use this bot to serve the requests of my family and close friends.

The aim was to

- provide a simpler way for the common mortal to access Artificial Intelligences
- experiment with artificial intelligence models - how do they differ? what do they support natively? can we provide some kind of eurystic about how to make the choice?
- experiment with instant messaging APIs (Signal, WhatsApp)
- lay off the foundations of a modern python service

Today this bot

- supports several Artificial Intelligence models:
    - a fair amount of gpt models
    - all the claude3 models
    - all the mistral models
    - dalle3
- supports voice messages and processing attachments (such as image files, to support "vision" requests
- supports tools calling
    - with a different perimeter for every user (ie. all users will have access to a common set of functions, users who have supplied a "tool configuration" will have access to the functions associated to that "tool")
- supports two instant messaging "transports"
    - whatsapp
    - signal
- supports out-of-band messaging with the bot itself
    - to enable and disable the dictation/echo mode (for audio messages)
    - to change the current model
    - to reset the current session (ie. wipe out the "context")
    - to get more details about the model used and the usage statistics
    - to provide configuration for the "tool calling"
- supports invites
    - the owner of the bot can invite other users
    - users can invite other users
    

What I would like to experiment next

- add a Slack transport
- add a "knowledge base driven RAG"

The main takeaways of this experience

- signal is completely free and supports a wide amount of use cases
- in order to use whatsapp you have to pay (for the meta business api or for some wrapper such as ultramsg or whapi) and these APIs support a limited perimeter - better to inspect them one by one to check if your use case is supported before paying
- every distinct model has its own peculiarities (thanks God openrouter exists and is maintained - it has a standard interface that brings you peace of mind - instead of creating a wrapper for every family like I did).
- Artificial Intelligence is so distant from everyday reality of the common mortal. At best, catholic associations are organising meetups to spread the word (against it).

If you want to know more about it, just drop me a message at [ivo@nilleb.com](mailto:ivo@nilleb.com) ;)
