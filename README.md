# you are a developer working on a Python project that automates "innovation"/product ideas by leveraging openAIs APIs to generate focus groups and iterate over product design.
# the project is called cu-autovate
# at its core, when run the program does the following:
# 1. creates an initial set of focus group personas
# 2. interviews the initial focus group around their needs
# 3. based on the initial focus group data, "innovates" a set of new products
# 4. brings that set of new product ideas back to the focus group and conducts feedback interviews
# 5. summarizes that feedback
# 6. evolves the products based on the focus group feedback
# 7. repeats steps 4-7 a set number of iterations
# 8. produces final products based on the iterations
# important points:
# - there is a settings.json file that contains all of the settings to control the program, the user will need to update the settings to their preference prior to running the program
# - there are various prompts in the program that will need to be updated depending on use case, they are in the prompts folder, they will need to be updated prior to running the program
# - example results can be found in the "example-results" branch
# - will need to install the "openai" Python library
# open source under MIT license
# please create a github readme for this project
# the readme should be formatted for github readmes and should include formatting such as headers and lists where appropriate

CU-Autovate is a Python project that automates "innovation"/product ideas by leveraging OpenAI's APIs to generate focus groups and iterate over product design.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Python 3+
2. OpenAI Python library

### Installing

1. Clone the repository

```
git clone https://github.com/username/cu-autovate.git
```

2. Install the OpenAI library

```
pip install openai
```

3. Update the settings.json file to your preference

4. Update the prompts in the prompts folder

### Running

1. Run the program

```
python cu-autovate.py
```

### Results

Example results can be found in the "example-results" branch.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.