import time
from parse import EV_parse_data
from llm_select import llm


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


def EVselfC(
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
