from anthropic import Anthropic
import os
import json


def get_anthropic_client():
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    return client


def prompt_to_json(prompt, model="claude-3-opus-20240229"):
    client = get_anthropic_client()
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    json_string = message.content[0].text
    return json.loads(json_string)


def get_distinct_parts_from_review_comments(comment):
    prompt = prompt_break_comment_down.format(comment=comment)
    return prompt_to_json(prompt)


def get_scores_from_comments(comments):
    prompt = prompt_score_all_comments.format(comments_json=json.dumps(comments))
    return prompt_to_json(prompt, model="claude-3-sonnet-20240229")


prompt_break_comment_down = """The following piece of text represents a review left on a piece of code. Please break the text down into distinct points. 

- no information should be thrown away
- if two points cover similar things then they should be combined into a single point

Format the result as a JSON array. Each element in the array should be a string.  Please respond with ONLY the array, please do not include any extra explanations or text.

Here is the text:

{comment}
"""

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


prompt_score_all_comments = """Label the following comments based on the defined scoring criteria. Assign an integer score from 1 (low value) to 10 (high value) for each comment.

Please output a JSON array of integers representing the different scores. Do not output any extra text or explanations.

Here is the scoring criteria:

{comment_score_criteria}

Here is a list of comments, formatted as a JSON array:

{comments_json}
"""
