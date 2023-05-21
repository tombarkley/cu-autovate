# this application will leverage the openai api to create an innovator persona
# that will be used to generate new ideas for a company
# the application will generate a unique id (res_id) for the results set that will be saved and referenced from the results folder
# a new folder under the results folder will be created with the res_id as the folder name
# the persona details for the innovator will be set by the autovator.prompt file in the prompts folder
# the autovator will leverage the openai api to create a focus group that consists of a certain number of personas
# the instruction for the focus group will be set by the focusgroup.prompt file in the prompts folder
# the application will save the focus group personas as individual files in a folder called personas under the res_id folder

# import the openai library
import openai
import os
import json
import time
import datetime
import ast
import random
import shutil
from multiprocessing.pool import ThreadPool

openai.api_key = os.environ["OPENAI_API_KEY"]

# function to import a prompt file
def import_prompt(prompt_name, prompt_type):
    prompt_file_name = "prompts/" + prompt_name + "." + prompt_type
    prompt_file = open(prompt_file_name, "r")
    prompt = prompt_file.read()
    prompt_file.close()
    return prompt

def save_json(folder, file_name, file_content):
    file = open(folder + "/" + file_name, "w")
    file.write(json.dumps(file_content))
    # file.write(file_content)
    file.close()

# function to create a new folder under results
def create_results_folder(res_id):
    res_id = str(res_id)
    results_folder = os.getcwd() + "/results/" + res_id
    os.mkdir(results_folder)
    # create a folder for the focus group personas
    focus_group_personas_folder = results_folder + "/personas"
    os.mkdir(focus_group_personas_folder)
    # create an iterations folder
    iterations_folder = results_folder + "/iterations"
    os.mkdir(iterations_folder)
    iterations_folder = results_folder + "/init_interviews"
    os.mkdir(iterations_folder)
    return results_folder

# function to save iteration results
def save_iteration_results(results_folder, iteration, iteration_results):
    iteration_file_name = results_folder + "/iterations/" + str(iteration) + ".json"
    iteration_file = open(iteration_file_name, "w")
    iteration_file.write(json.dumps(iteration_results))
    iteration_file.close()

def copy_files(prev_directory, new_directory):
    for file in os.listdir(prev_directory):
        shutil.copy(prev_directory + "/" + file, new_directory + "/" + file)

# function to call open ai api to create the focus group personas
def api_create_focus_group_personas(persona_count, settings):
    focus_group_prompt = import_prompt("market_research_firm", "context")
    focus_group_prompt += "\n\n"
    focus_group_prompt += import_prompt("focus_group", "instruction")
    focus_group_prompt += "\n\n"
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "I")
    autovator.replace("[am]", "am")
    focus_group_prompt += autovator
    focus_group_prompt += "\n\n"
    focus_group_prompt += import_prompt("focus_group", "output")
    focus_group_prompt = focus_group_prompt.replace("[persona_count]", str(persona_count))
    return get_ai_completion(focus_group_prompt, "json", [], settings['api'])

