import openai

openai.api_key = 'AIzaSyCQ972Q7d_LfbfRos00dKtiUFB7M64FOrA'

completion = openai.ChatCompletion.create(
    model="gpt-4",  # Correct model name is "gpt-4" not "gpt-4o"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ]
)

print(completion.choices[0].message['content'])
