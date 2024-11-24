from langchain.prompts import PromptTemplate

krEV_task_description = """
당신은 세계적으로 인정받는 OKR(Objectives and Key Results) 전문 컨설턴트입니다. 당신의 임무는 주어진 Key Result를 철저히 분석하고 평가하여, 조직의 목표 달성을 위한 최적의 OKR 수립을 지원하는 것입니다.

평가 대상:
input_sentence: {input_sentence}
upper_objective: {upper_objective}
company: {company}
team: {team}

각 기준에 대해 다음 정보를 제공하세요
- description: 점수에 대한 구체적인 근거를 분석합니다.
- score: 1-5점 (1: 매우 낮음, 5: 매우 높음)

평가 지침
1. 주어진 회사, 업종, 가이드라인, 팀 정보를 고려하여 맥락에 맞는 평가를 제공하세요.
2. 객관적이고 전문적인 관점에서 평가하되, 확신에 찬 톤으로 의견을 제시하세요.
3. 각 평가 요소를 개별적으로 분석하세요.
4. 산업 특성을 고려하여 평가에 반영하세요.

"""

kr_background_template = """
company: {company}
field: {field}
team: {team}
"""

# krEV 프롬프트들

# 평가요소의 의미 설명
krEV_connectivity_description = """
당신은 OKR(Objectives and Key Results) 평가 전문가입니다. 주어진 Key Result(input_sentence)가 Objective(upper_objective)와 얼마나 연관성이 있는지 평가해야 합니다. 다음 평가 기준에 따라 단계적으로 사고하세요:

1. 점수별 기준 검토
   1점 기준 =
   - Key Result가 Objective 구현과 연결성이 거의 없으며 간접적인 영향이 미미한가요?
   2점 기준 =
   - Key Result가 Objective 구현과 직접적 연결성은 낮지만, 간접적으로 영향을 줄 수 있나요?
   3점 기준 =
   - Key Result가 Objective 구현과 관련성은 있지만, 핵심적이거나 필수적인 요소는 아닌가요?
   4점 기준 =
   - Key Result가 Objective 구현에 중요하지만, 필수적인 핵심 요소까지는 아닌가요?
   5점 기준 =
   - Key Result가 Objective 구현에 필수적이고 핵심적인 요소인가요? 또는 Objective가 구현된 구체적인 결과/모습을 나타내나요?

2. 산업 및 조직 특성 고려
   - 주어진 회사, 업종, 팀 정보를 고려할 때, 이 Key Result의 상위 objective와의 연관성은 어떻게 평가되나요?

3. 종합 평가
   위의 분석을 바탕으로, 1-5점 척도에서 어떤 점수가 가장 적절한가요? 그 이유는 무엇인가요?

위의 단계별 사고 과정을 거친 후, 종합적으로 판단하여 다음 두 가지 결과를 제시하세요:

1. predict_connectivity_description: 평가 기준에 따른 구체적인 평가 (위의 사고 과정을 반영하여 작성)
2. predict_connectivity_score: 최종 평가 점수 (1-5점)

주의사항
- 평가는 객관적이고 전문적이어야 하며, 주어진 회사, 업종, 팀 정보를 고려하여 맥락에 맞는 평가를 제공하세요.
- 확신에 찬 톤으로 답변하되, 합리적|이고 구체적인 근거를 제시하세요.
- 산업과 조직의 특성을 고려하여 평가에 반영하세요.

{prefix_guideline}
{prefix_example}

이제 주어진 input_sentence에 대해 위의 단계를 따라 사고하고, 요청된 형식으로 결과를 제시하세요.
"""

# fewshot
krEV_connectivity_examples = [
  {
  "guideline": "레시피 개발이 고객의 요리에 대한 접근성을 높이는 데 어떻게 기여하는지 설명해주세요. 예를 들어, 어떤 레시피를 개발했고, 어떤 부분에서 고객의 요리 접근성을 향상시켰는지 구체적으로 설명해주세요. 콘텐츠가 고객의 요리에 대한 흥미와 참여를 유발하는 데 어떤 영향을 미치는지 설명해주세요. 예를 들어, 어떤 콘텐츠를 제작했고, 그 콘텐츠가 어떻게 고객의 요리에 대한 흥미와 참여를 이끌어냈는지 구체적으로 설명해주세요. 고객이 하루에 한 끼는 요리를 하고 싶도록 만드는 목표 달성에 어떻게 기여하는지 설명해주세요. 예를 들어, 어떤 방식으로 고객에게 요리의 즐거움을 전달하고, 요리에 대한 동기를 부여하는지 구체적으로 설명해주세요." ,
  "input_sentence" : "일상 요리들의 조리 과정을 50% 줄일 수 있는 제품+요리법을 연구, 개발한다.",
  "upper_objective" : "고객이 하루에 한 끼는 요리를 하고 싶게 한다.",
  "predict_connectivity_description": "조리를 쉽고 빠르게 할 수 있는 것은 고객이 하루에 한끼 정도는 요리를 할 수 있게 만드는 요소입니다.",
  "predict_connectivity_score" : "5",
  }
]

