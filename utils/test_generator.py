import random
from typing import Dict, List

# Question bank organised by skill (expandable)
QUESTION_BANK: Dict[str, List[Dict]] = {
    "python": [
        {"question": "What is the difference between a list and a tuple in Python?",
         "options": ["Lists are mutable, tuples are immutable", "Tuples are mutable, lists are immutable",
                     "Both are mutable", "Both are immutable"],
         "correct_answer": "Lists are mutable, tuples are immutable"},
        {"question": "What does the 'self' keyword refer to in Python?",
         "options": ["The class itself", "The current instance of the class",
                     "A built-in variable", "A global reference"],
         "correct_answer": "The current instance of the class"},
        {"question": "Which of the following is used to handle exceptions in Python?",
         "options": ["try-except", "if-else", "for-while", "switch-case"],
         "correct_answer": "try-except"},
        {"question": "What is a decorator in Python?",
         "options": ["A function that modifies another function",
                     "A class attribute", "A loop construct", "A data type"],
         "correct_answer": "A function that modifies another function"},
        {"question": "What is the output of len([1, [2, 3], 4])?",
         "options": ["3", "4", "5", "Error"],
         "correct_answer": "3"},
    ],
    "javascript": [
        {"question": "What is the difference between '==' and '===' in JavaScript?",
         "options": ["'===' checks type and value, '==' checks only value",
                     "They are identical", "'==' is stricter", "None of the above"],
         "correct_answer": "'===' checks type and value, '==' checks only value"},
        {"question": "What is a closure in JavaScript?",
         "options": ["A function with access to its outer scope",
                     "A way to close the browser", "A type of loop", "A CSS feature"],
         "correct_answer": "A function with access to its outer scope"},
        {"question": "Which method adds an element to the end of an array?",
         "options": ["push()", "pop()", "shift()", "unshift()"],
         "correct_answer": "push()"},
        {"question": "What does 'typeof null' return in JavaScript?",
         "options": ["'object'", "'null'", "'undefined'", "'boolean'"],
         "correct_answer": "'object'"},
        {"question": "What is the purpose of 'async/await'?",
         "options": ["Handle asynchronous operations", "Create classes",
                     "Define variables", "Style elements"],
         "correct_answer": "Handle asynchronous operations"},
    ],
    "sql": [
        {"question": "What does SQL stand for?",
         "options": ["Structured Query Language", "Simple Query Language",
                     "Standard Query Logic", "System Query Language"],
         "correct_answer": "Structured Query Language"},
        {"question": "Which SQL keyword is used to retrieve data?",
         "options": ["SELECT", "GET", "FETCH", "RETRIEVE"],
         "correct_answer": "SELECT"},
        {"question": "What is a PRIMARY KEY?",
         "options": ["A unique identifier for each record",
                     "The first column in a table", "A foreign reference", "An index"],
         "correct_answer": "A unique identifier for each record"},
        {"question": "Which clause is used to filter results?",
         "options": ["WHERE", "FILTER", "HAVING", "LIMIT"],
         "correct_answer": "WHERE"},
        {"question": "What does JOIN do in SQL?",
         "options": ["Combines rows from two or more tables",
                     "Deletes duplicate rows", "Creates a new table", "Sorts the results"],
         "correct_answer": "Combines rows from two or more tables"},
    ],
    "data structures": [
        {"question": "What is the time complexity of searching in a balanced BST?",
         "options": ["O(log n)", "O(n)", "O(1)", "O(n^2)"],
         "correct_answer": "O(log n)"},
        {"question": "Which data structure uses FIFO?",
         "options": ["Queue", "Stack", "Tree", "Graph"],
         "correct_answer": "Queue"},
        {"question": "What is a hash table?",
         "options": ["A structure that maps keys to values using a hash function",
                     "A sorted array", "A linked list variant", "A type of tree"],
         "correct_answer": "A structure that maps keys to values using a hash function"},
        {"question": "Which data structure uses LIFO?",
         "options": ["Stack", "Queue", "Array", "Linked List"],
         "correct_answer": "Stack"},
        {"question": "What is the worst-case time complexity of inserting into an unsorted array?",
         "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
         "correct_answer": "O(1)"},
    ],
}

# Generic fallback questions
_GENERIC_QUESTIONS = [
    {"question": "What is the most important concept in {skill}?",
     "options": ["Fundamentals", "Syntax", "Libraries", "Frameworks"],
     "correct_answer": "Fundamentals"},
    {"question": "Which learning approach is best for {skill}?",
     "options": ["Practice-based learning", "Only reading docs",
                 "Watching videos only", "Memorisation"],
     "correct_answer": "Practice-based learning"},
    {"question": "How would you stay updated with {skill}?",
     "options": ["Follow official docs and community", "Ignore updates",
                 "Only use old versions", "Avoid community forums"],
     "correct_answer": "Follow official docs and community"},
]


def generate_test_questions(skill_name: str, num_questions: int = 5) -> List[Dict]:
    """Generate interview-style multiple-choice questions for a given skill."""
    skill_key = skill_name.lower().strip()
    bank = QUESTION_BANK.get(skill_key, None)

    if bank:
        selected = random.sample(bank, min(num_questions, len(bank)))
    else:
        # Use generic fallback questions
        selected = [
            {k: v.replace("{skill}", skill_name) if isinstance(v, str) else v for k, v in q.items()}
            for q in _GENERIC_QUESTIONS[:num_questions]
        ]

    return selected