def get_ai_completion(prompt, response_type, previous_content=[], input_settings={}):
    api_settings = {
        "temperature": 1.3,
        "max_tokens": 1500,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.75,
        "max_previous_content": 5,
        "max_retries": 3
    }
    # loop through api_settings and update the values with the values in input_settings if they exist
    for key in api_settings:
        if key in input_settings:
            api_settings[key] = input_settings[key]
    
    messages = []
    messages.append({"role": "system", "content": prompt})
    if len(previous_content) > 0:
        if len(previous_content) > api_settings['max_previous_content'] * 2:
            # append the last max_previous_content messages
            for message in previous_content[-api_settings['max_previous_content']*2:]:
                messages.append(message)
        else:
            for message in previous_content:
                messages.append(message)
    retry_count = 0
    if response_type == "text":
        ret_string = ""
        while retry_count < api_settings['max_retries'] or retry_count == 0:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=api_settings['temperature'],
                    max_tokens=api_settings['max_tokens'],
                    frequency_penalty=api_settings['frequency_penalty'],
                    presence_penalty=api_settings['presence_penalty']
                )
                # print("got response")
                # print(response)
                response_string = response.choices[0].message.content
                ret_string = response_string
                retry_count = api_settings['max_retries'] + 1
            except Exception as error:
                print(error)
                print("error parsing response")
                retry_count += 1
                time.sleep(retry_count * 10)
                print()
                try:
                    print(response)
                except:
                    print("error printing response")
        return ret_string
    elif response_type == "json":
        ret_json = []
        while retry_count < api_settings['max_retries'] or retry_count == 0:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=api_settings['temperature'],
                    max_tokens=api_settings['max_tokens'],
                    frequency_penalty=api_settings['frequency_penalty'],
                    presence_penalty=api_settings['presence_penalty']
                )
                # print("got response")
                # print(response)
                response_string = response.choices[0].message.content
                ret_json = ast.literal_eval(response_string)
                retry_count = api_settings['max_retries'] + 1
            except Exception as error:
                print(error)
                print("error parsing response")
                retry_count += 1
                time.sleep(retry_count * 10)
                # print(response)
        return ret_json
    elif response_type == "number_scale":
        ret_num = -1
        while retry_count < api_settings['max_retries'] or retry_count == 0:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=api_settings['temperature'],
                    max_tokens=api_settings['max_tokens'],
                    frequency_penalty=api_settings['frequency_penalty'],
                    presence_penalty=api_settings['presence_penalty']
                )
                # print("got response")
                # print(response)
                response_string = response.choices[0].message.content
                ret_num = int(response_string)
                retry_count = api_settings['max_retries'] + 1
            except Exception as error:
                print(error)
                print("error parsing response")
                retry_count += 1
                time.sleep(retry_count * 10)
                # print(response)
        return ret_num

def get_ai_edit(input, prompt, response_type, input_settings={}):
    api_settings = {
        "temperature": 0.5,
        "top_p": 1.0,
        "max_retries": 3
    }
    for key in api_settings:
        if key in input_settings:
            api_settings[key] = input_settings[key]
    retry_count = 0
    if response_type == "text":
        ret_string = ""
        while retry_count < api_settings['max_retries'] or retry_count == 0:
            try:
                response = openai.Edit.create(
                    model="text-davinci-edit-001",
                    instruction=prompt,
                    input=input,
                    temperature=api_settings['temperature'],
                    top_p=1.0
                )
                # print("got response")
                # print(response)
                response_string = response.choices[0].text
                ret_string = response_string
                retry_count = api_settings['max_retries'] + 1
            except Exception as error:
                print(error)
                print("error parsing response")
                retry_count += 1
                time.sleep(retry_count * 10)
                print()
                try:
                    print(response)
                except:
                    print("error printing response")
        return ret_string
    elif response_type == "json":
        ret_json = []
        while retry_count < api_settings['max_retries'] or retry_count == 0:
            try:
                response = openai.Edit.create(
                    model="text-davinci-edit-001",
                    instruction=prompt,
                    input=input,
                    temperature=api_settings['temperature'],
                    top_p=1.0
                )
                # print("got response")
                # print(response)
                response_string = response.choices[0].text
                ret_json = ast.literal_eval(response_string)
                retry_count = api_settings['max_retries'] + 1
            except Exception as error:
                print(error)
                print("error parsing response")
                retry_count += 1
                time.sleep(retry_count * 10)
                print()
                try:
                    print(response)
                except:
                    print("error printing response")
        return ret_json
    
def create_init_interview_questions(question_count, api_settings):
    questions_prompt = import_prompt("market_research_firm", "context")
    questions_prompt += "\n\n"
    questions_prompt += import_prompt("interview_questions", "instruction")
    questions_prompt += "\n\n"
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "I")
    autovator.replace("[am]", "am")
    questions_prompt += autovator
    questions_prompt += "\n\n"
    questions_prompt += import_prompt("interview_questions", "output")
    questions_prompt = questions_prompt.replace("[question_count]", str(question_count))
    return get_ai_completion(questions_prompt, "json", [], api_settings)

def consumer_init_interview(persona, questions, api_settings):
    # context:
    interview_prompt = import_prompt("consumer_init_interview", "context")
    interview_prompt += "\n\n"
    interview_prompt += "This is your persona: \n\n"
    interview_prompt += json.dumps(persona)
    # instruction:
    interview_prompt += "\n\n"
    interview_prompt += import_prompt("consumer_init_interview", "instruction")
    # input:
    interview_prompt += "\n\n"
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "I")
    autovator.replace("[am]", "am")
    interview_prompt += autovator
    interview_prompt += "\n\n"
    # output:
    interview_prompt += import_prompt("text_conversation", "output")
    interview_results = []
    result_set = []
    for question in questions:
        # print("question:")
        # print(question)
        result_set.append({"role": "user", "content": question})
        question_response = get_ai_completion(interview_prompt, "text", result_set, api_settings)
        # print("response:")
        # print(question_response)
        result_set.append({"role": "assistant", "content": question_response})
        interview_results.append({question: question_response})
    return interview_results