# 예시 형식 지정, input_variables에 해당하는 변수만 바뀔거고 { } 자리에 들어간다는 의미.
krEV_connectivity_example_prompt = PromptTemplate(
  input_variables = ["guideline", "input_sentence", "upper_objective", "predict_connectivity_description", "predict_connectivity_score"],
  template = '''
  <예시>
  "guideline": {guideline}
  "input_sentence": {input_sentence}
  "upper_objective": {upper_objective}
  "predict_connectivity_description": {predict_connectivity_description}
  "predict_connectivity_score": {predict_connectivity_score}
  '''
)

krEV_connectivity_suffix = """
<입력>
"guideline": {guideline_con}
"input_sentence": {input_sentence}
"upper_objective": {upper_objective}
"predict_connectivity_description":
"predict_connectivity_score":
출력 형식은 key가 predict_connectivity_description와 predict_connectivity_score 2개인 json형식입니다. json이라는 문구나 백틱 같은 특수문자는 사용하지 마십시오.
"""

# krEV 프롬프트들

# 평가요소의 의미 설명
krEV_measurability_description = """
당신은 OKR(Objectives and Key Results) 평가 전문가입니다. 주어진 Key Result(input_sentence)가 얼마나 정량적으로 측정 가능한지 평가해야 합니다. 다음 평가 기준에 따라 단계적으로 사고하세요:

1. 점수별 기준 검토
   1점 기준 =
   - Key Result가 측정과 완전히 무관한 내용인가요?
   2점 기준 =
   - Key Result에 측정할 대상은 있지만, 양적으로나 질적으로 달라지는 정도가 없어서 측정이 안 되나요?
   3점 기준 =
   - Key Result를 측정할 대상과 방법이 존재하지만, 그 방법이 간접적이거나 추정에 의존해야 하나요?
   4점 기준 =
   - Key Result의 측정 대상이 달라지는 정도를 정성적인 설명을 통해 측정할 수 있나요?
   5점 기준 =
   - Key Result의 측정 대상이 양적으로 명확하게 달라지는 정도가 나타나나요?

2. 산업 및 조직 특성 고려
   - 주어진 회사, 업종, 팀 정보를 고려할 때, 이 Key Result의 측정 가능성은 어떻게 평가되나요?

3. 종합 평가
   위의 분석을 바탕으로, 1-5점 척도에서 어떤 점수가 가장 적절한가요? 그 이유는 무엇인가요?

위의 단계별 사고 과정을 거친 후, 종합적으로 판단하여 다음 두 가지 결과를 제시하세요:

1. predict_measurability_description: 평가 기준에 따른 구체적인 평가 (위의 사고 과정을 반영하여 작성)
2. predict_measurability_score: 최종 평가 점수 (1-5점)

주의사항
- 평가는 객관적이고 전문적이어야 하며, 주어진 회사, 업종, 팀 정보를 고려하여 맥락에 맞는 평가를 제공하세요.
- 확신에 찬 톤으로 답변하되, 합리적이고 구체적인 근거를 제시하세요.
- 산업과 조직의 특성을 고려하여 평가에 반영하세요.

{prefix_guideline}
{prefix_example}

이제 주어진 input_sentence에 대해 위의 단계를 따라 사고하고, 요청된 형식으로 결과를 제시하세요.
"""

