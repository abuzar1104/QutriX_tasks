# Import the 'json' module to work with JSON files.
# Import the 'random' module to shuffle the questions.
import json
import random


def load_questions(filename="questions.json"):
    """
    This function loads the list of questions from a specified JSON file.
    It includes error handling for cases where the file might be missing or corrupted.
    """
    try:
        with open(filename, "r") as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' contains invalid JSON.")
        return []


def run_quiz(questions):
    """
    This function takes a list of questions, runs the quiz, tracks the score,
    and displays the final results to the user with a custom message.
    """
    score = 0

    if not questions:
        print("No questions could be loaded. Cannot start the quiz.")
        return

    random.shuffle(questions)

    # --- Start of the Quiz ---
    print("--- Welcome to the Tech Quiz! ---")
    print("Answer the following questions by typing A, B, C, or D.\n")

    for index, item in enumerate(questions):
        print(f"Q{index + 1}: {item['question']}")

        for option in item["options"]:
            print(option)

        # --- User Input Loop ---
        while True:
            user_answer = input("Your answer: ").strip().upper()
            if user_answer in ["A", "B", "C", "D"]:
                break
            else:
                print("Invalid input. Please enter A, B, C, or D.")

        # --- Answer Checking ---
        correct_answer = item["answer"].upper()

        if user_answer == correct_answer:
            print("Correct! 🎉\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was {correct_answer}. 😔\n")

    # --- Final Score Calculation and Output ---
    print("--- Quiz Finished! ---")
    total_questions = len(questions)

    if total_questions > 0:
        percentage = (score / total_questions) * 100
    else:
        percentage = 0

    print(f"Your final score is: {score} out of {total_questions}")
    print(f"You scored {percentage:.2f}%.")

    # Display a custom message based on the user's score
    if percentage >= 80:
        print("\nExcellent work! You have a strong grasp of these concepts. 🚀")
    elif percentage >= 50:
        print("\nGood job! You passed. Keep practicing! 👍")
    else:
        print("\nGood effort. Review the topics and try again! 📚")


# This code runs only when the script is executed directly.
if __name__ == "__main__":
    quiz_questions = load_questions()
    run_quiz(quiz_questions)
