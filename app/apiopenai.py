import openai

openai.api_key = "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"

# engines = openai.Engine.list()

# print(engines)

completion = openai.Completion.create(engine="text-davinci-003", prompt="schreibe einen gruss an marlon von david", max_tokens=100)

print(completion.choices[0].text)