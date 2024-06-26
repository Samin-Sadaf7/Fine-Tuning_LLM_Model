import json

import google.generativeai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

GEMINI_API_KEY = "AIzaSyD2dx6j8qsU9qEeikO9duNrIU9644dlqBw"

def generate_by_Gemini(prompt):
    google.generativeai.configure(api_key=GEMINI_API_KEY)
    model = google.generativeai.GenerativeModel(model_name='gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

def get_answer_prompt(actual_answer, question, answer):
    actual_answer = actual_answer.replace("'", "").replace('"', "").replace('\n', "")
    prompt = ("""You are assisting a medical student in preparing for an exam. The student has answered a QUESTION and wants to check if the ANSWER is correct. \
    As an assistant, your job is to examine the ANSWER and provide detailed feedback. You are given the QUESTION and the student's ANSWER to that QUESTION. Also, the actual Answer to that question is given. \
    Now evaluate the student's answer and give detailed feedback. If the answer seems incorrect, also provide the correct answer. \
    Correct Answer: '{actual_answer}'
    QUESTION: '{question}'
    STUDENT'S ANSWER: '{answer}'
    YOUR FEEDBACK: """).format(actual_answer=actual_answer, question=question, answer=answer)
    return prompt

@csrf_exempt
def response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            actual_answer = data.get("actual_answer")
            student_answer = data.get("student_answer")
            question = data.get("question")
            
            if actual_answer and student_answer and question:
                prompt = get_answer_prompt(actual_answer=actual_answer, question=question, answer=student_answer)
                feedback = generate_by_Gemini(prompt=prompt)
                response_message = f"Received: {data.get('message', '')}"
                return JsonResponse({'response': response_message, 'feedback': feedback}, status=200)
            else:
                return JsonResponse({'error': 'Missing one or more required fields'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def echo_view(request, param):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response_message = f"Received: {data.get('message', '')} with URL param: {param}"
            return JsonResponse({'response': response_message})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
