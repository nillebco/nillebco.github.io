---
tags:
  - bash
  - script
date: 2024-09-15
published: true
---

# Use podman as if it was docker (docker alias for podman)

I am a big fan of podman, since it supports rootless containers.

But yet, it's not 100% compatible with docker. It's a pain to set up devcontainers, for example.

So you could be interested in a little "wrapper", that you should place in your PATH env variable.

```bash
#!/bin/bash
updated_params=()

# Iterate over all the parameters
for param in "$@"; do
  # Check if the parameter is "run"
  if [ "$param" == "run" ]; then
    # Add "run" and "--userns" to the updated parameters
    updated_params+=("$param" "--userns=keep-id:uid=1000,gid=1000")
  else
    # Add the parameter as is to the updated parameters
    updated_params+=("$param")
  fi
done

# echo "podman ${updated_params[@]}"

# Execute the docker command with the updated parameters
podman "${updated_params[@]}"
```
