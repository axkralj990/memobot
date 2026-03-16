from dotenv import load_dotenv
from src.openai_parser import parse_daily_entry

load_dotenv()

if __name__ == "__main__":
    # Example messages
    examples = [
        "Today I slept 7 hours, had 2 coffees, feeling pretty anxious (maybe a 4), took my omega3 and vitamins, went for a cold shower for 5 minutes",
        "Great productive day! Slept well, did 20 min meditation, ate salmon for lunch, feeling good physically and mentally calm",
        "Rough day, barely slept 5 hours, drank 3 coffees to stay awake, anxiety through the roof, productivity was low"
    ]
    
    # Or use custom input
    message = input("Describe your day: ")
    
    entry = parse_daily_entry(message)
    print("\n" + "="*50)
    print("Parsed Entry:")
    print("="*50)
    print(entry.model_dump_json(indent=2))