def imagine_products(interview_results, api_settings):
    # context:
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "You")
    autovator.replace("[am]", "are")
    imagine_prompt = autovator
    # instruction:
    imagine_prompt += "\n\n"
    imagine_prompt += import_prompt("imagine_products", "instruction")
    # input:
    imagine_prompt += "\n\n"
    imagine_prompt += import_prompt("imagine_products", "input")
    imagine_prompt += "\n\n"
    imagine_prompt += json.dumps(interview_results)
    imagine_prompt += "\n\n"
    # output:
    imagine_prompt += import_prompt("imagine_products", "output")
    # print(imagine_prompt)
    return get_ai_completion(imagine_prompt, "json", [], api_settings)

def create_feedback_questions(question_count, api_settings):
    questions_prompt = import_prompt("market_research_firm", "context")
    questions_prompt += "\n\n"
    questions_prompt += import_prompt("feedback_questions", "instruction")
    questions_prompt += "\n\n"
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "I")
    autovator.replace("[am]", "am")
    questions_prompt += autovator
    questions_prompt += "\n\n"
    questions_prompt += import_prompt("feedback_questions", "output")
    questions_prompt = questions_prompt.replace("[question_count]", str(question_count))
    return get_ai_completion(questions_prompt, "json", [], api_settings)

def consumer_feedback_interview(product, persona, questions, api_settings):
    print(persona['firstName'])
    # context:
    feedback_prompt = import_prompt("consumer_feedback", "context")
    feedback_prompt += "\n\n"
    feedback_prompt += "This is your persona: \n\n"
    feedback_prompt += json.dumps(persona)
    # instruction:
    feedback_prompt += "\n\n"
    feedback_prompt += "This is the product the credit union is considering launching: \n\n"
    feedback_prompt += json.dumps(product)
    # input:
    feedback_prompt += "\n\n"
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "I")
    autovator.replace("[am]", "am")
    feedback_prompt += autovator
    feedback_prompt += "\n\n"
    # output:
    number_prompt = "Please answer the question on a scale of 1 to 10.  Answer just the integer value - no words."
    text_prompt = import_prompt("text_conversation", "output")
    feedback_results = []
    result_set = []
    for question in questions:
        question_prompt = ""
        if question["response_type"] == "number_scale":
            question_prompt = feedback_prompt + number_prompt
            print("number scale question")
        else:
            question_prompt = feedback_prompt + text_prompt
        result_set.append({"role": "user", "content": question["question"]})
        question_response = get_ai_completion(question_prompt, "text", result_set, api_settings)
        # print("response:")
        # print(question_response)
        if question["response_type"] == "number_scale":
            result_set.append({"role": "assistant", "content": str(question_response)})
        else:
            result_set.append({"role": "assistant", "content": question_response})
        feedback_results.append({question["question"]: question_response})
    return feedback_results

def analyze_product_feedback(feedback_results, response_type, api_settings):
    # context:
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "You")
    autovator.replace("[am]", "are")
    analyze_prompt = autovator
    # instruction:
    analyze_prompt += "\n\n"
    analyze_prompt += import_prompt("analyze_feedback", "instruction")
    # input:
    analyze_prompt += "\n\n"
    analyze_prompt += import_prompt("analyze_feedback", "input")
    analyze_prompt += "\n\n"
    analyze_prompt += json.dumps(feedback_results)
    analyze_prompt += "\n\n"
    # output:
    if response_type == "number_scale":
        analyze_prompt += import_prompt("number_scale", "output")
        return get_ai_completion(analyze_prompt, "json", [], api_settings)
    else:
        analyze_prompt += import_prompt("summary", "output")
        return get_ai_completion(analyze_prompt, "text", [], api_settings)

def edit_product(product, feedback_summary, api_settings):
    # context:
    autovator = import_prompt("autovator", "input")
    autovator.replace("[I]", "You")
    autovator.replace("[am]", "are")
    edit_prompt = autovator
    # instruction:
    edit_prompt += "\n\n"
    edit_prompt += import_prompt("edit_product", "instruction")
    # input:
    edit_prompt += "\n\n"
    edit_prompt += json.dumps(feedback_summary)
    edit_prompt += "\n\n"
    # output:
    edit_prompt += import_prompt("edit_json", "output")
    return get_ai_edit(json.dumps(product), edit_prompt, "json", api_settings)