# fewshot
krEV_measurability_examples = [
  {
  "guideline": "고객의 요리 접근성을 어떻게 측정할 수 있을까요? 예를 들어, 레시피 조회수, 레시피 활용 후기 작성 수, 요리 관련 질문 감소율 등을 통해 측정할 수 있습니다. 고객의 요리에 대한 흥미와 참여를 어떻게 측정할 수 있을까요? 예를 들어, 콘텐츠 조회수, 좋아요 수, 댓글 수, 공유 수, 요리 관련 커뮤니티 활동 참여율 등을 통해 측정할 수 있습니다. 고객이 하루에 한 끼는 요리를 하고 싶게 만드는 성공률을 어떻게 측정할 수 있을까요? 예를 들어, 고객 설문조사를 통해 요리 빈도를 조사하거나, 요리 관련 상품 구매 데이터를 분석하여 측정할 수 있습니다. 레시피 개발이라는 활동 자체가 아닌, 그 결과로 나타나는 고객의 요리 접근성 향상에 초점을 맞춰야 합니다. 예를 들어, 레시피 개발을 통해 고객이 요리에 대한 자신감이 향상되었는지, 요리 시간이 단축되었는지, 새로운 요리에 도전하는 비율이 높아졌는지 등을 측정할 수 있습니다. 콘텐츠 제작이라는 활동 자체가 아닌, 그 결과로 나타나는 고객의 요리에 대한 흥미와 참여 증가에 초점을 맞춰야 합니다. 예를 들어, 콘텐츠를 통해 고객이 요리 관련 정보를 얼마나 얻었는지, 새로운 요리 레시피를 얼마나 시도해보았는지, 요리에 대한 만족도가 높아졌는지 등을 측정할 수 있습니다. 고객이 요리에 대한 긍정적인 인식을 갖게 되고, 실제로 요리를 더 자주 하도록 유도하는 결과를 도출하는 데 초점을 맞춰야 합니다. 예를 들어, 고객의 요리 만족도가 높아졌는지, 요리 관련 활동에 대한 참여율이 증가했는지, 요리에 대한 스트레스가 감소했는지 등을 측정할 수 있습니다." ,
  "input_sentence" : "일상 요리들의 조리 과정을 50% 줄일 수 있는 제품+요리법을 연구, 개발한다.",
  "upper_objective" : "고객이 하루에 한 끼는 요리를 하고 싶게 한다.",
  "predict_measurability_description": "현재대비 50% 정도로 요리 과정이 간소화되어야 하는데, 현재가 어느정도인지 나타나지 않아서 50%로 줄어드는 것을 측정하기 어렵다",
  "predict_measurability_score" : "3",
  }
]

# 예시 형식 지정, input_variables에 해당하는 변수만 바뀔거고 { } 자리에 들어간다는 의미.
krEV_measurability_example_prompt = PromptTemplate(
  input_variables = ["guideline", "input_sentence", "upper_objective", "predict_measurability_score", "predict_measurability_description"],
  template = """
  <예시>
  "guideline": {guideline}
  "input_sentence": {input_sentence}
  "upper_objective": {upper_objective}
  "predict_measurability_description": {predict_measurability_description}
  "predict_measurability_score": {predict_measurability_score}

  """
)

krEV_measurability_suffix = """
<입력>
"guideline": {guideline_mea}
"input_sentence": {input_sentence}
"upper_objective": {upper_objective}
"predict_measurability_description":
"predict_measurability_score":

출력 형식은 key가 predict_measurability_description와 predict_measurability_score 2개인 json형식입니다. json이라는 문구나 백틱 같은 특수문자는 사용하지 마십시오.
"""

# krEV 프롬프트들

# 평가요소의 의미 설명
krEV_directivity_description = """
당신은 OKR(Objectives and Key Results) 평가 전문가입니다. 주어진 Key Result(input_sentence)가 얼마나 결과 지향적인지 평가해야 합니다. 다음 평가 기준에 따라 단계적으로 사고하세요:

1. 점수별 기준 검토
   1점 기준 =
   - Key Result가 결과가 아닌 방향이나 행동, 할 일로 표현되어 있나요?
   2점 기준 =
   - Key Result가 결과를 암시하는 부분이 있지만, 여전히 방향성이나 과정에 더 중점을 두고 있나요?
   3점 기준 =
   - Key Result에 결과를 구성하는 '무엇'은 있지만 '얼마나'가 없나요? 또는 행동으로나 결과로 모두 설명이 가능하지만 모호함이 존재하나요?
   4점 기준 =
   - Key Result가 결과 중심적으로 표현되어 있지만, 완벽한 명확성이나 구체성에 약간 부족함이 있나요?
   5점 기준 =
   - Key Result가 방향, 행동이 아닌 결과로 명확하게 표현되어 있나요?

2. 산업 및 조직 특성 고려
   - 주어진 회사, 업종, 팀 정보를 고려할 때, 이 Key Result의 결과 지향성은 어떻게 평가되나요?

3. 종합 평가
   위의 분석을 바탕으로, 1-5점 척도에서 어떤 점수가 가장 적절한가요? 그 이유는 무엇인가요?

위의 단계별 사고 과정을 거친 후, 종합적으로 판단하여 다음 두 가지 결과를 제시하세요:

1. predict_directivity_description: 평가 기준에 따른 구체적인 평가 (위의 사고 과정을 반영하여 작성)
2. predict_directivity_score: 최종 평가 점수 (1-5점)

주의사항
- 평가는 객관적이고 전문적이어야 하며, 주어진 회사, 업종, 팀 정보를 고려하여 맥락에 맞는 평가를 제공하세요.
- 확신에 찬 톤으로 답변하되, 합리적이고 구체적인 근거를 제시하세요.
- 산업과 조직의 특성을 고려하여 평가에 반영하세요.

{prefix_guideline}
{prefix_example}

이제 주어진 input_sentence에 대해 위의 단계를 따라 사고하고, 요청된 형식으로 결과를 제시하세요.
"""

