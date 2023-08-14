"""
The learner will answer a question with a block of text. The automarker will need to compare that text against a set of answers.
"""

learner_answer_1 = """
Agile is about collaboration, so is devops. It focuses on cross-functional collaboration. There is also a big focus on culture - both agile and dev-ops is about empowering people. Devops is a lot like agile with extra tools and tech stapled on. They both aim to add value as quickly as possible while being sustainable and good for people.
"""

learner_answer_2 = """
The Agile methodology is a project management approach that involves breaking the project into phases and emphasizes continuous collaboration and improvement phases plan, Design, Develop, Test, Deploy, and Review. DevOps is visualized as an infinite loop comprising the steps: plan, code, build, test, release, deploy, operate, monitor, then back to plan, and so on. In a nutshell, DevOps is a natural extension of agile approaches, extending from software development to IT systems and infrastructure management. It strives to emphasize individuals and interactions over processes and documentation.
"""

answer_concepts = [
    s.strip()
    for s in [
        "Collaboration: Both DevOps and Agile emphasize collaboration between development, operations, and other stakeholders.",
        "Iterative Approach: Agile promotes iterative development and continuous feedback, while DevOps extends this to deployment and operations processes.",
        "Continuous Integration (CI): Agile focuses on frequent integration of code, while DevOps integrates automated testing and deployment through CI pipelines.",
        "Continuous Delivery (CD): Agile aims for working software at the end of each sprint, and DevOps extends this to automated, reliable delivery into production.",
        "Flexibility: Agile's adaptive planning aligns with DevOps' ability to rapidly adapt and respond to changes in software and infrastructure.",
        "Customer-Centric: Agile's customer-centric approach aligns with DevOps' emphasis on delivering value to end-users quickly and consistently.",
        "Feedback Loop: Both emphasize continuous feedback from users and stakeholders, improving software quality and operations over time.",
        "Automation: DevOps automates not only deployment but also infrastructure provisioning, aligning with Agile's focus on reducing manual tasks.",
        "Short Feedback Loops: Agile's short development cycles combine with DevOps' quick deployment cycles for rapid identification and resolution of issues.",
        "Cross-Functional Teams: Both encourage cross-functional teams to ensure end-to-end ownership of the software, from development to deployment and operation.",
        "Shared Goals: Both DevOps and Agile share the common goal of delivering high-quality software quickly and efficiently.",
        "Quality Assurance: Agile emphasizes continuous testing, and DevOps extends this to automated testing as part of the deployment pipeline, ensuring consistent quality.",
        "Transparency: Agile's transparency in communication is mirrored in DevOps' emphasis on sharing information and collaborating across teams.",
        "Reduced Risk: Agile's incremental approach reduces project risks; DevOps further mitigates risks by automating deployment and allowing for quick rollbacks.",
        "Frequent Releases: Agile's frequent releases align with DevOps' ability to automate and streamline the release process, making releases more manageable.",
        "Cross-Functional Knowledge: Both promote cross-functional knowledge sharing, ensuring team members understand the entire software lifecycle.",
        "Continuous Improvement: Agile's retrospective meetings for process improvement merge with DevOps' emphasis on continuously enhancing development and operations processes."
        "Efficiency: Agile eliminates wasteful processes, while DevOps eliminates inefficiencies in deployment and operations, leading to smoother workflows.",
        "Empowerment: Agile empowers teams to make decisions; DevOps empowers them to manage the end-to-end software lifecycle.",
        "Customer Satisfaction: Agile's responsiveness to changing requirements complements DevOps' rapid delivery, leading to increased customer satisfaction.",
        "Shorter Time-to-Market: Agile shortens development cycles, and DevOps reduces deployment times, resulting in quicker time-to-market.",
        "Automated Monitoring: DevOps automates monitoring and alerting, aligning with Agile's focus on continuous measurement and improvement.",
        "Cultural Shift: Both require a cultural shift towards collaboration, continuous learning, and embracing change for improved software development.",
        "Value Delivery: Agile's focus on delivering value aligns with DevOps' commitment to delivering features to users faster and more reliably.",
        "Adaptive Planning: Agile's adaptive planning is enhanced by DevOps' ability to quickly adjust deployment and operations strategies based on feedback.",
        "Efficient Communication: Agile's emphasis on face-to-face communication extends into DevOps' emphasis on clear communication between development and operations teams.",
    ]
]