def create_new_result_set():
    # create a unique id for the results set
    res_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(res_id)

    # create a new folder under results
    results_folder = create_results_folder(res_id)
    return res_id

def set_interview_questions(results_folder, settings):
    if os.path.exists(results_folder + "/init_interview_questions.json"):
        init_interview_questions = json.load(open(results_folder + "/init_interview_questions.json"))
    else:
        init_interview_questions = create_init_interview_questions(settings['question_count'], settings['api'])
        save_json(results_folder, "init_interview_questions.json", init_interview_questions)
    return init_interview_questions

def set_personas(results_folder, settings):
    personas = []
    for file in os.listdir(results_folder + "/personas"):
        personas.append(json.load(open(results_folder + "/personas/" + file)))
    while len(personas) < settings['min_personas']:
        iter_personas = api_create_focus_group_personas(3, settings)
        # append each persona in iter_personas to focus_group_personas
        personas.extend(iter_personas)
        for persona in iter_personas:
            file_name = persona["firstName"] + "-" + persona["age"] + "-" + persona["occupation"] + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".json"
            save_json(results_folder + "/personas", file_name, persona)
    return personas

def conduct_init_interviews(results_folder, personas, init_interview_questions, settings):
    if os.path.exists(results_folder + "/all_interview_results.json"):
        all_interview_results = json.load(open(results_folder + "/all_interview_results.json"))
    else:
        def do_interview(persona):
            if not os.path.exists(results_folder + "/init_interviews/" + persona["firstName"] + "-" + persona["age"] + "-" + persona["occupation"] + ".json"):
                interview_results = consumer_init_interview(persona, init_interview_questions, settings['api'])
                save_json(results_folder + "/init_interviews", persona["firstName"] + "-" + persona["age"] + "-" + persona["occupation"] + ".json", interview_results)
        with ThreadPool() as pool:
            pool.map(do_interview, personas)
        # load the interview results from results/ res_id / init_interviews
        # for each interview question in interview results
        all_interview_results = {}
        for file in os.listdir(results_folder + "/init_interviews"):
            interview_results = json.load(open(results_folder + "/init_interviews/" + file))
            # for each key in interview question
            for item in interview_results: 
                for key in item:
                    # if key is not in all_interview_results dict
                    if key not in all_interview_results:
                        # add key to all_interview_results
                        all_interview_results[key] = []
                    # append interview question to all_interview_results
                    all_interview_results[key].append(item[key])
        # save all_interview_results to results/ res_id / all_interview_results.json
        save_json(results_folder, "all_interview_results.json", all_interview_results)
    return all_interview_results

def create_product_ideas(results_folder, all_interview_results, settings):
    if os.path.exists(results_folder + "/product_ideas.json"):
        product_ideas = json.load(open(results_folder + "/product_ideas.json"))
    else:
        product_ideas = []
        def create_product_idea(i):
            # get a random interview question
            random_question = random.choice(list(all_interview_results.keys()))
            # get the length of the interview question result set
            result_set_length = len(all_interview_results[random_question])
            sample_positions = []
            for j in range(0, settings['sample_size']):
                new_sample = random.randint(0, result_set_length - 1)
                while new_sample in sample_positions:
                    new_sample = random.randint(0, result_set_length - 1)

                sample_positions.append(new_sample)
            # for key in all_interview_results append the value at the random position to random_interview_results
            random_interview_results = {}
            for key in all_interview_results:
                for position in sample_positions:
                    if key not in random_interview_results:
                        random_interview_results[key] = []
                    random_interview_results[key].append(all_interview_results[key][position])       
            product_ideas.append(imagine_products(random_interview_results, settings['api']))
        with ThreadPool() as pool:
            pool.map(create_product_idea, range(0, settings['product_count']))
        # remove products in array that are empty
        product_ideas = [product for product in product_ideas if product]
        save_json(results_folder, "product_ideas.json", product_ideas)
    return product_ideas

