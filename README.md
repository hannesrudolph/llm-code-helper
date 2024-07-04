# LLM Code Helper Ver 2

## Description

LLM Code Helper is a utility designed to facilitate interaction with a Language Learning Model (LLM) for suggesting code modifications. It provides a convenient way to format your code with line numbers, improving the LLM's understanding and accuracy. Additionally, this tool can apply the LLM's suggestions, which are returned in a JSON format, directly to your code.

> :warning: **Important Note**: This application is currently in its testing phase. It may contain bugs, and there are likely areas for improvement to enhance usability. If you utilize this code, we kindly ask that you contribute back any improvements you make. Due to life's demands, we haven't had as much time as we'd like to refine this tool. Your contributions are greatly appreciated!

## Installation

1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Run `pip install -r requirements.txt` to install all the necessary dependencies.

## Usage

1. Run `python app.py` to start the application.
2. Go to `http://localhost:5000` and paste your code into the box and press `Format Code`.
3. Copy the formatted code.
4. Provide your LLM instructions for what you want to do and then paste your copied code (with line numbers) after your instructions (make sure to put your pasted code in triple backticks ```` ``` ````).
5. Go to `http://localhost:5000` and navigate to `/process-changes`.
6. Paste your original code without line numbers into the first box.
7. Copy the JSON from the LLM response into the second box and press the `Process Changes` button.
8. Copy your new code with the copy button and paste it into your original codebase.

## Custom LLM Prompt

Here is a LLM prompt I start with. Change the initial `Context:` instructions to suit your situation.

````
Context: I am working on a WordPress plugin using PHP 8.2.

```
Please provide your suggested code changes in the following JSON format:

```json
[
  {
    "type": "remove",
    "lines": "LINE_NUMBERS",
    "text": ""
  },
  {
    "type": "insertafter",
    "lines": "LINE_NUMBER",
    "text": "CODE_TO_INSERT"
  },
  {
    "type": "replace",
    "lines": "LINE_NUMBERS",
    "text": "REPLACEMENT_CODE"
  }
]
```

**Explanation of JSON Format:**

* **Array of Changes:** The response should be a JSON array, where each element represents a single change to be made to the code.
* **Change Object:** Each change object must have the following properties:
  * **type:** A string indicating the type of change. It can be one of the following:
    * `"remove"`: To delete lines of code.
    * `"insertafter"`: To insert code after a specific line.
    * `"replace"`: To replace lines of code with new code.
  * **lines:** A string specifying the line numbers affected by the change.
    * For `"remove"` and `"replace"`, this can be a single line number (e.g., `"15"`) or a range of lines (e.g., `"10-20"`).
    * For `"insertafter"`, this should be the line number after which the new code should be inserted.
  * **text:** A string containing the code to be inserted or used as a replacement. For `"remove"` changes, this should be an empty string (`""`).

**Example:**

```json
[
  {
    "type": "remove",
    "lines": "13",
    "text": ""
  },
  {
    "type": "insertafter",
    "lines": "25",
    "text": "console.log('This is the inserted code.');"
  },
  {
    "type": "replace",
    "lines": "30-32",
    "text": "// This is the replacement code."
  }
]
```

**Benefits:**

* **Structured Data:** This JSON format provides a clear and structured way to represent code changes, making it easier to parse and apply them programmatically using the `process-changes` endpoint.
* **Reduced Ambiguity:** The specific format reduces ambiguity and ensures that the AI assistant's instructions are interpreted correctly.
* **Improved Efficiency:** By providing instructions in this format, you can streamline the process of applying code changes and avoid the need for manual interpretation or rewriting.

If you understand my instructions and the context, please indicate it with a one-sentence response.
````

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).