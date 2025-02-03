# knack: generate a mapping from the UI

Tags: knack, api
Publish Date: January 23, 2025

my opinion: knack is not playing faily with third-party developers who would like to obtain their Relations schema.


- there is no API to extract the field names and their IDs.
- the UI is hiding the fields data when they are out of sight

So here a simple method to obtain the mappings from the UI, using your Developer tools

**prerequisite**: reduce the zoom to the minimum possible, so that all the fields are displayed on the UI, even if you can't read them with a microscope


```javascript
function getLabel(keyElement) {
    return keyElement.parentElement.getElementsByClassName('truncate')[0].innerHTML
}

const keys = document.getElementsByClassName('field-key-display')
const mapping = {}

// Build the mapping
Array.from(keys).forEach(keyElement => {
    const label = getLabel(keyElement)
    const key = keyElement.innerHTML
    mapping[label] = key
})

console.log('Label to Key Mapping:', JSON.stringify(mapping, null, 2))

```


This will print to the Console the complete mapping of your table
