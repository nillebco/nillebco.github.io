---
tags:
  - OpenAI
  - nodeJS
  - python
date: 2024-09-19
published: true
---

# Generate a JSON Schema for OpenAI Structured Outputs

Maybe you are a nodeJS developer and you need to pass a json_schema to your chat.completion call

Something like this:

```bash
    const completion = await model.chat.completions.create({
        messages: [{
            role: "user",
            content: query
        }],
        model,
        temperature: 0.0,
        response_format: responseFormat,
    });
```

But the, how should that `responseFormat` look like?

I didn't know how to implement this using just nodeJS - so I dug a bit into the openAI parse method, and extracted a little helper, in python

```python
import json
from typing import Optional, Any, List

from pydantic import BaseModel
from openai.lib._parsing._completions import type_to_response_format_param

# begin section Model - replace this section
class PersonName(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]

class Contact(BaseModel):
    name: PersonName
    user_id: Optional[Any] = None
    phone_numbers: List[str]
    emails: List[str]

model = Contact
# end section Model

print(json.dumps(type_to_response_format_param(model)))

```
