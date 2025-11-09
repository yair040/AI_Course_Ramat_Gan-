"""
Task 1: Generate random sentences categorized by subject
"""

import random
from utils import save_sentences, SENTENCES_FILE, RANDOM_SEED, NUM_SENTENCES


# Sentence templates for each category
SPORT_TEMPLATES = [
    "I enjoy playing {sport} every weekend",
    "The {team} won the championship this year",
    "Training for the {event} is very challenging",
    "{sport} requires excellent physical conditioning",
    "Watching {sport} games is my favorite pastime",
    "The {team} has talented players this season",
    "I practice {sport} three times a week",
    "The {event} competition was incredibly exciting",
    "Professional {sport} athletes inspire me greatly",
    "Our local {team} made it to the finals",
]

FOOD_TEMPLATES = [
    "I love eating {food} for dinner",
    "The {dish} tastes absolutely delicious",
    "Cooking {meal} is my favorite hobby",
    "Fresh {food} from the market is wonderful",
    "This {dish} recipe is easy to prepare",
    "I always order {food} at restaurants",
    "Homemade {meal} is better than takeout",
    "The aroma of {food} makes me hungry",
    "I discovered a new {dish} recipe today",
    "Traditional {meal} brings back childhood memories",
]

WORK_TEMPLATES = [
    "The meeting starts at {time} tomorrow",
    "I finished the {task} project successfully",
    "Working on {activity} today was productive",
    "The {task} deadline is next week",
    "I need to complete the {activity} report",
    "Our team discussed {task} strategies today",
    "The {activity} presentation went very well",
    "I have a conference call at {time}",
    "Collaborating on {task} with colleagues is enjoyable",
    "The {activity} workshop was highly informative",
]

# Word lists for filling templates
SPORT_WORDS = [
    'basketball', 'soccer', 'tennis', 'swimming', 'volleyball',
    'baseball', 'hockey', 'golf', 'running', 'cycling'
]

TEAM_WORDS = [
    'Tigers', 'Eagles', 'Warriors', 'Champions', 'Spartans',
    'Knights', 'Dragons', 'Panthers', 'Falcons', 'Lions'
]

EVENT_WORDS = [
    'marathon', 'tournament', 'championship', 'competition',
    'triathlon', 'playoffs', 'finals', 'Olympics', 'race', 'match'
]

FOOD_WORDS = [
    'pizza', 'sushi', 'pasta', 'salad', 'sandwich',
    'burger', 'tacos', 'rice', 'soup', 'steak'
]

DISH_WORDS = [
    'lasagna', 'curry', 'stir-fry', 'casserole', 'risotto',
    'paella', 'ramen', 'pho', 'chili', 'gumbo'
]

MEAL_WORDS = [
    'breakfast', 'lunch', 'dinner', 'brunch', 'feast',
    'banquet', 'barbecue', 'buffet', 'picnic', 'potluck'
]

TASK_WORDS = [
    'marketing', 'budget', 'research', 'development', 'design',
    'analysis', 'planning', 'implementation', 'testing', 'documentation'
]

ACTIVITY_WORDS = [
    'training', 'brainstorming', 'review', 'audit', 'evaluation',
    'assessment', 'optimization', 'integration', 'deployment', 'monitoring'
]

TIME_WORDS = [
    '9 AM', '10 AM', '2 PM', '3 PM', '4 PM',
    'noon', 'morning', 'afternoon', 'evening', 'midnight'
]


def generate_sentence(category: str) -> str:
    """
    Generate one sentence for the given category

    Args:
        category: One of 'sport', 'food', or 'work'

    Returns:
        Generated sentence string
    """
    if category == 'sport':
        template = random.choice(SPORT_TEMPLATES)
        # Determine which placeholder to fill
        if '{sport}' in template:
            return template.format(sport=random.choice(SPORT_WORDS))
        elif '{team}' in template:
            return template.format(team=random.choice(TEAM_WORDS))
        elif '{event}' in template:
            return template.format(event=random.choice(EVENT_WORDS))

    elif category == 'food':
        template = random.choice(FOOD_TEMPLATES)
        if '{food}' in template:
            return template.format(food=random.choice(FOOD_WORDS))
        elif '{dish}' in template:
            return template.format(dish=random.choice(DISH_WORDS))
        elif '{meal}' in template:
            return template.format(meal=random.choice(MEAL_WORDS))

    elif category == 'work':
        template = random.choice(WORK_TEMPLATES)
        if '{task}' in template:
            return template.format(task=random.choice(TASK_WORDS))
        elif '{activity}' in template:
            return template.format(activity=random.choice(ACTIVITY_WORDS))
        elif '{time}' in template:
            return template.format(time=random.choice(TIME_WORDS))

    return "Default sentence"


def generate_sentences(n: int = NUM_SENTENCES, seed: int = RANDOM_SEED) -> list:
    """
    Generate n sentences with random category assignment

    Args:
        n: Number of sentences to generate
        seed: Random seed for reproducibility

    Returns:
        List of generated sentences
    """
    random.seed(seed)
    sentences = []
    categories = ['sport', 'food', 'work']

    for i in range(n):
        category = random.choice(categories)
        sentence = generate_sentence(category)
        sentences.append(sentence)

    return sentences


def main():
    """Main execution for Task 1"""
    print("=" * 60)
    print("TASK 1: Generate Sentences")
    print("=" * 60)

    # Generate sentences
    sentences = generate_sentences()

    # Print to console
    print(f"\nGenerated {len(sentences)} sentences:\n")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i:3d}. {sentence}")

    # Save to file
    save_sentences(sentences, SENTENCES_FILE)
    print(f"\n✓ Sentences saved to {SENTENCES_FILE}")

    return sentences


if __name__ == "__main__":
    main()