# fewshot
krEV_directivity_examples = [
  {
  "guideline": "레시피 개발이라는 활동 자체가 아닌, 그 결과로 나타나는 고객의 요리 접근성 향상에 초점을 맞춰야 합니다. 예를 들어, 레시피 개발을 통해 고객이 요리에 대한 자신감이 향상되었는지, 요리 시간이 단축되었는지, 새로운 요리에 도전하는 비율이 높아졌는지 등을 측정할 수 있습니다. 콘텐츠 제작이라는 활동 자체가 아닌, 그 결과로 나타나는 고객의 요리에 대한 흥미와 참여 증가에 초점을 맞춰야 합니다. 예를 들어, 콘텐츠를 통해 고객이 요리 관련 정보를 얼마나 얻었는지, 새로운 요리 레시피를 얼마나 시도해보았는지, 요리에 대한 만족도가 높아졌는지 등을 측정할 수 있습니다. 고객이 요리에 대한 긍정적인 인식을 갖게 되고, 실제로 요리를 더 자주 하도록 유도하는 결과를 도출하는 데 초점을 맞춰야 합니다. 예를 들어, 고객의 요리 만족도가 높아졌는지, 요리 관련 활동에 대한 참여율이 증가했는지, 요리에 대한 스트레스가 감소했는지 등을 측정할 수 있습니다." ,
  "input_sentence" : "일상 요리들의 조리 과정을 50% 줄일 수 있는 제품+요리법을 연구, 개발한다.",
  "upper_objective" : "고객이 하루에 한 끼는 요리를 하고 싶게 한다.",
  "predict_directivity_description": "조리과정 50% 감소라는 것은 결과이나, 조리과정이 현재 어느정도에서 얼마나 달라지는지로 표현되어야 더 좋은 결과다",
  "predict_directivity_score" : "4",
  }
]

# 예시 형식 지정, input_variables에 해당하는 변수만 바뀔거고 { } 자리에 들어간다는 의미.
krEV_directivity_example_prompt = PromptTemplate(
  input_variables = ["guideline", "input_sentence", "upper_objective", "predict_directivity_score", "predict_directivity_description"],
  template = """
  <예시>
  "guideline": {guideline}
  "input_sentence": {input_sentence}
  "upper_objective": {upper_objective}
  "predict_directivity_description": {predict_directivity_description}
  "predict_directivity_score": {predict_directivity_score}
  """
)

krEV_directivity_suffix = """
<입력>
"guideline": {guideline_dir}
"input_sentence": {input_sentence}
"upper_objective": {upper_objective}
"predict_directivity_description":
"predict_directivity_score":

출력 형식은 key가 predict_directivity_description와 predict_directivity_score 2개인 json형식입니다. json이라는 문구나 백틱 같은 특수문자는 사용하지 마십시오.
"""

