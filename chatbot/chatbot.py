import openai

openai.api_key = "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"

messages = []
system_msg = input("helo Friend how are you!!\n")
messages.append({"role":"system", "content": system_msg})

print("wanna chat?")
while input != "quit()":
    message = input()
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")