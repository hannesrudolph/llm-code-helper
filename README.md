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
Context: I am working on existing code that I need to be modified. I will provide line numbers for each line of code. Use the line numbers as refences but ignore them otherwise. 

```
Please provide your suggested code changes in the following JSON format:

```json
[
  {
    "type": "remove",
    "lines": "LINE_NUMBERS",
    "text": "",
    "first_original_line": "FIRST_LINE_OF_ORIGINAL_TEXT_TO_BE_REMOVED"
  },
  {
    "type": "insertafter",
    "lines": "LINE_NUMBER",
    "text": "CODE_TO_INSERT",
    "first_original_line": "ORIGINAL_TEXT_AFTER_WHICH_CODE_SHOULD_BE_INSERTED"
  },
  {
    "type": "replace",
    "lines": "LINE_NUMBERS",
    "text": "REPLACEMENT_CODE",
    "first_original_line": "FIRST_LINE_OF_ORIGINAL_TEXT_TO_BE_REPLACED"
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
  * **first_original_line:** Just the first line of the original code that is being modified. This is used to verify the original text before making changes.
    * For `"remove"`, this is the first line of the text being removed.
    * For `"insertafter"`, this is the line that will be above the inserted line.
    * For `"replace"`, this is the first line of the text being replaced.

**Important Points to Prevent Off-by-One Errors:**

1. **Context Awareness:** Ensure that the `first_original_line` provided in the JSON matches exactly with the first line of the code to be removed, inserted after, or replaced. This line is crucial for accurately locating the position for changes.
2. **Line Number Calculation:** Verify that the line numbers specified in the `lines` field are correct and correspond to the actual lines in the original code.
3. **Review Before Applying:** Before applying the changes, review the JSON output to confirm that the line numbers and the `first_original_line` values match your expectations. This will help catch any off-by-one errors before they are introduced.

**Example:**

```json
[
  {
    "type": "remove",
    "lines": "13",
    "text": "",
    "first_original_line": "    echo 'Line to be removed';"
  },
  {
    "type": "insertafter",
    "lines": "25",
    "text": "    echo 'Inserted line of code';",
    "first_original_line": "    echo 'Line above inserted code';"
  },
  {
    "type": "replace",
    "lines": "30-32",
    "text": "    function new_function() {\n        return 'New function';\n    }",
    "first_original_line": "    function old_function() {"
  }
]
```

**Benefits:**

* **Structured Data:** This JSON format provides a clear and structured way to represent code changes, making it easier to parse and apply them programmatically using the `process-changes` endpoint.
* **Reduced Ambiguity:** The specific format reduces ambiguity and ensures that the AI assistant's instructions are interpreted correctly.
* **Improved Efficiency:** By providing instructions in this format, you can streamline the process of applying code changes and avoid the need for manual interpretation or rewriting.
* **Verification:** The inclusion of the original text allows for verification before making changes, reducing the risk of unintended modifications.

If you understand my instructions and the context, please indicate it with a one-sentence response.
````

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).