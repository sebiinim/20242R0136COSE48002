# JSON 문자열을 딕셔너리로 파싱
import json
import time
import re

from llm_select import llm

EV_error = """
{
    "description" : None,
    "score" : None
}"""

RV_error = """
{
    "descritpion" : None,
    "revision" : None
}"""


# 키와 값의 타입을 검증하는 함수
def EV_validate(data):
    required_keys = {"description": str, "score": int}

    # 각 키를 검사
    for key, expected_type in required_keys.items():
        if key not in data or not isinstance(
            data[key], expected_type
        ):  # key와 value type 체크
            return False

    return True


def EV_parse_data(raw_string):
    # 일단 파싱 및 테스트 시도
    try:
        data = json.loads(raw_string)
        if EV_validate(data):
            return data  # 올바른 상황
        else:
            return EV_error  # json 형식이지만 key, value 등에서 오류가 있는 상황
    # LLM 사용해서 파싱
    except json.JSONDecodeError:
        # LLM을 통해 올바른 JSON 형식으로 수정 요청
        #         1. 출력은 반드시 중괄호 {}로 시작하고 끝나야 합니다. 2. key는 description, score 2개이며 각 타입은 str, int 입니다. 3. 모든 키와 값은 큰따옴표(")로 감싸야 합니다. score의 value인 int는 제외합니다. 4. 출력 시 모든 특수문자를 제거하십시오. 5. JSON 포맷만 반환하십시오. (추가 설명 금지)
        prompt = """ 다음 입력을 JSON 파싱이 가능한 형식으로 변환하십시오. 
        """
        res = llm.invoke(raw_string + prompt).content

        match = re.search(r"\{.*\}", res, re.DOTALL)
        if match != None:
            res = match.group(0)

        print("111" + res)
        try:  # 파싱 시도
            data = json.loads(res)
            if EV_validate(data):  # key, value가 유효함
                return data
            else:  # 유효하지 않으면 EV 에러 값 리턴
                return EV_error

        except json.JSONDecodeError:  # 파싱 실패
            return EV_error


def RV_validate(data):
    required_keys = {"description": str, "revision": str}

    # 각 키를 검사
    for key, expected_type in required_keys.items():
        if key not in data:  # key 체크
            return False
        if not isinstance(data[key], expected_type):  # value의 type 체크
            return False

    return True


def RV_parse_data(raw_string):
    # 일단 파싱 및 테스트 시도
    try:
        data = json.loads(raw_string)
        if RV_validate(data):
            return data  # 파싱이 되면 그대로 리턴
        else:
            return RV_error
    # LLM 사용해서 파싱
    except json.JSONDecodeError:
        # LLM을 통해 올바른 JSON 형식으로 수정 요청
        #         1. 출력은 반드시 중괄호 {}로 시작하고 끝나야 합니다. 2. key는 description, revision 2개이며 각 타입은 str, int 입니다. 3. 모든 키와 값은 큰따옴표(")로 감싸야 합니다. score의 value인 int는 제외합니다. 4. 출력 시 모든 특수문자를 제거하십시오. 5. JSON 포맷만 반환하십시오. (추가 설명 금지)
        prompt = """ 다음 입력을 JSON 파싱이 가능한 형식으로 변환하십시오. 
        """
        res = llm.invoke(raw_string + prompt).content

        match = re.search(r"\{.*\}", res, re.DOTALL)
        res = match.group(0)

        try:  # 파싱 시도
            data = json.loads(res)
            if RV_validate(data):  # key, value가 유효함
                return data
            else:  # 유효하지 않으면 EV 에러 값 리턴
                return RV_error

        except json.JSONDecodeError:  # 파싱 실패
            return RV_error


# input: score 3개, des 3개
# output: 과반수 score, 병합된 des
def whowins(score1, score2, score3, des1, des2, des3):
    scores = [score1, score2, score3]
    dess = [des1, des2, des3]

    score_des_dict = {}
    for score, des in zip(scores, dess):
        if score in score_des_dict:
            score_des_dict[score].append(des)
        else:
            score_des_dict[score] = [des]

    # 점수들의 집합을 생성하여 유일한 값들의 개수를 셈
    unique_scores = set(scores)

    if len(unique_scores) == 1:
        # 모든 값이 같을 경우
        win_score = score1
        win_des = llm.invoke(
            "세 문장을 조합해서 재구성해줘: " + ", ".join(score_des_dict[win_score])
        ).content
    elif len(unique_scores) == 2:
        # 두 값이 같고 하나만 다른 경우
        for score in unique_scores:
            if scores.count(score) == 2:
                win_score = score
                win_des = llm.invoke(
                    "두 문장을 조합해서 재구성해줘: "
                    + ", ".join(score_des_dict[win_score])
                ).content
                break
    else:
        # 셋 다 다른 경우, 중간값을 반환
        win_score = sorted(scores)[1]
        win_des = score_des_dict[win_score][0]

    raw_string = "win_score: " + str(win_score) + ",\n" + "win_des: " + win_des + ",\n"

    res = EV_parse_data(raw_string)
    iterator = iter(res.items())
    key1, value1 = iterator.__next__()
    key2, value2 = iterator.__next__()
    win_score = value1
    win_des = value2
    return win_score, win_des


def selfC(
    EVRVfunc,
    input_sentence,
    upper_objective,
    memory,
    guideline,
    example1,
    example2,
    example3,
    isguide,
    isexample,
    criteria,
):
    print("\nselfC")
    res1 = EVRVfunc(
        input_sentence, upper_objective, memory, guideline, example1, isguide, isexample
    )
    iterator = iter(res1.items())
    key1, value1 = iterator.__next__()
    key2, value2 = iterator.__next__()
    des_1, score_1 = value1, value2
    print(f"des_1: {des_1}")
    print(f"score_1: {score_1}")
    time.sleep(3)

    res2 = EVRVfunc(
        input_sentence, upper_objective, memory, guideline, example2, isguide, isexample
    )
    iterator = iter(res2.items())
    key1, value1 = iterator.__next__()
    key2, value2 = iterator.__next__()
    des_2, score_2 = value1, value2
    print(f"des_2: {des_2}")
    print(f"score_2: {score_2}")
    time.sleep(3)

    res3 = EVRVfunc(
        input_sentence, upper_objective, memory, guideline, example3, isguide, isexample
    )
    iterator = iter(res3.items())
    key1, value1 = iterator.__next__()
    key2, value2 = iterator.__next__()
    des_3, score_3 = value1, value2
    print(f"des_3: {des_3}")
    print(f"score_3: {score_3}")
    time.sleep(3)

    winscore, windes = whowins(score_1, score_2, score_3, des_1, des_2, des_3)
    res = {
        f"predict_{criteria}_description": windes,
        f"predict_{criteria}_score": winscore,
    }
    time.sleep(3)
    return res