krEV_connectivity_examples_1 = [
  {
  "guideline" : "해당 마케팅 채널 활용 전략이 신규 고객 유치 목표 달성에 어떻게 기여하는가? (예: 특정 채널을 통해 신규 고객 유치율을 높이는 전략) 해당 고객 경험 제공 전략이 신규 고객 유치 및 매출 300% 달성 목표와 어떻게 연결되는가? (예: 고객 경험 향상을 통한 고객 충성도 증가, 재구매율 증가 등) 해당 프로모션 전략이 신규 고객 유치 목표와 어떻게 연결되는가? (예: 프로모션을 통해 신규 고객 유치율을 높이는 전략)",
  "input_sentence" : "APP 다운로드 5만 달성 (500% 성장)",
  "upper_objective" : "신규 고객 유치 (매출 300% 달성 목표)",
  "predict_connectivity_description": "신규 고객 확대를 통해, 매장 이용 소비자까지 app다운로드와가 늘어남",
  "predict_connectivity_score" : "4.5",
  },
  {
  "guideline" : "서비스 품질 및 사용성 만족도를 향상시키는 것은 서비스 품질 및 사용성 제고라는 목표 달성에 직접적으로 기여합니다. 사용자 만족도 향상은 서비스 품질 및 사용성 개선의 핵심 지표가 됩니다. 사용자 만족도를 측정하는 것은 목표 달성 여부를 파악하는데 도움이 됩니다. 서비스 이용 관련 지표 개선은 서비스 품질 및 사용성 제고 목표 달성에 직접적으로 기여합니다. 서비스 이용률 증가는 서비스 활용도를 높이는 결과를 가져오며, 이는 곧 서비스 품질 및 사용성이 개선되었음을 의미합니다. 서비스 안정성 및 신뢰성 강화는 서비스 품질 및 사용성 제고 목표 달성에 직접적으로 기여합니다. 서비스 안정성이 향상되면 사용자 경험이 개선되고, 서비스에 대한 신뢰도가 높아지게 됩니다.",
  "input_sentence" : "내부 시스템 및 인프라 재정비(DB 안정화, APP 경량화, 서비스 확장성을 위한 Back Office 정비)",
  "upper_objective" : "서비스 품질 및 사용성 제고(서비스 편의성, 직관성, 안정성 개선)",
  "predict_connectivity_description": "DB 안정화, APP 경량화, 백오피스 구축하면, 어떤 품질/사용성과 연관 되는지 불명확",
  "predict_connectivity_score" : "3",
  }
]

krEV_connectivity_examples_2 = [
  {
  "guideline" : "해당 질문은 'PC방 Lvup.gg 샘플 데이터 확보'라는 목표와 직접적인 연결성을 가지고 있으며, 데이터 확보라는 목표 달성에 필수적인 요소를 묻고 있습니다. (예: 목표 달성을 위한 데이터 확보 목표 수량) 다양한 유형의 데이터 확보는 사용자에게 다양한 정보를 제공하여 플랫폼 활용도를 높이는 데 기여합니다. (예: 사용자들이 필요로 하는 다양한 샘플 데이터 유형을 확보하는 것이 목표 달성에 중요한 요소) 신뢰도 높은 데이터는 플랫폼의 정확성과 신뢰성을 높이는 데 중요한 역할을 합니다. (예: 신뢰도 높은 데이터 확보는 플랫폼의 경쟁력을 강화하고 목표 달성에 중요한 영향을 미칩니다.)",
  "input_sentence" : "PC방 대회 통해 Lvup.gg 접속률, 가입률 데이터 확보 (*1개 PC방에서 얼만큼의 접속률/가입률을 기대 할 수 있을지 세컨드찬스 의견 필요)",
  "upper_objective" : "PC방 Lvup.gg 샘플 데이터 확보",
  "predict_connectivity_description": "상위목표와 같은 이야기입니다. 연결은 잘되었다고 볼 수 있으나, 세부목표로서의 초점이 명확하지 않습니다",
  "predict_connectivity_score" : "3",
  }
]

krEV_connectivity_examples_3 = [
  {
  "guideline" : "어떤 핵심 기술 및 서비스 개발이 에듀테크 사업 진출과 시장 경쟁력 확보에 가장 중요한 역할을 할 수 있을까요? (예: 인공지능 기반 맞춤형 학습 시스템, VR/AR 기반 교육 콘텐츠 개발, 온라인 학습 플랫폼 구축) 어떤 차별화된 교육 콘텐츠 및 서비스 제공이 고객 만족도 향상과 시장 점유율 확보에 가장 큰 영향을 미칠 수 있을까요? (예: 개인 맞춤형 학습 콘텐츠 제공, 몰입형 학습 경험 제공, 편리한 학습 환경 구축) 에듀테크 사업 성공을 위해 어떤 분야의 전문 인력 확보가 가장 중요하다고 생각되나요? (예: 교육 콘텐츠 개발, 플랫폼 개발, 데이터 분석, 마케팅)",
  "input_sentence" : "에듀테크 기업과 파트너십을 1건 이상 구축한다.",
  "upper_objective" : "에듀테크 기업으로 변모한다.",
  "predict_connectivity_description": "외부 에듀테크 기업과 파트너십 1건 구축 *자체적인 역량 구축없이 외부 기업과의 파트너십은 좋은 전략이 아님",
  "predict_connectivity_score" : "3",
  }
]

