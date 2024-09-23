
import pandas as pd
from datasets import load_dataset
import pandas as pd

dataset = load_dataset("squad_v2")
def convert_to_jsonl(squad_data, output_path):
    """ Convert SQuAD data to JSONL format """
    data = []

    # Iterate through the data to extract question, context, and answers
    for item in squad_data:
        context = item['context']
        question = item['question']
        # Check if there are answers; SQuAD 2.0 includes unanswerable questions
        if item['answers']['text']:
            answer_text = item['answers']['text'][0]  # Taking the first answer if available
            answer_start = item['answers']['answer_start'][0]
        else:
            answer_text = ''
            answer_start = -1
        
        # Append data in a format suitable for model training
        data.append({
            'context': context,
            'question': question,
            'answer_text': answer_text,
            'answer_start': answer_start
        })
    
    # Convert to DataFrame then to JSONL
    df = pd.DataFrame(data)
    df.to_json(output_path, orient='records', lines=True, force_ascii=False)

# Prepare the data from the train split
convert_to_jsonl(dataset['train'], 'squad_train.jsonl')