def set_feedback_questions(results_folder, settings):
    if os.path.exists(results_folder + "/feedback_questions.json"):
        feedback_questions = json.load(open(results_folder + "/feedback_questions.json"))
    else:
        feedback_questions = create_feedback_questions(settings['question_count'], settings['api'])
        save_json(results_folder, "feedback_questions.json", feedback_questions)
    return feedback_questions

def conduct_feedback_interviews(results_folder, personas, product_ideas, feedback_questions, settings):
    if not os.path.exists(results_folder + "/feedback_interviews"):
        os.makedirs(results_folder + "/feedback_interviews")
    if os.path.exists(results_folder + "/feedback_interviews/feedback_interviews.json"):
        feedback_interviews = json.load(open(results_folder + "/feedback_interviews/feedback_interviews.json"))
    else:
        feedback_interviews = []
        for product in product_ideas:
            # if "name" exists in product
            if "name"  in product:
                product_feedback = {
                    "name": product["name"],
                    "feedback": []
                }
                for item in feedback_questions:
                    product_feedback["feedback"].append({
                        "question": item["question"],
                        "response_type": item["response_type"],
                        "results": []
                    }) 
                product_folder = results_folder + "/feedback_interviews/" + product["name"]
                if not os.path.exists(product_folder):
                    os.makedirs(product_folder)
                def do_interview(persona):
                    if not os.path.exists(product_folder + "/" + persona["firstName"] + "-" + persona["age"] + "-" + persona["occupation"] + ".json"):
                        feedback_interview = consumer_feedback_interview(product, persona, feedback_questions, settings['api'])
                        save_json(product_folder, persona["firstName"] + "-" + persona["age"] + "-" + persona["occupation"] + ".json", feedback_interview)
                with ThreadPool() as pool:
                    pool.map(do_interview, personas)
                # for persona in personas:
                #     if not os.path.exists(product_folder + "/" + persona["firstName"] + "-" + persona["age"] + "-" + persona["occupation"] + ".json"):
                #         feedback_interview = consumer_feedback_interview(product, persona, feedback_questions, settings['api'])
                #         save_json(product_folder, persona["firstName"] + "-" + persona["age"] + "-" + persona["occupation"] + ".json", feedback_interview)
                for file in os.listdir(product_folder):
                    interview_results = json.load(open(product_folder + "/" + file))
                    for item in interview_results:
                        for key in item:
                            for question in product_feedback["feedback"]:
                                if key == question["question"]:
                                    question['results'].append(item[key])
                        #     product_feedback["feedback"][key]["results"].append(item[key])
                        # product_feedback["feedback"][question["question"]]["results"].append(question["answer"])
                    # product_feedback.append(json.load(open(product_folder + "/" + file)))
                save_json(product_folder, "product_feedback.json", product_feedback)
        for folder in os.listdir(results_folder + "/feedback_interviews"):
            feedback_interviews.append(json.load(open(results_folder + "/feedback_interviews/" + folder + "/product_feedback.json")))
        save_json(results_folder + "/feedback_interviews", "feedback_interviews.json", feedback_interviews)
    return feedback_interviews

def sum_feedback_interviews(results_folder, feedback_interviews, settings):
    if os.path.exists(results_folder + "/sum_feedback_interviews.json"):
        sum_feedback_interviews = json.load(open(results_folder + "/sum_feedback_interviews.json"))
    else:
        sum_feedback_interviews = []
        def get_summary(product):
            product_folder = results_folder + "/feedback_interviews/" + product["name"]
            if os.path.exists(product_folder + "/sum_product_feedback_interviews.json"):
                product_feedback = json.load(open(product_folder + "/sum_product_feedback_interviews.json"))
            else:
                product_feedback = {
                    "name": product["name"],
                    "feedback": []
                }
                for feedback in product["feedback"]:
                    sum_feedback = analyze_product_feedback({
                        "question": feedback["question"],
                        "results": feedback["results"]
                    }, feedback["response_type"], settings)
                    product_feedback["feedback"].append({
                        "question": feedback["question"],
                        "results": sum_feedback,
                        "response_type": feedback["response_type"]
                    })
            save_json(product_folder, "sum_product_feedback_interviews.json", product_feedback)
            sum_feedback_interviews.append(product_feedback)
        with ThreadPool() as pool:
            pool.map(get_summary, feedback_interviews)
        save_json(results_folder, "sum_feedback_interviews.json", sum_feedback_interviews)
    return sum_feedback_interviews