krEV_measurability_examples_1 = [
  {
  "guideline" : "참여자 고충 유형별 발생 건수 및 해결 비율을 어떻게 정량적으로 측정할 수 있을까요? (예: 고객센터 문의, 설문조사, 커뮤니티 게시글 등을 통해 고충 유형별 발생 건수를 파악하고, 해결된 건수를 기준으로 해결 비율을 계산할 수 있습니다.) 참여자 고충 해결 프로세스 개선 효과를 어떻게 정량적으로 측정할 수 있을까요? (예: 고충 접수부터 해결까지 걸리는 시간, 해결률, 고객 만족도 조사 결과 등을 통해 측정할 수 있습니다.) 참여자 고충 해결 시스템 및 도구 구축 효과를 어떻게 정량적으로 측정할 수 있을까요? (예: 시스템 및 도구 이용률, 고충 접수 및 해결 건수, 사용자 만족도 조사 결과 등을 통해 측정할 수 있습니다.)",
  "input_sentence" : "대기일수 줄이기",
  "upper_objective" : "참여자의 고충을 도출하고 해결한다.",
  "predict_measurability_description": "대기일수(대상)를 얼마나 줄일 것인지가 있어야 측정할 수 있음",
  "predict_measurability_score" : "2",
  }
]

krEV_measurability_examples_2 = [
  {
  "guideline" : "어린이 시청자 도달 범위를 측정할 수 있는 지표는 무엇이며, 어떻게 측정할 수 있을까요? (예: 동영상 조회수, 구독자 수, 시청 시간, 콘텐츠 공유 수 등을 통해 측정할 수 있습니다.) 어린이 시청자들에게 미친 긍정적인 영향을 어떻게 측정할 수 있을까요? (예: 시청 후 학습 관련 설문 조사, 학습 성취도 평가, 시청 후 콘텐츠 만족도 조사 등을 통해 측정할 수 있습니다.) 어린이 독자층의 참여를 어떻게 측정할 수 있을까요? (예: 동영상 댓글, 좋아요, 공유 수, 시청자와의 소통 활동, 콘텐츠 관련 이벤트 참여율 등을 통해 측정할 수 있습니다.)!",
  "input_sentence" : "유튜브 서비스 1개월 후 구독자 수 10,000명을 달성한다",
  "upper_objective" : "동영상 콘텐츠 출시로 어린이 독자를 기쁘게 한다",
  "predict_measurability_description": "측정 대상(구독자수)과 측정 기준(명수)/수준(10,000명)이 명확하여 측정기능함",
  "predict_measurability_score" : "5",
  } ,
  {
  "guideline" : "제품의 영양소 함량을 어떻게 측정하고, '한 끼에 필요한 영양소 기준'은 어떻게 정의하는가? (예: 한국인 영양섭취기준) 소비자 인식은 어떻게 측정 가능한가? (예: 설문조사, 제품 리뷰 분석, 소셜 미디어 분석) 다양한 영양 요구 사항을 어떻게 정의하고, 제품의 적합성은 어떻게 측정하는가? (예: 제품 라인업 구성, 타겟 소비자 그룹 분석)",
  "input_sentence" : "저칼로리 건강죽을 개발하여 간편하고 포만감 있게 먹으면서도 다이어트가 될 수 있는 대용식을 제공한다.",
  "upper_objective" : "한끼에 필요한 영양소를 제공한다",
  "predict_measurability_description": "저칼로리 건강죽이라는 측정의 대상은 있으나, 어떤 함량, 어느정도의 칼로리, 다이어트 효과, 대용식제품의 개발 기한 등 측정할 기준이 없다",
  "predict_measurability_score" : "2",
  }
]

