# 🎯 Portfolio

## Speak with a web page

Tags: #web-extension #chrome #safari #desktop #iOS

Too long to read? Let the web page speak to you. Ask for a summary, ask questions, execute simple functions. Available on all pages, includes a Reader Mode (to display what the realtime assistant reads)

Works well with [OpenAI Ephemeral Key Server](#openai-ephemeral-key-server)

[promotional video](https://youtube.com/shorts/YD_as_008lI)
[source code](https://github.com/nillebco/web-extension-voice-rt)
[changelog](https://github.com/nillebco/web-extension-voice-rt/blob/main/CHANGELOG.md)

## OpenAI ephemeral key server

Tags: #service #openai

Simple nodeJS based service that returns openAI real-time video ephemeral keys (validity: 1 minute)

## personal assistant for signal, telegram, whatsapp

For a long while I have been hosting a proxy to OpenAI via Signal, WhatsApp and Telegram. I was thinking that AI access should be shared with friends, because it's incredibly useful in social interactions (make a summary of the ongoing conversations, access tools, perform simple tasks, access different models according to the need, ...)

### more about this

[An AI-based Instant Messaging Assistant](https://nilleb.com/blog/#an-ai-based-instant-messaging-assistant)

## Azure, GCP, Hetzner resources management with terraform

Infrastructure as Code allows reproducibility, traceability and observability to organizations. Each organization is unique, with its own policies. We use terraform to manage organizational resources in Cloud Native environments, and sentinel policies to enforce organizational requirements.

Keywords: private endpoints, private dns zones, network security groups, load balancers, frontdoor profiles, functions and container apps, database servers (cosmosdb, postgres, sql server, mongodb), azuread applications and domain administrator grants. Hetzner firewalls, subnets and hosts. Google Cloud Storage, clour run instances, functions.

## Token Exchange services

In today’s web, we have several identities. Almost one for every site.

Our Token Exchange Services allow a seamless integration between different web applications (typically, a Digital Workplace integration).

- LumApps
  - Bunchball (gamification)
  - Coveo (Search & Semantic Search)
  - Looker

## A chatbot answering any LumApps related question

[LumApps](https://www.lumapps.com/) (a Digital Workplace) offers a public [documentation web site](https://docs.lumapps.com/docs/). It’s a gold mine, and we use it a lot, at [Ariella Digital Consulting](https://www.arielladigitalconsulting.com/).

So we have

- dumped all of its content (you can use the lumapps toolbox OR use one of our crawlers)
- converted them to markdown
- split them to chunks (choosing the right size is paramount)
- cleaned them up (you know, that “Request a change on this documentation.” and a few others)
- converted the chunks to embeddings (multiqampnet, to be honest - it’s cheaper than OpenAI and does a great great great job)
- stored all the chunks in a vector database - we love Rust, hence qdrant was a match made in Paradise.

This is all for the information storage part

Whenever a user asks a question to our bot, we

- convert the question to embeddings,
- compute the closest items in qdrant,
- pick the 100 highest results.
- prepare a prompt (that’s developer lingo for “format the question in a way that will force OpenAI to answer without faking the answer and highlight the sources”)
  - (the prompt includes as a context some of the previously selected results)
- send all this to our favourite Generative AI

 We render on screen the OpenAI response.

---

This is a sample of what we get, when querying our little LumDocsBot:

### Which widgets are supported on mobile?

Supported widgets on mobile include Comments, Content list, Drive, Featured image, File list, File management, HTML content, iFrame, Image gallery, Introduction, Links, Mandatory read, Metadata, Play, Title, Users list, and Video. [Source](https://docs.lumapps.com/docs/mobile-l3073093865382487)

### What do I need to build a digital assistant?

To create a new digital assistant, you need to go to the Digital Assistant web app and log in, click NEW assistant to open the Customize you assistant wizard, select a standard (en or fr), create the assistant, give it a personality, add email addresses for users you want to add as Technical staff and Assistant managers, and configure the assistant knowledge by building resources and enhancing the comprehension. Source: https://docs.lumapps.com/docs/knowledge-l9660062419741646DA

### My Google integrations don't work. Can you help me?

Verify which rights are granted for the LumApps application on Google admin side. Go to https://admin.google.com/ac/apps/gmail/marketplace/domaininstall. Make sure that the LumApps application is activated for all of the OUs containing the users that should access the GSuite integrations. If it is not activated, follow the Google documentation (https://support.google.com/a/answer/172931?hl=en) to activate it. In the LumApps app, access Data Access and make sure that all the Google services you need are Granted. If Status reads Partially granted or Revoked, it means some services are not accessible by LumApps. Make sure to grant their access. If the integrations still do not show in LumApps, uninstall the LumApps app in GSuite and try installing it again. Make sure you are not skipping any step from the LumApps installation documentation (https://docs.lumapps.

### Which are the custom dimensions in Google Analytics 4?

Customer ID, Customer Name, Site ID, Site Name, Site Slug, Content Internal Type, Content Type ID, Content Type Name, Content Is Homepage, Content ID, Content Title, Content Slug, Content Tag IDs, Content Tags, Content Metadata IDs, Content Metadata, Search Terms, User Is Admin, User Primary Language, and User Secondary Language. Source: https://docs.lumapps.com/docs/knowledge-l24187961517950485

## The Expertise Locator

This company wishes to improve the collaboration across their departments and reduce the onboarding attrition.

This organization is distributed across an entire continent - with eventually poor connectivity.

The organization’s public web sites store thousands of PDFs (projects TARs & RRPs, briefs and papers, …) , blog posts, author biographies, … and more.

We have converted non-structured  and semi-structured data into structured data. We have extracted publication dates, author names, countries, and texts. We have then mapped the recognized author names to a primary source of truth.

Challenges:

- map the orthographic variants of a name to the content of a normalized database
- determine the best size of a paragraph, before converting it to an embedding
- keep a good quality across a corpus of thousands of documents, distributed over the last 30 years
- keep the performances of the vector database high enough to satisfy the queries of thousands of users
- keep the bundle as small as possible in order to guarantee a good network connectivity from all around the globe

### more about this

- [Searching for people is not the same as searching for articles and concepts](https://nilleb.com/blog/#searching-for-people-is-not-the-same-as-searching-for-articles-and-concepts)
