#!/usr/bin/env python
import sys
from is_your_reputation_tracker_part_of_crew_automation.crew import IsYourReputationTrackerPartOfCrewAutomationCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'company_name': 'sample_value',
        'aliases': 'sample_value',
        'website': 'sample_value',
        'social_media_handles': 'sample_value',
        'sentiment_model_config': 'sample_value',
        'neg_threshold': 'sample_value'
    }
    IsYourReputationTrackerPartOfCrewAutomationCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'company_name': 'sample_value',
        'aliases': 'sample_value',
        'website': 'sample_value',
        'social_media_handles': 'sample_value',
        'sentiment_model_config': 'sample_value',
        'neg_threshold': 'sample_value'
    }
    try:
        IsYourReputationTrackerPartOfCrewAutomationCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        IsYourReputationTrackerPartOfCrewAutomationCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'company_name': 'sample_value',
        'aliases': 'sample_value',
        'website': 'sample_value',
        'social_media_handles': 'sample_value',
        'sentiment_model_config': 'sample_value',
        'neg_threshold': 'sample_value'
    }
    try:
        IsYourReputationTrackerPartOfCrewAutomationCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