krEV_measurability_examples_3 = [
  {
  "guideline" : "고객 만족도는 설문조사, NPS 점수, 고객 리뷰 등을 통해 측정할 수 있습니다. 측정 대상은 토스 송금 서비스 이용 고객이며, 측정 기준은 '매우 만족', '만족', '보통', '불만족', '매우 불만족' 등의 5점 척도를 사용합니다. 예시: '2023년 말 토스 송금 서비스 이용 고객 NPS 점수가 70점 이상 달성한다. 월간 활성 사용자 수는 토스 앱 내 송금 기능 이용 기록을 기반으로 측정할 수 있습니다. 측정 대상은 토스 송금 서비스를 이용하여 송금을 한 사용자이며, 측정 기준은 월별 사용자 수를 기준으로 합니다. 예시: '2023년 말 토스 송금 서비스의 월간 활성 사용자 수가 500만 명 이상 달성한다. 평균 송금 시간은 토스 송금 서비스 이용 기록을 기반으로 측정할 수 있습니다. 측정 대상은 토스 송금 서비스 이용 고객이며, 측정 기준은 송금 시작부터 완료까지 걸리는 시간을 기준으로 합니다. 예시: '2023년 말 토스 송금 서비스의 평균 송금 시간이 5초 이내 달성한다.",
  "input_sentence" : "계좌 개설과 송금을 위해 필수로 알려진 오프라인 은행 지점 방문을 필요없게 만든다",
  "upper_objective" : "현존 하는 어떤 인터넷 뱅킹보다 더 쉽고 간편한 송금할 수 있는 온라인 송금 프로덕트를 고객에게 선보이자",
  "predict_measurability_description": "오프라인 은행지점방문이 필요없어졌다는 것을 구현하게 되었는지 여부를 측정가능하다",
  "predict_measurability_score" : "5",
  },
  {
  "guideline" : "신규 유저 유입률은 어떻게 측정할 수 있을까요? 예를 들어, 캠페인 전후 각 서비스의 신규 유저 수를 비교하여 증가율을 계산할 수 있습니다. 사용자 만족도는 어떻게 측정할 수 있을까요? 예를 들어, 서비스 이용 후 설문조사를 통해 만족도를 평가하거나, 서비스 이용 빈도 및 지속 시간 등을 분석하여 만족도를 추정할 수 있습니다. 매출 증진은 어떻게 측정할 수 있을까요? 예를 들어, 캠페인 전후 각 서비스의 매출 변화를 비교하여 증가율을 계산할 수 있습니다.",
  "input_sentence" : "쇼핑몰 매출 확대를 위한 마케팅 서비스 도입 (공비서스토어 쇼핑 DM, 재구매 유도 추천 상품).",
  "upper_objective" : "서비스 연계 마케팅 강화 (공비서, 공비서 스토어, 네일아트앱)",
  "predict_measurability_description": "도입 여부는 측정할 수 있으나, 서비스를 얼마나 잘 도입했는지의 수준을 측정할 수 없음",
  "predict_measurability_score" : "2",
  }
]

krEV_directivity_examples_1 = [
  {
  "guideline" : "고객 만족도는 토스 송금 서비스의 결과를 나타냅니다. 고객 만족도가 높아진다는 것은 토스 송금 서비스가 고객의 요구를 충족하고 있다는 것을 의미합니다. 예시: '토스 송금 서비스 이용 후, '다시 이용하고 싶다'는 응답 비율이 90% 이상 달성한다. 월간 활성 사용자 수는 토스 송금 서비스의 결과를 나타냅니다. 월간 활성 사용자 수가 증가한다는 것은 토스 송금 서비스가 고객에게 인정받고 있다는 것을 의미합니다. 예시: '2023년 말 토스 송금 서비스를 이용한 사용자 중, 월 2회 이상 송금을 한 사용자 비율이 50% 이상 달성한다. 평균 송금 시간 단축은 토스 송금 서비스의 결과를 나타냅니다. 평균 송금 시간이 단축될수록 고객의 편의성이 증가하고 토스 송금 서비스의 경쟁력이 강화됩니다. 예시: '2023년 말 토스 송금 서비스 이용 고객 중, 송금 시간에 대한 만족도가 90% 이상 달성한다.",
  "input_sentence" : "공인인증서_OTP/보안카드 등이 없어도 송금할 수 있게 된다",
  "upper_objective" : "현존 하는 어떤 인터넷 뱅킹보다 더 쉽고 간편한 송금할 수 있는 온라인 송금 프로덕트를 고객에게 선보이자",
  "predict_directivity_description": "은행지점 방문이 필요없게 된 것은 확실한 변화이자 결과다. 단, 프로덕트 차원에서 해당변화를 구현할 기능이나 프로세스가 무엇이라는 것이 있으면 더 좋은 결과다",
  "predict_directivity_score" : "4",
  }
]