def evolve_product(results_folder, products, feedback_summary, settings):
    evolved_folder = results_folder + "/evolved_products"
    if not os.path.exists(evolved_folder):
        os.makedirs(evolved_folder)
    if os.path.exists(results_folder + "/evolved_products.json"):
        evolved_products = json.load(open(evolved_folder + "/evolved_products.json"))
    else:
        evolved_products = []
        def evolve_product(product):
            if os.path.exists(evolved_folder + "/" + product["name"] + ".json"):
                evolved_products.append(json.load(open(evolved_folder + "/" + product["name"] + ".json")))
            else:
                for feedback in feedback_summary:
                    if feedback["name"] == product["name"]:
                        product_feedback_summary = feedback["feedback"]
                
                evolved_product = edit_product(product, product_feedback_summary, settings['api'])
                evolved_products.append(evolved_product)
                save_json(evolved_folder, product["name"] + ".json", evolved_product)
        with ThreadPool() as pool:
            pool.map(evolve_product, products)
        evolved_products = [product for product in evolved_products if product]
        save_json(evolved_folder, "evolved_products.json", evolved_products)
    return evolved_products

def log_milestones(input_text, res_id):
    print(str(datetime.datetime.now()) + ' ' + input_text)
    with open("results/" + str(res_id) + "/log.txt", "a") as myfile:
        myfile.write(str(res_id) + ' ' + str(datetime.datetime.now()) + ' ' + input_text + "\n")

def autovate_instance(res_id):
    results_folder = "results/" + str(res_id)
    log_milestones("Starting autovate instance", res_id)
    settings = json.load(open("settings.json"))
    init_interview_questions = set_interview_questions(results_folder, settings['init_interview_questions'])
    log_milestones("Created init questions", res_id)
    personas = set_personas(results_folder, settings['focus_group'])
    log_milestones("Created personas", res_id)
    all_interview_results = conduct_init_interviews(results_folder, personas, init_interview_questions, settings['init_interview'])
    log_milestones("Conducted init interviews", res_id)
    product_ideas = create_product_ideas(results_folder, all_interview_results, settings['imagine_products'])
    log_milestones("Created init product ideas", res_id)
    for j in range(0, len(settings['iterations'])):
        iter_directory = results_folder + '/iterations/' + str(j)
        if j == 0:
            prev_directory = results_folder
        else:
            prev_directory = results_folder + '/iterations/' + str(j-1)
        if not os.path.exists(iter_directory):
            os.makedirs(iter_directory)
            os.makedirs(iter_directory + "/personas")
        if j == 0 or settings['iterations'][j]['new_questions'] == True:
            if settings['iterations'][j]['new_questions'] == False:
                iteration_question_count = settings['feedback_questions']['question_count']
            else:
                iteration_question_count = settings['iterations'][j]['question_count']
            feedback_questions = set_feedback_questions(iter_directory, {
                "question_count": iteration_question_count,
                "api": settings['feedback_questions']['api']
            })
            log_milestones("Created feedback questions for iteration " + str(j), res_id)
        else:
            feedback_questions = json.load(open(prev_directory + "/feedback_questions.json"))
            save_json(iter_directory, "feedback_questions.json", feedback_questions)
        if settings['iterations'][j]['new_personas'] == True:
            personas = set_personas(iter_directory, {
                "min_personas": settings['iterations'][j]['min_personas'],
                "api": settings['focus_group']['api']
            })
            log_milestones("Created personas for iteration " + str(j), res_id)
        else:
            copy_files(prev_directory + "/personas", iter_directory + "/personas")
            # personas is already set so no need to set again but copying files for trackability
        feedback_interviews = conduct_feedback_interviews(iter_directory, personas, product_ideas, feedback_questions, settings['feedback_interviews'])
        log_milestones("Conducted feedback interviews for iteration " + str(j), res_id)
        feedback_summary = sum_feedback_interviews(iter_directory, feedback_interviews, settings['summarize_feedback'])
        log_milestones("Summarized feedback interviews for iteration " + str(j), res_id)
        product_ideas = evolve_product(iter_directory, product_ideas, feedback_summary, settings['evolve_product'])
        log_milestones("Evolved product ideas for iteration " + str(j), res_id)
    save_json(results_folder, "final_products.json", product_ideas)
    log_milestones("Finished autovate instance", res_id)



# print timestamp
# print(datetime.datetime.now())
# print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

new_result = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
print(new_result)

autovate_instance(20230521120355)


