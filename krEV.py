from krEVprompt import krEV_connectivity_description, kr_background_template, krEV_connectivity_example_prompt, krEV_connectivity_examples, krEV_connectivity_examples_1, krEV_connectivity_examples_2, krEV_connectivity_examples_3, krEV_connectivity_suffix, krEV_directivity_description, krEV_directivity_example_prompt, krEV_directivity_examples, krEV_directivity_examples_1, krEV_directivity_examples_2, krEV_directivity_examples_3, krEV_directivity_suffix, krEV_measurability_description, krEV_measurability_example_prompt, krEV_measurability_examples, krEV_measurability_examples_1, krEV_measurability_examples_2, krEV_measurability_examples_3, krEV_measurability_suffix, krEV_task_description

from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.chains import ConversationChain
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import copy
import json
import time
import re

from parse import parse_data, selfC
from main import llm, train_df, test_df

def krconnectivityEV(input_sentence, upper_objective, guideline_con, example_con, isguide, isexample):
  keyResult_memory = ConversationBufferMemory()

  # 1. 메모리의 system_message에 Task Description 추가
  keyResult_memory.save_context(
    inputs={"human": krEV_task_description},
    outputs={"AI": "해결할 과제를 학습했습니다."},
  )
  
  if isguide:
    prefix_guideline = '- 주어진 가이드라인을 평가에 이용하세요'
    guideline_con = guideline_con
  else:
    prefix_guideline = ' '
    guideline_con = ' '
    for example in example_con:
      example["guideline"] = ' '

  if isexample:
    prefix_example = '- 예시는 참고용일 뿐입니다. 현재 주어진 input_sentence와 upper_objective에 집중하여 평가하세요.'
  else:
    prefix_example = ' '

  prefix = krEV_connectivity_description.format(prefix_guideline = prefix_guideline, prefix_example = prefix_example)
  suffix = krEV_connectivity_suffix.format(input_sentence = input_sentence, upper_objective = upper_objective, guideline_con = guideline_con)

  krEV_connectivity_fewshot_prompt = FewShotPromptTemplate(
    prefix = prefix + '\n\n',
    examples = example_con,
    example_prompt = krEV_connectivity_example_prompt,
    suffix = suffix
  )

  if isexample:
    final_prompt = krEV_connectivity_fewshot_prompt.format(input_sentence=input_sentence, upper_objective=upper_objective)
  else:
    final_prompt = prefix + suffix

  # print(type(final_prompt))
  # print('*'*50, '\n', final_prompt, '\n', '*'*50)

  chain_connectivity = ConversationChain(
    llm=llm,
    memory=keyResult_memory,
  )

  krEV_connectivity = chain_connectivity.run(final_prompt)

  res = parse_data(krEV_connectivity)
  return res

# res = krconnectivityEV("인사를 잘 한다", "칭찬을 받는다", "con 가이드라인", krEV_connectivity_examples_1, True, True)
# print(res)
# print(type(res))

def krmeasurabilityEV(input_sentence, upper_objective, guideline_mea, example_mea, isguide, isexample):
  keyResult_memory = ConversationBufferMemory()

  # 1. 메모리의 system_message에 Task Description 추가
  keyResult_memory.save_context(
    inputs={"human": krEV_task_description},
    outputs={"AI": "해결할 과제를 학습했습니다."},
  )
  
  if isguide:
    prefix_guideline = '- 주어진 가이드라인을 평가에 이용하세요'
    guideline_mea = guideline_mea
  else:
    prefix_guideline = ' '
    guideline_mea = ' '
    for example in example_mea:
      example["guideline"] = ' '

  if isexample:
    prefix_example = '- 예시는 참고용일 뿐입니다. 현재 주어진 input_sentence와 upper_objective에 집중하여 평가하세요.'
  else:
    prefix_example = ' '

  prefix = krEV_measurability_description.format(prefix_guideline = prefix_guideline, prefix_example = prefix_example)
  suffix = krEV_measurability_suffix.format(input_sentence = input_sentence, upper_objective = upper_objective, guideline_mea = guideline_mea)

  krEV_measurability_fewshot_prompt = FewShotPromptTemplate(
    prefix = prefix + '\n\n',
    examples = example_mea,
    example_prompt = krEV_measurability_example_prompt,
    suffix = suffix
  )

  if isexample:
    final_prompt = krEV_measurability_fewshot_prompt.format(input_sentence=input_sentence, upper_objective=upper_objective)
  else:
    final_prompt = prefix + suffix

  # print(type(final_prompt))
  # print('*'*50, '\n', final_prompt, '\n', '*'*50)

  chain_measurability = ConversationChain(
    llm=llm,
    memory=keyResult_memory,
  )

  krEV_measurability = chain_measurability.run(final_prompt)

  res = parse_data(krEV_measurability)
  return res

