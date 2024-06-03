from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview, AgileCard

import os
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


reviewers = [
    "raymond.mawina@umuzi.org",
    "aminat.amusa@umuzi.org",
    "mpho.mashau@umuzi.org",
    "themba.ntuli@umuzi.org",
    "ngoako.ramokgopa@umuzi.org",
    "percival.rapha@umuzi.org",
    "sbonelo.mkhize@umuzi.org",
    "vuyisanani.meteni@umuzi.org",
]

comments = [
    "Nicely Done!",
    'Your project failed some of our tests. Here are the details:\n\n# Test suite: test_person_interests\n## Test: test_many_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Samuel", age=12, gender="male", interests=\\["turtles","elephants","wizards","luggage"\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Samuel. I am 12 years old. I am male. My interests are turtles, elephants, wizards and luggage.` but we expected `Hello, my name is Samuel, my gender is male and I am 12 years old. My interests are turtles, elephants, wizards and luggage.`.\n## Test: test_no_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Tshepo", age=54, gender="male", interests=\\[\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Tshepo. I am 54 years old. I am male. I have no interest.` but we expected `Hello, my name is Tshepo, my gender is male and I am 54 years old. I have no interests.`.\n## Test: test_one_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Margret", age=23, gender="female", interests=\\["chess"\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Margret. I am 23 years old. I am female. My interest is chess.` but we expected `Hello, my name is Margret, my gender is female and I am 23 years old. My interest is chess.`.\n## Test: test_two_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Kiki", age=32, gender="female", interests=\\["cheese","wine"\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Kiki. I am 32 years old. I am female. My interests are cheese and wine.` but we expected `Hello, my name is Kiki, my gender is female and I am 32 years old. My interests are cheese and wine.`.\n----------------------------------------',
    'FINAL STATUS: not yet competent\n----------------------------------------\n# REVIEW:\n\nFINAL REVIEW STATUS: not yet competent\n\nYour project failed some of our tests. Here are the details:\n\n# Test suite: test_person_interests\n## Test: test_no_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Tshepo", age=54, gender="male", interests=\\[\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Tshepo, my gender is male and I am 54 years old. I have no interest.` but we expected `Hello, my name is Tshepo, my gender is male and I am 54 years old. I have no interests.`.\n----------------------------------------',
    "Nicely done!",
    "Nice work! all requested changes were addressed.",
    'FINAL STATUS: not yet competent\n----------------------------------------\n# REVIEW:\n\nFINAL REVIEW STATUS: not yet competent\n\nYour project failed some of our tests. Here are the details:\n\n# Test suite: test_person_interests\n## Test: test_many_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Samuel", age=12, gender="male", interests=\\["turtles","elephants","wizards","luggage"\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Samuel. My gender is male and I am 12 years old. My interests are turtles, elephants, wizards and luggage.` but we expected `Hello, my name is Samuel, my gender is male and I am 12 years old. My interests are turtles, elephants, wizards and luggage.`.\n## Test: test_no_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Tshepo", age=54, gender="male", interests=\\[\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Tshepo. My gender is male and I am 54 years old. I have no interest.` but we expected `Hello, my name is Tshepo, my gender is male and I am 54 years old. I have no interests.`.\n## Test: test_one_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Margret", age=23, gender="female", interests=\\["chess"\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Margret. My gender is female and I am 23 years old. My interest is chess.` but we expected `Hello, my name is Margret, my gender is female and I am 23 years old. My interest is chess.`.\n## Test: test_two_interests\n### FAILURE: There was an error when we tried to Constructed a person with the arguments (name="Kiki", age=32, gender="female", interests=\\["cheese","wine"\\]) and then call the hello method:\nYour code returned the wrong value. It returned `Hello, my name is Kiki. My gender is female and I am 32 years old. My interests are cheese and wine.` but we expected `Hello, my name is Kiki, my gender is female and I am 32 years old. My interests are cheese and wine.`.\n----------------------------------------',
    "The requested changes were addressed, well done.",
    "Nicely done!",
    "Your work made my day, line number 10 is the juice for me. Good work buddy.",
    "LGTM, Great work",
]


# class Command(BaseCommand):
#     def handle(self, *args, **options):


comment_score_criteria = """
1. General Approval or Disapproval:

Examples: "Looks good", "LGTM", "Needs work","Nice job", "I like this"
Score: 1/10
Value: Very low, as they provide no specific information or actionable feedback.

2. Superficial Observations:

Examples: "Not sure about this"
Score: 2/10
Value: Low, as they still lack specific details or guidance.
Medium-Value Comments

3. Specific Praise or Criticism Without Detail:

Examples: "Good use of the singleton pattern", "This method is too complex"
Score: 4/10
Value: Moderate, as they identify areas of strength or weakness but do not elaborate on why or how to improve.

4. Pointing Out Issues or Bugs:

Examples: "This could cause a null pointer exception", "This function doesn't handle edge cases"
Score: 5/10
Value: Moderate to high, as they highlight potential problems but may not provide solutions.
High-Value Comments
Detailed Explanations:

5. Examples: "Using a singleton pattern here is good because it ensures there's only one instance, which is crucial for this part of the application. However, consider lazy initialization to improve performance."
Score: 7/10
Value: High, as they provide in-depth reasoning and context.

6. Constructive Feedback with Suggestions:

Examples: "This method is too complex. Consider breaking it down into smaller, more manageable functions. This will improve readability and maintainability."
Score: 8/10
Value: High, as they not only identify issues but also suggest practical improvements.

7. Code Examples or References:

Examples: "This loop can be optimized. Here's a link to a more efficient algorithm: [link]. Also, see the code snippet below for a possible refactor."
Score: 9/10
Value: Very high, as they provide tangible examples and resources for improvement.

8. Comprehensive Review with Multiple Insights:

Examples: "Overall, this code is well-structured. Here are a few suggestions: 1) Simplify the if-else logic on line 45, 2) Add comments to explain the regex pattern on line 72, 3) Consider using a list comprehension on line 85 for better readability."
Score: 10/10
Value: Very high, as they offer a thorough review with multiple actionable points, helping the author to improve the code significantly.
These criteria can be used to score comments based on their depth, specificity, and helpfulness, ensuring that feedback provided during code reviews is both constructive and valuable.

9. Negative reviews

Examples: "Here is the code you need. Just paste it in", "What an idiot"
Score: Negative score, depending on the severity 

"""


prompt_score_all_comments = f"""Label the following comments based on the defined scoring criteria. Assign an integer score from 1 (low value) to 10 (high value) for each comment.

Please output a JSON array of integers representing the different scores. Do not output any extra text or explanations.

Here is the scoring criteria:

{comment_score_criteria}

Here is a list of comments, formatted as a JSON array:

{comments}
"""


prompt_score_single_comment = f"""Label the following comment based on the defined scoring criteria. Assign an integer score from 1 (low value) to 10 (high value) .

Please output an integer score and nothing else.

Here is the scoring criteria:

{comment_score_criteria}

Here is the comment:

{comment}
"""


prompt_break_comment_down = f"""The following piece of text represents a review left on a piece of code. Please break the text down into distinct points. 

- no information should be thrown away
- if two points cover similar things then they should be combined into a single point

Format the result as a JSON array. Each element in the array should be a string.  Please respond with ONLY the array, please do not include any extra explanations or text.

Here is the text:

{comment}
"""


message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": prompt_break_comment_down,
        }
    ],
    model="claude-3-opus-20240229",
)
print(message.content[0].text)
