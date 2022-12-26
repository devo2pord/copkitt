import os
import openai
import argparse
import re

MAX_INPUT_LENGTH = 32

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i",type=str,required=True)
    args = parser.parse_args()
    user_input = args.input

    if validate_length(user_input):
        print(f"User input: {user_input}")
        generate_branding_snippet(user_input)
        generate_keywords(user_input)
    else:
        raise ValueError(
            f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {user_input}"
        )
def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH  

def generate_keywords(propmt: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate related branding keywords for {propmt}"
    print(enriched_prompt)
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=enriched_prompt, max_tokens=32
    )

    # Extract output text.
    keywords_text: str = response["choices"][0]["text"]

    # Strip whitespace.
    keywords_text = keywords_text.strip()
    keywords_array = re.split(",|\n|;|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(f"Keywords: {keywords_array}")
    return keywords_array

def generate_branding_snippet(propmt: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate upbeat branding snippet for {propmt}"
    print(enriched_prompt)
    # TODO: increase max_token so that a full stop can be reached then slice and return a full sentence result.
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=enriched_prompt, max_tokens=32 
    )

    # Extract output text.
    branding_text: str = response["choices"][0]["text"]

    # Strip whitespace.
    branding_text = branding_text.strip()

    # Add ... to trucated statement.
    last_char = branding_text[-1]
    if last_char not in {".", "!","?"}:
        branding_text += "..."

    print(f"Snippet: {branding_text}")
    return branding_text


if __name__ == "__main__":
    main()