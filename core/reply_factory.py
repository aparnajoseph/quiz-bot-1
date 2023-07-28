
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id):
    '''
    Validates and stores the answer for the current question to session.
    '''
     if current_question_id is None:
        return False, "No active question to answer."

    # Fetch the current question details from the PYTHON_QUESTION_LIST
    current_question = next(
        (question for question in PYTHON_QUESTION_LIST if question["id"] == current_question_id),
        None
    )

    if not current_question:
        return False, "Invalid question ID."

    # Assuming the answer is valid and not empty, you can add more specific validation as needed
    if not answer or not isinstance(answer, str):
        return False, "Invalid answer format."

    # Store the answer in the session for later use if needed
    session["answers"].append({"question_id": current_question_id, "answer": answer})
    
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
      if current_question_id is None:
        next_question = PYTHON_QUESTION_LIST[0]["question"]
        next_question_id = PYTHON_QUESTION_LIST[0]["id"]
        return next_question, next_question_id

    # Find the index of the current_question_id in the list
    current_question_index = next(
        (index for index, question in enumerate(PYTHON_QUESTION_LIST) if question["id"] == current_question_id),
        None
    )

    # If the current_question_id is not found or the last question is already reached, return None
    if current_question_index is None or current_question_index == len(PYTHON_QUESTION_LIST) - 1:
        return None, -1

    # Get the next question from the list
    next_question = PYTHON_QUESTION_LIST[current_question_index + 1]["question"]
    next_question_id = PYTHON_QUESTION_LIST[current_question_index + 1]["id"]
    return next_question, next_question_id
    


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
     user_answers = session.get("answers", [])

    # Count the number of correct answers (This is a dummy implementation as the correct answers are not stored)
    num_correct_answers = 0
    for answer in user_answers:
        # In a real implementation, you would compare user's answer with the correct answer from the PYTHON_QUESTION_LIST
        question_id = answer.get("question_id")
        user_answer = answer.get("answer")
        correct_answer = get_correct_answer_by_question_id(question_id)  # Implement this function

        # This is a dummy comparison. Replace this with your actual comparison logic
        if user_answer == correct_answer:
            num_correct_answers += 1

    # Calculate the final score based on the number of correct answers (This is a dummy score calculation)
    total_questions = len(PYTHON_QUESTION_LIST)
    score_per_question = 10  # Assuming each correct answer gives 10 points
    final_score = num_correct_answers * score_per_question

    # Generate the final response based on the score (This is a dummy response)
    final_response = f"Thank you for answering the questions! Your final score is: {final_score} out of {total_questions * score_per_question}."

    return final_response

