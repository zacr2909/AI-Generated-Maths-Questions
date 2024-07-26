import openai
import json

#set the api
api_key = 'your_key'

#chatgpt message variable
chatgpt = []
#start the openai api client
openai.api_key = api_key

def generate_questions(maths_topic):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Create a list of 3 multiple-choice math questions on the topic of {maths_topic}. For each question, provide a question text, a list of four options labeled a), b), c), and d), a correct_answer that is one of these letters ('a', 'b', 'c', 'd'), and a hint to help solve the question if needed. Return the questions as a JSON array of objects."},
            {"role": "user", "content": maths_topic}
        ],
    )
    content = response['choices'][0]['message']['content'].strip()

    try:
        questions_list = json.loads(content)
        return questions_list
    except json.JSONDecodeError:
        print("Invalid JSON content:", content)
        return None

def present_questions(questions_list):
    for question_info in questions_list:
        # check if 'question' key exists
        if 'question' not in question_info:
            print("Tutor: Error - The key 'question' does not exist in the question info.")
            print(f"Tutor: The available keys are: {list(question_info.keys())}")  # Print the available keys for debugging.
            continue  # skip this question and move to the next

        # assuming the keys exist, print the question
        print(f"Tutor: {question_info['question']}")

        # check if 'options' key exists
        if 'options' in question_info and isinstance(question_info['options'], dict):
            for key, value in sorted(question_info['options'].items()):
                print(f"Tutor: {key}) {value}")
        else:
            print("Tutor: Error - The key 'options' is missing or is not a dictionary.")
            continue

        # start loop for the user to answer or ask for help
        while True:
            user_input = input("You: ").strip().lower()

            # If the user asks for help
            if user_input == 'help':
                hint = question_info.get('hint', 'There is no hint for this question.')
                print(f"Tutor: {hint}")
                continue

            # check if the users answer is correct
            correct_answer = question_info['correct_answer'].lower()
            if user_input == correct_answer:
                print("Tutor: Correct! Well done.")
                break
            else:
                print("Tutor: That's not correct. Try again, or type 'help' for a hint.")


def main():
    while True:
        print("Tutor: What subject would you like to work on today? (Type 'exit' to end)")
        user_subject = input("You: ").strip().lower()

        if user_subject == 'exit':
            print("Tutor: Goodbye! Have a great day.")
            break

        questions_list = generate_questions(user_subject)
        if questions_list:
            present_questions(questions_list)
        else:
            print("Tutor: I'm sorry, I couldn't generate questions for that subject. Please try again or choose a different topic.")            
main()
