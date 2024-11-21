import openai
from Utilities import get_content_from_tweet_csv



def summarize_tweet(file_name):
    """
    Function to send the user input to the ChatGPT model and return the analysis.
    """
    tweet_content = get_content_from_tweet_csv(file_name)
    # print(f"Tweet content: {tweet_content}") 
    client = openai.OpenAI(api_key='Enter your API key here')
    try:
        # Create a chat completion
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify the model to use
            messages=[
                {"role": "system", "content": "这是我爬取的一些推文内容，请帮我详细总结下每一条推文的内容。"},
                {"role": "user", "content": tweet_content}
            ],
            max_tokens=5000,  # Limit the response length
            temperature=0.7    # Adjust creativity level
        )

        # Extract the model's reply
        analysis = response.choices[0].message.content
        return analysis

    except Exception as e:
        return f"An error occurred: {e}"
    
if __name__ == '__main__':
    print(summarize_tweet("tweet.csv"))