# category_selector.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_category_id_from_prompt(prompt):
    """
    Uses OpenAI to determine the most relevant YouTube category ID from a user's prompt.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # List of available YouTube category IDs and their names
    # This is crucial for the model to pick a valid category
    youtube_categories = {
        '23': 'Comedy', '24': 'Entertainment', '22': 'People & Blogs',
        '10': 'Music', '17': 'Sports', '20': 'Gaming',
        '28': 'Science & Technology', '26': 'Howto & Style',
        '27': 'Education', '1': 'Film & Animation',
        '15': 'Pets & Animals', '25': 'News & Politics',
        '2': 'Autos & Vehicles', '19': 'Travel & Events'
    }

    # The prompt instructs the model to return a single category ID
    prompt_for_category = f"""
    Based on the following user prompt, identify the most relevant YouTube video category ID from the list provided.
    
    Prompt: "{prompt}"
    
    Available Categories and IDs:
    {json.dumps(youtube_categories, indent=2)}
    
    Your response should be a single string containing only the category ID. Do not include any other text or explanation.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that identifies the best YouTube category ID for a given topic."},
                {"role": "user", "content": prompt_for_category}
            ]
        )
        
        category_id = response.choices[0].message.content.strip()

        # Simple validation to make sure the ID is in our list
        if category_id in youtube_categories:
            print(f"OpenAI selected category: '{youtube_categories[category_id]}' (ID: {category_id})")
            return category_id
        else:
            print(f"OpenAI returned an invalid category ID: {category_id}")
            return None

    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return None

if __name__ == '__main__':
    # Test the function
    test_prompt = "A video about a cat playing the piano"
    cat_id = get_category_id_from_prompt(test_prompt)
    if cat_id:
        print(f"The recommended category ID is: {cat_id}")