# res = krmeasurabilityEV("인사를 잘 한다", "칭찬을 받는다", "mea 가이드라인", krEV_measurability_examples_2, True, True)
# print(res)
# print(type(res))

def krdirectivityEV(input_sentence, upper_objective, guideline_dir, example_dir, isguide, isexample):
  keyResult_memory = ConversationBufferMemory()

  # 1. 메모리의 system_message에 Task Description 추가
  keyResult_memory.save_context(
    inputs={"human": krEV_task_description},
    outputs={"AI": "해결할 과제를 학습했습니다."},
  )
  
  if isguide:
    prefix_guideline = '- 주어진 가이드라인을 평가에 이용하세요'
    guideline_dir = guideline_dir
  else:
    prefix_guideline = ' '
    guideline_dir = ' '
    for example in example_dir:
      example["guideline"] = ' '

  if isexample:
    prefix_example = '- 예시는 참고용일 뿐입니다. 현재 주어진 input_sentence와 upper_objective에 집중하여 평가하세요.'
  else:
    prefix_example = ' '

  prefix = krEV_directivity_description.format(prefix_guideline = prefix_guideline, prefix_example = prefix_example)
  suffix = krEV_directivity_suffix.format(input_sentence = input_sentence, upper_objective = upper_objective, guideline_dir = guideline_dir)

  krEV_directivity_fewshot_prompt = FewShotPromptTemplate(
    prefix = prefix + '\n\n',
    examples = example_dir,
    example_prompt = krEV_directivity_example_prompt,
    suffix = suffix
  )

  if isexample:
    final_prompt = krEV_directivity_fewshot_prompt.format(input_sentence=input_sentence, upper_objective=upper_objective)
  else:
    final_prompt = prefix + suffix

  # print(type(final_prompt))
  # print('*'*50, '\n', final_prompt, '\n', '*'*50)

  chain_directivity = ConversationChain(
    llm=llm,
    memory=keyResult_memory,
  )

  krEV_directivity = chain_directivity.run(final_prompt)

  res = parse_data(krEV_directivity)
  return res

res = krdirectivityEV("인사를 잘 한다", "칭찬을 받는다", "dir 가이드라인", krEV_directivity_examples_1, True, True)
print(res)
print(type(res))

# kr 평가, 기존 가이드라인 이용
def krEV(df_data, index, isguide, isexample):
  # 메모리 생성
  keyResult_memory = ConversationBufferMemory()

  # 1. 메모리의 system_message에 Task Description 추가
  keyResult_memory.save_context(
    inputs={"human": krEV_task_description},
    outputs={"AI": "해결할 과제를 학습했습니다."},
  )

  # 1.5 df_data에서 값 가져오기
  input_sentence = df_data.loc[index, 'input_sentence']
  upper_objective = df_data.loc[index, 'upper_objective']
  company = df_data.loc[index, 'company']
  field = df_data.loc[index, 'field']
  team = df_data.loc[index, 'team']
  
  if (df_data.loc[index, "type"] != "Key Result"):
    print("Key Result가 아닙니다.")
    return

  guideline_con = ''
  guideline_mea = ''
  guideline_dir = ''
  if isguide:
    guideline_con = df_data.loc[index]['Connectivity_Question']
    guideline_mea = df_data.loc[index]['Measurability_Question']
    guideline_dir = df_data.loc[index]['Directivity_Question']


  print("index: ",index)
  print(f"row_num: {df_data.loc[index]['row_num']}")
  print("guideline_con :"+ str(guideline_con))
  print("guideline_mea :"+ str(guideline_mea))
  print("guideline_dir :"+ str(guideline_dir))
  print(f"input_sentence: {input_sentence}")
  print(f"upper_objective: {upper_objective}")
  print('\n')


  # 2. 메모리의 human_message에 background 정보 추가
  keyResult_background = kr_background_template.format(
    company=company,                  #회사명
    field=field,                      #업종
    team=team,                        #팀명
  )

  keyResult_memory.save_context(
    inputs={"system": keyResult_background},
    outputs={"AI": "기업의 배경 정보를 학습했습니다."},
  )

  # 2.5 평가요소마다 메모리 만들기
  krEV_memory_connectivity = copy.deepcopy(keyResult_memory)
  krEV_memory_measurability = copy.deepcopy(keyResult_memory)
  krEV_memory_directivity = copy.deepcopy(keyResult_memory)

  # 평가 시행
  krEV_connectivity = krconnectivityEV(input_sentence, upper_objective, krEV_memory_connectivity, guideline_con, krEV_connectivity_examples, isguide, isexample)
  krEV_measurability = krmeasurabilityEV(input_sentence, upper_objective, krEV_memory_measurability, guideline_mea, krEV_measurability_examples, isguide, isexample)
  krEV_directivity = krdirectivityEV(input_sentence, upper_objective, krEV_memory_directivity, guideline_dir, krEV_directivity_examples, isguide, isexample)

  return krEV_connectivity | krEV_measurability | krEV_directivity