krEV_directivity_examples_2 = [
  {
  "guideline" : "이 질문은 고객의 소비하지 않는 이유를 파악하는 결과를 도출하는 데 초점을 맞추며, 이는 활동이나 작업이 아닌 결과입니다. (예: 고객 불만 사항 분석 보고서, 경쟁사 제품 분석 결과 보고서 등) 이 질문은 상품 기획, 디자인, 마케팅 전략의 개선을 통한 결과를 중심으로 질문합니다. (예: 개선된 상품 출시 후 매출 변화, 마케팅 캠페인 결과 보고서 등) 이 질문은 고객 소비 유도 전략의 성공 가능성을 평가하는 결과 중심 질문입니다. (예: 마케팅 캠페인 효과 분석 보고서, 고객 만족도 조사 결과 등)",
  "input_sentence" : "브랜드 검색량 월 1,700건에서 3,500건으로 증대",
  "upper_objective" : "고객이 우리 옷을 소비하지 않는 부분에 대한 문제 해결",
  "predict_directivity_description": "결과를 구성하는 무엇이 얼마나 달라지는가가 잘 표현되어 있다",
  "predict_directivity_score" : "5",
  },
  {
  "guideline" : "고객 만족도는 토스 송금 서비스의 결과를 나타냅니다. 고객 만족도가 높아진다는 것은 토스 송금 서비스가 고객의 요구를 충족하고 있다는 것을 의미합니다. 예시: '토스 송금 서비스 이용 후, '다시 이용하고 싶다'는 응답 비율이 90% 이상 달성한다. 월간 활성 사용자 수는 토스 송금 서비스의 결과를 나타냅니다. 월간 활성 사용자 수가 증가한다는 것은 토스 송금 서비스가 고객에게 인정받고 있다는 것을 의미합니다. 예시: '2023년 말 토스 송금 서비스를 이용한 사용자 중, 월 2회 이상 송금을 한 사용자 비율이 50% 이상 달성한다. 평균 송금 시간 단축은 토스 송금 서비스의 결과를 나타냅니다. 평균 송금 시간이 단축될수록 고객의 편의성이 증가하고 토스 송금 서비스의 경쟁력이 강화됩니다. 예시: '2023년 말 토스 송금 서비스 이용 고객 중, 송금 시간에 대한 만족도가 90% 이상 달성한다.",
  "input_sentence" : "계좌 개설과 송금을 위해 필수로 알려진 오프라인 은행 지점 방문을 필요없게 만든다",
  "upper_objective" : "현존 하는 어떤 인터넷 뱅킹보다 더 쉽고 간편한 송금할 수 있는 온라인 송금 프로덕트를 고객에게 선보이자",
  "predict_directivity_description": "은행지점 방문이 필요없게 된 것은 확실한 변화이자 결과입니다. 단, 프로덕트 차원에서 해당변화를 구현할 기능이나 프로세스가 무엇이고 언제까지 구현한다는 것이 있으면 더 좋은 결과입니다",
  "predict_directivity_score" : "4",
  }
]

krEV_directivity_examples_3 = [
  {
  "guideline" : "핵심 기술 및 서비스 개발 및 구축을 통해 어떤 결과를 도출하고자 하는지 명확하게 나타낼 수 있을까요? (예: 새로운 에듀테크 서비스 출시, 기존 교육 사업 성장 촉진, 새로운 수익 창출 모델 확보) 차별화된 교육 콘텐츠 및 서비스 제공을 통해 어떤 결과를 도출하고자 하는지 명확하게 나타낼 수 있을까요? (예: 고객 충성도 향상, 브랜드 인지도 증진, 새로운 시장 진출 기회 확보) 전문 인력 확보 및 육성을 통해 어떤 결과를 도출하고자 하는지 명확하게 나타낼 수 있을까요? (예: 에듀테크 사업 경쟁력 강화, 혁신적인 교육 서비스 개발, 지속 가능한 성장 기반 확보)",
  "input_sentence" : "에듀테크 R&D 조직을 구성하고 에듀테크 성장 로드맵을 완성한다. (4월 말까지)",
  "upper_objective" : "에듀테크 기업으로 변모한다.",
  "predict_directivity_description": "조로드맵 완성은 목표를 수립하기 위한 계획서라는 차원에서는 결과라고 보기 어려우나, 에듀테크로 변하는 전략차원에서 첫 결과물로 의미를 가질 수 있습니다",
  "predict_directivity_score" : "3",
  }
]