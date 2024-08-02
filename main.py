import json
from difflib import get_close_matches

#load the knowledge base into the program
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file: #opening the file_path in read mode as file
        data: dict = json.load(file) #read the JSON content from the file and loads it into a Python dictionary and assigning it to the variable 'data'
    return data

#save the dictionary into knowledge base to have the old responses stored in the memory any time we restart the program
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file: #opening the file_path in write mode as file
        json.dump(data, file, indent = 2) #insert data into json (write the dictionary data to the file with an indentation of 2 spaces, making the JSON output more readable)
        #note: The function does not return anything; it just writes the data to the specified file.

#find the best match from the dictionary
def find_best_match(user_question: str, questions: list[str]) -> str | None: #because maybe what it might be looking for in the knowledge_base might not exist
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #the maximum number of matches to return (n) of 1 so it can give us the best answer possible and similarity threshold (cutoff) of accuracy 60%
    return matches[0] if matches else None #because it can be empty

#getting answers for questions
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

#main script
def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')
            
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learnt a new respond \U0001F60A')


if __name__ == '__main__':
    chatbot()
