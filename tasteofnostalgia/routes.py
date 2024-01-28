from tasteofnostalgia import APP

import cohere



"""Spicy Wontons - eaten Jan 25, 2024: 1/5
Subway sandwich - eaten Jan 20, 2024: 4/5
Big Mac - eaten Jan 15, 2024: 3/5
Pizza Pizza - eaten Jan 10, 2024: 4/5
Ramen Noodles - eaten Jan 5, 2024: 5/5"""

@APP.route("/")
def recommendation():
    co = cohere.Client('BSnGEJ95ZX7mMUasrq7Au6iFXtfz0VkGXrUOxiD2')
    food = ['Spicy Wontons', 'Subway Sandwich', 'Big Mac', 'Pizza Pizza']
    ratings = [1, 4, 3, 4, 5]
    date = ['Jan 25, 2024', 'Jan 20, 2024', 'Jan 15, 2024', 'Jan 10, 2024', 'Jan 5, 2024']
    prompt = "Based on this information, suggest a food similar to one that the user has ranked highly and hasn't eaten recently: "
    for i in range(len(food)):
        prompt+="\n" + food[i] + " - eaten " + date[i] + ": " + ratings[i] + "/5 "
    print("Prompt: " + prompt)
    response = co.generate(prompt=prompt,)
    print("Cohere:" + response)


@APP.route("/")
def hello_world():
    return "<p>Hello, World!</p>"