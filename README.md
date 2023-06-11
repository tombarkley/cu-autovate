<!---
you are a developer working on a Python project that automates "innovation"/product ideas by leveraging openAIs APIs to generate focus groups and iterate over product design.
the project is called cu-autovate
at its core, when run the program does the following:
    1. creates an initial set of focus group personas
    2. interviews the initial focus group around their needs
    3. based on the initial focus group data, "innovates" a set of new products
    4. brings that set of new product ideas back to the focus group and conducts feedback interviews
    5. summarizes that feedback
    6. evolves the products based on the focus group feedback
    7. repeats steps 4-7 a set number of iterations
    8. produces final products based on the iterations
important points:
    - there is a settings.json file that contains all of the settings to control the program, the user will need to update the settings to their preference prior to running the program
    - there are various prompts in the program that will need to be updated depending on use case, they are in the prompts folder, they will need to be updated prior to running the program
    - example results can be found in the "example-results" branch
    - will need to install the "openai" Python library
open source under MIT license
please create a github readme for this project
the readme should be formatted for github readmes and should include formatting such as headers and lists where appropriate
--->

CU-Autovate is a Python project that automates "innovation"/product ideas by leveraging openAIs APIs to generate focus groups and iterate over product design.

## Table of Contents

- [Basic Overview](#basic-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [Usage](#usage)
  - [settings.json](#settingsjson)
  - [prompts](#prompts)
  - [Running the Program](#running-the-program)
- [Example Results](#example-results)
- [License](#license)

## Basic Overview

When run, the program does the following:

1. Creates an initial set of focus group personas
2. Interviews the initial focus group around their needs
3. Based on the initial focus group data, "innovates" a set of new products
4. Brings that set of new product ideas back to the focus group and conducts feedback interviews
5. Summarizes that feedback
6. Evolves the products based on the focus group feedback
7. Repeats steps 4-7 a set number of iterations
8. Produces final products based on the iterations


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need to install the "openai" Python library.

### Installing

Clone this repository to your local machine.

```
git clone https://github.com/tombarkley/cu-autovate.git
```

## Usage

Before running the program, you will need to update the settings in the `settings.json` file to your preference. You will also need to update the prompts in the `prompts` folder prior to running the program.
<!---
this is what the settings.json file looks like:
{
    "focus_group": {
        "min_personas": 10,
        "api": {
            "temperature": 1.00,
            "frequency_penalty": 0,
            "presence_penalty": 1.25,
            "max_retries": 15
        }
    },
    "init_interview": {
        "api": {
            "temperature": 0.75,
            "frequency_penalty": 0,
            "presence_penalty": 0.75,
            "max_previous_content": 2,
            "max_retries": 15
        }
    },
    "init_interview_questions": {
        "question_count": 4,
        "api": {
            "temperature": 0.75,
            "frequency_penalty": 0,
            "presence_penalty": 0.75,
            "max_retries": 15
        }
    },
    "imagine_products": {
        "product_count": 10,
        "sample_size": 3,
        "api": {
            "temperature": 1.00,
            "frequency_penalty": 0,
            "presence_penalty": 0.75,
            "max_retries": 15
        }
    },
    "feedback_questions": {
        "question_count": 7,
        "api": {
            "temperature": 0.75,
            "frequency_penalty": 0,
            "presence_penalty": 0.75,
            "max_retries": 15
        }
    },
    "feedback_interviews": {
        "api": {
            "temperature": 0.45,
            "frequency_penalty": 0,
            "presence_penalty": 0.25,
            "max_retries": 10
        }
    },
    "summarize_feedback": {
        "api": {
            "temperature": 0.25,
            "frequency_penalty": 0,
            "presence_penalty": 0.25,
            "max_retries": 15
        }
    },
    "evolve_product": {
        "api": {
            "temperature": 0.50,
            "frequency_penalty": 0,
            "presence_penalty": 0.75,
            "max_retries": 15
        }
    },
    "iterations": [
        {
            "new_personas": false,
            "new_questions": false
        },
        {
            "new_personas": true,
            "min_personas": 10,
            "new_questions": true,
            "question_count": 8
        },
        {
            "new_personas": true,
            "min_personas": 10,
            "new_questions": true,
            "question_count": 5
        } 
    ]
}
--->
### settings.json

The `settings.json` file contains all of the settings to control the program. You will need to update the settings to your preference prior to running the program.

There are the following sections in the `settings.json` file:

  - focus_group (object) - contains the settings for the initial focus group personas
    - min_personas (int) - controls the minimum number of personas to generate for the initial focus group
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - init_interview (object) - contains the settings for the initial focus group interviews (only api settings)
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - init_interview_questions (object) - contains the settings for the initial focus group interview questions
    - question_count (int) - controls the number of questions to ask the initial focus group
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - imagine_products (object) - contains the settings for the inital product generation
    - product_count (int) - controls the number of products to generate
    - sample_size (int) - controls the number of responses to feed to the generation function
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - feedback_questions (object) - contains the settings for the feedback questions
    - question_count (int) - controls the number of questions to ask the focus group
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - feedback_interviews (object) - contains the settings for the feedback interviews (only api settings)
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - summarize_feedback (object) - contains the settings for the feedback summary (only api settings)
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - evolve_product (object) - contains the settings for the product evolution (only api settings)
    - api (object) - contains the settings for the openAI API call
      - temperature (float) - controls the randomness of the output
      - frequency_penalty (float) - controls how often the same word is repeated
      - presence_penalty (float) - controls how often the same word is repeated
      - max_retries (int) - controls how many times the API call will be retried if it fails
  - iterations (array of objects) - contains the settings for the iterations
    - new_personas (bool) - controls whether new personas will be generated
    - min_personas (int) - controls the minimum number of personas to generate
    - new_questions (bool) - controls whether new questions will be generated
    - question_count (int) - controls the number of questions to ask the focus group

### prompts

The `prompts` folder contains the prompt files for the program. The prompt files are used to generate the personas, questions, and products. They can be changed to allow different purposes without having to change the underlying code.

The prompt files are combined in the order below for each function:

  - Creating Initial Interview Questions 
    - `market_research_firm.context`
    - `interview_questions.instruction`
    - `autovator.input`
    - `interview_questions.output`
  - Creating Focus Group Personas
    - `market_research_firm.context`
    - `focus_group.instruction`
    - `autovator.input`
    - `focus_group.output`
  - Conducting Initial Interviews
    - `consumer_init_interview.context`
    - `consumer_init_interview.instruction`
    - `autovator.input`
    - `text_conversation.output`
  - Creating Initial Products
    - `autovator.input`
    - `imagine_products.instruction`
    - `imagine_products.input`
    - `imagine_products.output`
  - Creating Feedback Questions
    - `market_research_firm.context`
    - `feedback_questions.instruction`
    - `autovator.input`
    - `feedback_questions.output`
  - Conducting Feedback Interviews
    - `consumer_feedback.context`
    - The instruction here feeds the personas and products from the previous steps
    - `autovator.input`
    - `text_conversation.output`
  - Summarizing Feedback
    - `autovator.input`
    - `analyze_feedback.instruction`
    - `analyze_feedback.input`
    - Either of:
      - `number_scale.output`
      - `summary.output`
  - Evolving Products
    - `autovator.input`
    - `edit_product.instruction`
    - The input is the feedback from the interviews
    - `edit_json.output`

### Running the Program

To run the program, simply execute the `cu-autovate.py` file.

```
python cu-autovate.py
```

## Example Results

Example results can be found in the [`example-results`](https://github.com/tombarkley/cu-autovate/blob/example-results/results_toc.md) branch.

## License

This project is open source under the MIT License.