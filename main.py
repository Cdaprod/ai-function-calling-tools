# LOAD KEYS ONELINER
import os, getpass
from dotenv import load_dotenv; load_dotenv()
api_keys = {k: __import__('os').getenv(k) or __import__('getpass').getpass(f"Enter {k}: ") for k in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]}

client = OpenAI(api_key=api_keys['OPENAI_API_KEY'])

func_call_tools = [
  {
    "type": "function",
    "function": {
      "name": "APICallTool",
      "description": "Dynamically constructs and sends HTTP requests to external APIs.",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "description": "The endpoint URL of the API to be called."
          },
          "method": {
            "type": "string",
            "enum": ["GET", "POST", "PUT", "DELETE"],
            "description": "The HTTP method to use."
          },
          "headers": {
            "type": "object",
            "description": "An object containing headers for the request."
          },
          "body": {
            "type": "object",
            "description": "Payload to send with POST/PUT requests."
          }
        },
        "required": ["url", "method"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "DataExtractionTool",
      "description": "Extracts specific data points from structured text.",
      "parameters": {
        "type": "object",
        "properties": {
          "data": {
            "type": "string",
            "description": "The raw data from which to extract information."
          },
          "pattern": {
            "type": "string",
            "description": "The regex pattern or query to use for data extraction."
          }
        },
        "required": ["data", "pattern"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "CodeExecutionTool",
      "description": "Executes code snippets in specified programming languages.",
      "parameters": {
        "type": "object",
        "properties": {
          "language": {
            "type": "string",
            "description": "The programming language of the code."
          },
          "code": {
            "type": "string",
            "description": "The code snippet to execute."
          }
        },
        "required": ["language", "code"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "DatabaseQueryTool",
      "description": "Executes SQL or NoSQL queries on a connected database.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The SQL or NoSQL query to execute."
          },
          "dbConnection": {
            "type": "object",
            "description": "Connection details for the database."
          }
        },
        "required": ["query", "dbConnection"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "TextGenerationTool",
      "description": "Generates or completes text based on prompts using a language model.",
      "parameters": {
        "type": "object",
        "properties": {
          "prompt": {
            "type": "string",
            "description": "The initial text or prompt for text generation."
          },
          "maxTokens": {
            "type": "integer",
            "description": "The maximum number of tokens to generate."
          }
        },
        "required": ["prompt"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "DataValidationTool",
      "description": "Validates input data against predefined rules or formats.",
      "parameters": {
        "type": "object",
        "properties": {
          "data": {
            "type": "object",
            "description": "The data object to validate."
          },
          "rules": {
            "type": "object",
            "description": "Validation rules for acceptable formats and values."
          }
        },
        "required": ["data", "rules"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "FileManagementTool",
      "description": "Manages file operations like reading, writing, moving, or deleting files.",
      "parameters": {
        "type": "object",
        "properties": {
          "filePath": {
            "type": "string",
            "description": "Path to the file for the operation."
          },
          "operation": {
            "type": "string",
            "enum": ["read", "write", "move", "delete"],
            "description": "The type of file operation to perform."
          },
          "content": {
            "type": "string",
            "description": "Content to write to a file (if applicable)."
          }
        },
        "required": ["filePath", "operation"]
      }
    }
  }
]


def execute_tool_call(tool_name, args):
    """
    Executes the appropriate tool based on the provided tool name and arguments.

    :param tool_name: Name of the tool to execute.
    :param args: Arguments required for the tool execution.
    :return: Result of the tool execution.
    """

    # Dictionary mapping tool names to their corresponding functions
    tool_functions = {
        "APICallTool": execute_api_call,
        "DataExtractionTool": extract_data,
        "CodeExecutionTool": execute_code,
        "DatabaseQueryTool": execute_database_query,
        "TextGenerationTool": generate_text,
        "DataValidationTool": validate_data,
        "FileManagementTool": manage_file
    }

    try:
        # Ensure the tool exists in the dictionary
        if tool_name in tool_functions:
            # Call the corresponding function with the appropriate arguments
            if tool_name == "APICallTool":
                return tool_functions[tool_name](
                    url=args.get("url"),
                    method=args.get("method"),
                    headers=args.get("headers", {}),
                    body=args.get("body", {})
                )
            elif tool_name == "DataExtractionTool":
                return tool_functions[tool_name](
                    data=args.get("data"),
                    pattern=args.get("pattern")
                )
            elif tool_name == "CodeExecutionTool":
                return tool_functions[tool_name](
                    language=args.get("language"),
                    code=args.get("code")
                )
            elif tool_name == "DatabaseQueryTool":
                return tool_functions[tool_name](
                    query=args.get("query"),
                    db_connection=args.get("dbConnection")
                )
            elif tool_name == "TextGenerationTool":
                return tool_functions[tool_name](
                    prompt=args.get("prompt"),
                    max_tokens=args.get("maxTokens", 100)
                )
            elif tool_name == "DataValidationTool":
                return tool_functions[tool_name](
                    data=args.get("data"),
                    rules=args.get("rules")
                )
            elif tool_name == "FileManagementTool":
                return tool_functions[tool_name](
                    file_path=args.get("filePath"),
                    operation=args.get("operation"),
                    content=args.get("content", "")
                )
        else:
            return f"Error: Unknown tool '{tool_name}'"
    
    except Exception as e:
        return f"Error executing tool '{tool_name}': {e}"

# Example implementations for tool functions
def execute_api_call(url, method, headers=None, body=None):
    # Simulate API call execution
    return f"API call to {url} with method {method} executed."

def extract_data(data, pattern):
    # Simulate data extraction
    return f"Data extracted from text using pattern '{pattern}'."

def execute_code(language, code):
    if language.lower() == 'python':
        exec(code)
        return "Python code executed successfully."
    else:
        return f"Code execution not supported for language: {language}"

def execute_database_query(query, db_connection):
    # Simulate database query execution
    return f"Database query '{query}' executed on connection {db_connection}."

def generate_text(prompt, max_tokens):
    # Simulate text generation
    return f"Generated text based on prompt: '{prompt}' with max tokens: {max_tokens}."

def validate_data(data, rules):
    # Simulate data validation
    return f"Data validated against rules: {rules}."

def manage_file(file_path, operation, content=None):
    # Simulate file management operations
    return f"File operation '{operation}' executed on '{file_path}' with content: {content}."

def execute_block(user_input):
    """
    Main execution block for processing user input, determining the appropriate tool,
    routing to the correct AI service, and executing the tool.

    :param user_input: The input string from the user that needs processing.
    :return: Result of the executed tool or error message.
    """
    # Prepare the initial messages for AI
    messages = [
        {"role": "system", "content": "Analyze the user's input and determine the best function tool to use based on the context provided."},
        {"role": "user", "content": user_input}
    ]

    # Initial AI response to determine which tool to use
    ai_response = chat_completion_request(messages, tools=ai_function_tools)

    if not ai_response:
        return "Error: Failed to get response from AI."

    try:
        # Check if the AI response includes a tool call
        tool_call = ai_response.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        # Determine which AI service to use based on the tool
        ai_service = determine_ai_service(tool_name)

        # Log AI service selection
        print(f"AI Service selected: {ai_service} for tool: {tool_name}")

        # Route to the appropriate AI service
        if ai_service == "OpenAI":
            service_response = make_openai_request(messages=messages, tools=[tool_call])
        elif ai_service == "Anthropic":
            service_response = make_anthropic_request(messages=messages, tools=[tool_call])
        else:
            return f"Error: No valid AI service found for tool '{tool_name}'"

        if not service_response:
            return "Error: AI service request failed."

        # Extract the tool call result from the service response
        if 'choices' in service_response and len(service_response['choices']) > 0:
            execution_result = execute_tool_call(tool_name, tool_args)
            return execution_result
        else:
            return "Error: AI service response does not contain valid choices."

    except Exception as e:
        return f"Unexpected error occurred: {e}"

# Example Usage
if __name__ == "__main__":
    user_input = "Extract all email addresses from the following text: 'Contact us at info@example.com or support@sample.org.'"
    result = execute_block(user_input)
    print(result)