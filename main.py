import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Check your api key.")

# instance of the GEMINI API
client = genai.Client(api_key=api_key)

# Python in built in order to settle it with CLI.
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt, tools=[available_functions], temperature=0
    ),
)

if response.usage_metadata.prompt_token_count == None:
    raise RuntimeError("No tokens used, check your api")
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count
prompt = args.user_prompt
function_result_list = []
if response.function_calls != None:
    for function_call in response.function_calls:
        # print(f"Calling function: {function_call.name}({function_call.args})"
        function_call_result = call_function(function_call, verbose=args.verbose)
        if not function_call_result.parts:
            raise Exception("...")
        if not function_call_result.parts[0].function_response:
            raise Exception("...")
        if not function_call_result.parts[0].function_response.response:
            raise Exception("...")
        function_result_list.append(function_call_result.parts[0])
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


else:
    if args.verbose == True:
        print(f"Agent :{response.text}")
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        print(f"Agent :{response.text}")
