# Reader: An AI-powered article discussion app powered by Prompt Flow
Prototype chat app built using [Prompt flow](https://github.com/microsoft/promptflow) and powered by OpenAI (and optionally MistralAI).

## Requirements
To run this repo you need an [OpenAI API](https://platform.openai.com) subscription and optionally a [MistralAI](https://console.mistral.ai/) subscription.


## Setup Instructions (required)
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys) and generate a new key for this project.
2. Click the Prompt Flow icon in the sidebar (looks like an origami figure of the letter "P").
3. Under "Connections" click the "+" symbol next to "OpenAI." This opens a file in the editor.
4. In the `name` field replace the placeholder text with `flow_reader_openai`.
5. Click the "Create Connection" link in the editor. This opens a command line process.
6. Paste your OpenAI API key when prompted.

## Running the app
The Codespace and app are built to run without further configuration.
1. Open `./reader-final/flow.dag.yaml`
2. Click `Visual Editor` to open the visual editor.
3. In Visual Editor, click the two overlapping play buttons in the top bar.
4. Select how you want to run the flow:
   - "Run with standard mode" runs the flow one time with the preconfigured chat input and provides detailed logs.
   - "Run with interactive mode (text only)" runs the flow as a chat app in terminal.
   - "Run with interactive mode (multi-modal)" runs the flow as a GUI chat app in your browser.
   - NOTE: If you choose multi-modal, follow the provided localhost link to open the GUI chat app.
5. To stop either interactive mode, press Ctrl + C in Terminal.

## Using MistralAI as question classifier (optional)
Out of the box the Reader app uses OpenAI for all AI processing. This is heavy-handed for the question classifier step, so you can use the ligher and cheaper Mistral Nemo app for this node instead.

At the moment, Prompt Flow does not support MistralAI as a connection, but it can be added manually as a tool and a Custom Connection. 

The tool is already provided in the file `./reader-final/mistral_connection.py`. This is also where you'll find the system message for this node.

To activate MistralAI as a connection:
1. Go to [console.mistral.ai](https://console.mistral.ai/) and generate a new MistralAI API key for this project.
2. Open the Prompt Flow panel in the sidebar.
3. Go to "Connections" and click the "+" symbol next to "Custom"
4. In the `name` field replace the placeholder text with `mistral_connection`.
5. Delete the `configs:` and `key1: "Test 1`" lines.
6. Under `secrets:` change `key2` to `api_key`.
7. Click the "Create Connection" link in the editor. This opens a command line process.
8. Paste your MistralAI API key when prompted.

Next, replace the existing Question Classifier node:

Open `flow.dag.yaml` in the text editor, find the `nodes:` section, and identify the `question_classifier` node. It look like this:

```yaml
nodes:
  name: question_classifier
  type: llm
  source:
    type: code
    path: question_classifier.jinja2
  inputs:
    model: gpt-3.5-turbo
    temperature: 0
    max_tokens: 100
    query: ${inputs.question}
  connection: flow_reader_openai
  api: chat
```

Replace the above node code with this:

```yaml
nodes:
  name: question_classifier
  type: python
  source:
    type: code
    path: mistral_connection.py
  inputs:
    connection: mistral_connection
    temperature: 0
    max_tokens: 100
    query: ${inputs.question}
    model_name: open-mistral-nemo
    top_p: 1
```

In the Visual Editor scroll to the `question_classifier` node and you should see an updated node with filled mandatory fields for `temperature`, `max_tokens`, `query`, `model_name`, and `top_p`.

Run the app as described above to test. 

## Quirks
- When you provide a link in the chat, the app caches and the rewritten article in `./reader-final/temp_cached_article.py`. When you provide a new link, the previous file is overwritten. This file is not deleted between sessions, so when you boot up the app after querying an article, it will refer back to the already cached article. You can safely delete `temp_cached_article.py` at any time.

## License
Published under the [MIT](LICENSE) license.