import numpy as np
from InstructorEmbedding import INSTRUCTOR
import spacy
import pandas as pd
import json

NORM_EPS = 1e-30
distance_functions = {
    "l2": lambda x, y: np.linalg.norm(x - y) ** 2,  # type: ignore
    "cosine": lambda x, y: 1 - np.dot(x, y) / ((np.linalg.norm(x) + NORM_EPS) * (np.linalg.norm(y) + NORM_EPS)),  # type: ignore
    "ip": lambda x, y: 1 - np.dot(x, y),  # type: ignore
}

# TODO: This is not DRY. We should be importing all the things.

# distance_function = distance_functions["cosine"]

_embedding_model = INSTRUCTOR("hkunlp/instructor-large", device="cpu")

embedding_function = lambda texts: _embedding_model.encode(texts).tolist()


def embed_sentence(sentence: str) -> np.ndarray:
    """Get the vector representing the meaning of a sentence"""
    return np.array(embedding_function(sentence))


def get_learner_vectors(learner_answer):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(learner_answer)
    learner_sentences = [sent.text.strip() for sent in doc.sents]
    learner_vectors = [embed_sentence(sent) for sent in learner_sentences]
    return learner_vectors, learner_sentences


def get_all_distances(learner_answer, distance_function="cosine"):
    distance_function = distance_functions[distance_function]
    concept_vectors = [embed_sentence(s) for s in answer_concepts]
    learner_vectors, learner_sentences = get_learner_vectors(learner_answer)

    distances = []

    for learner_sentence, learner_vector in zip(learner_sentences, learner_vectors):
        for concept, concept_vector in zip(answer_concepts, concept_vectors):
            distances.append(
                [
                    distance_function(learner_vector, concept_vector),
                    concept.replace(";", ","),  # semicolons break the csv
                    learner_sentence.replace(";", ","),
                ]
            )

    return sorted(distances)


def get_scores(answer, distance_function):
    distances = get_all_distances(answer, distance_function)
    df = pd.DataFrame(distances, columns=["distance", "concept", "sentence"])
    df.sort_values(by=["distance"], inplace=True)
    df.drop_duplicates(subset=["sentence"], keep="first", inplace=True)
    df.drop_duplicates(subset=["concept"], keep="first", inplace=True)

    d = {
        (threshold := 0.05 + 0.01 * n): len(df[df["distance"] < threshold])
        for n in range(10)
    }
    # breakpoint()

    return d


cosine = get_scores(learner_answer_1, "cosine")
print()
print("COSINE Answer 1")
print(json.dumps(cosine, indent=4))

cosine = get_scores(learner_answer_2, "cosine")
print()
print("COSINE Answer 2")
print(json.dumps(cosine, indent=4))

l2 = get_scores(learner_answer_1, "l2")
print()
print("L2 Answer 1")
print(json.dumps(l2, indent=4))

l2 = get_scores(learner_answer_2, "l2")
print()
print("L2 Answer 2")
print(json.dumps(l2, indent=4))

ip = get_scores(learner_answer_1, "ip")
print()
print("IP Answer 1")
print(json.dumps(ip, indent=4))

ip = get_scores(learner_answer_2, "ip")
print()
print("IP Answer 2")
print(json.dumps(ip, indent=4))


# cosine_distances = sorted(get_all_distances("cosine"))
# l2_distances = sorted(get_all_distances("l2"))
# ip_distances = sorted(get_all_distances("ip"))  # < 0.8 seems okish


# with open("gitignore/cosine_distances.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(cosine_distances)

# with open("gitignore/l2_distances.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(l2_distances)

# with open("gitignore/ip_distances.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(ip_distances)

"""
Algorithm:
- couple "concepts" with "hints"
- get vectors for concepts ans learner sentences
- get distances 
- filter duplicates and cutoff
- count rows 
- if the learner didn't get a high enough score then give them a hint from a concept that they missed. 

negative concepts and common mistakes
- have another list of bad_concepts
- do the same exercise to find a number of matching rows. This time if too many lines are matched then tell the learner they got it wrong 
"""