# kr 평가, 기존 가이드라인 이용
# def krEV_selfC(df_data, index, isguide, isexample):
  # 메모리 생성
  keyResult_memory = ConversationBufferMemory()

  # 1. 메모리의 system_message에 Task Description 추가
  keyResult_memory.save_context(
    inputs={"human": krEV_task_description},
    outputs={"AI": "해결할 과제를 학습했습니다."},
  )

  # 1.5 df_data에서 값 가져오기
  input_sentence = df_data.loc[index, 'input_sentence']
  upper_objective = df_data.loc[index, 'upper_objective']
  company = df_data.loc[index, 'company']
  field = df_data.loc[index, 'field']
  team = df_data.loc[index, 'team']

  guideline_con = ''
  guideline_mea = ''
  guideline_dir = ''
  if isguide:
    guideline_con = df_data.loc[index]['Connectivity_Question']
    guideline_mea = df_data.loc[index]['Measurability_Question']
    guideline_dir = df_data.loc[index]['Directivity_Question']

  print("index: ",index)
  print(f"row_num: {df_data.loc[index]['row_num']}")
  print("guideline_con :"+ str(guideline_con))
  print("guideline_mea :"+ str(guideline_mea))
  print("guideline_dir :"+ str(guideline_dir))
  print(f"input_sentence: {input_sentence}")
  print(f"upper_objective: {upper_objective}")
  print('\n')


  # 2. 메모리의 human_message에 background 정보 추가
  keyResult_background = kr_background_template.format(
    company=company,                  #회사명
    field=field,                      #업종
    team=team,                        #팀명
  )

  keyResult_memory.save_context(
    inputs={"system": keyResult_background},
    outputs={"AI": "기업의 배경 정보를 학습했습니다."},
  )

  # 2.5 평가요소마다 메모리 만들기
  krEV_memory_connectivity = copy.deepcopy(keyResult_memory)
  krEV_memory_measurability = copy.deepcopy(keyResult_memory)
  krEV_memory_directivity = copy.deepcopy(keyResult_memory)

  # 평가 시행
  krEV_connectivity = selfC(krconnectivityEV, input_sentence, upper_objective, krEV_memory_connectivity, guideline_con,
                            krEV_connectivity_examples_1, krEV_connectivity_examples_2, krEV_connectivity_examples_3, isguide, isexample, "connectivity")
  krEV_measurability = selfC(krmeasurabilityEV, input_sentence, upper_objective, krEV_memory_measurability, guideline_mea,
                            krEV_measurability_examples_1, krEV_measurability_examples_2, krEV_measurability_examples_3, isguide, isexample, "measurability")
  krEV_directivity = selfC(krdirectivityEV, input_sentence, upper_objective, krEV_memory_directivity, guideline_dir,
                          krEV_directivity_examples_1, krEV_directivity_examples_2, krEV_directivity_examples_3, isguide, isexample, "directivity")

  #print(krEV_connectivity + krEV_measurability + krEV_directivity)
  # 결과 저장, 문자열 메소드 이용
  df_data = krEVsaveResult(df_data, index, krEV_connectivity | krEV_measurability | krEV_directivity)

  #결과 출력
  print("\n<evaluation result>")
  print(f"predict_connectivity_description: {df_data.loc[index, 'predict_connectivity_description']}")
  print(f"predict_connectivity_score: {df_data.loc[index, 'predict_connectivity_score']}")
  print(f"predict_measurability_description: {df_data.loc[index, 'predict_measurability_description']}")
  print(f"predict_measurability_score: {df_data.loc[index, 'predict_measurability_score']}")
  print(f"predict_directivity_description: {df_data.loc[index, 'predict_directivity_description']}")
  print(f"predict_directivity_score: {df_data.loc[index, 'predict_directivity_score']}")
  print('\n')