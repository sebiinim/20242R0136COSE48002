from langchain.prompts import PromptTemplate

objEV_task_description = """
당신은 세계적으로 인정받는 OKR(Objectives and Key Results) 전문 컨설턴트입니다. 당신의 임무는 주어진 Objective를 철저히 분석하고 평가하여, 조직의 목표 달성을 위한 최적의 OKR 수립을 돕는 것입니다.

평가 대상
input_sentence: {input_sentence}
upper_objective: {upper_objective}
company: {company}
field: {field}
team: {team}

각 기준에 대해 다음 정보를 제공하세요.
- description: 점수에 대한 구체적인 근거를 설명합니다.
- score: 1-5점 (1: 매우 낮음, 5: 매우 높음)

평가 지침.
1. 주어진 회사, 업종, 가이드라인, 팀 정보를 고려하여 맥락에 맞는 평가를 제공하세요.
2. 객관적이고 전문적인 관점에서 평가하되, 확신에 찬 톤으로 의견을 제시하세요.
3. 각 평가 요소를 개별적으로 분석하세요.
4. 산업 특성을 고려하여 평가에 반영하세요.
"""

obj_background_template = """
company: {company}
field: {field}
team: {team}
"""


# 예시 형식 지정, input_variables에 해당하는 변수만 바뀔거고 { } 자리에 들어간다는 의미.
objEV_example_prompt = PromptTemplate(
    input_variables=[
        "guideline",
        "input_sentence",
        "upper_objective",
        "description",
        "score",
    ],
    template="""
    <예시 입력>
    "guideline": {guideline}
    "input_sentence": {input_sentence}
    "upper_objective": {upper_objective}
    
    <예시 출력>
    "description": {description}
    "score": {score}
  """,
)

objEV_suffix = """
<입력>
"guideline": {guideline}
"input_sentence": {input_sentence}
"upper_objective": {upper_objective}
"description":
"score":

출력 형식은 key가 description와 score 2개인 json형식입니다. json이라는 문구나 백틱 같은 특수문자는 사용하지 마십시오.
"""

# 평가요소의 의미 설명
objEV_align_description = """
당신은 OKR(Objectives and Key Results) 평가 전문가입니다. 주어진 Objective(input_sentence)가 Upper_Objective와 얼마나 align되어 있는지 평가해야 합니다. 다음 평가 기준에 따라 단계적으로 사고하세요.

1. 점수별 기준 검토
   1점 기준 =
   - Objective가 Upper_Objective와 완전히 무관한가요?
   2점 기준 =
   - Objective가 Upper Objective의 Align이 아예 무관하다고 보기 어렵지만, Align의 정도를 판단하기 위해서 여러 가정들을 거쳐야 하나요?
   3점 기준 =
   - Objective가 Upper Objective와 전략적으로는 연결되어 있지만, 초점이 다소 불분명한가요?
   4점 기준 =
   - Objective가 Upper Objective와 명확한 연관성이 있으나, 일부 개선이 필요한가요?
   5점 기준 =
   - Objective가 Upper Objective와의 전체 혹은 일부와 전략적 연결이 매우 뚜렷한가요? 또는 최상위 조직의 경우, 미션/비전/전략 방향이 균형있게 반영되어있나요?

2. 산업 및 조직 특성 고려
   - 주어진 회사, 업종, 팀 정보를 고려할 때, 이 objective의 Upper objective와의 연관성은 어떻게 평가되나요?

3. 종합 평가
   위의 분석을 바탕으로, 1-5점 척도에서 어떤 점수가 가장 적절한가요? 그 이유는 무엇인가요?

위의 단계별 사고 과정을 거친 후, 종합적으로 평가하여 다음 두 가지 결과를 제시하세요.

1. description: 평가 기준에 따른 구체적인 평가 (위의 사고 과정을 반영하여 작성)
2. score: 최종 평가 점수 (1-5점)

주의사항.
- 평가는 객관적이고 전문적이어야 하며, 주어진 회사, 업종, 팀 정보를 고려하여 맥락에 맞는 평가를 제공하세요.
- 확신에 찬 톤으로 답변하되, 합리적이고 구체적인 근거를 제시하세요.
- 산업과 조직의 특성을 고려하여 평가에 반영하세요.

{prefix_guideline}
{prefix_example}

이제 주어진 input_sentence에 대해 위의 단계를 따라 사고하고, 요청된 형식으로 결과를 제시하세요.
"""

# fewshot
objEV_align_examples = [
    {
        "guideline": "해당 고객층 확보는 어떻게 공비서 프로그램의 초기 전략인 '모든 매출은 고객에게서 나온다'에 기여할까요? (예: 고객층을 네일샵 초보 창업자로 설정하면, 이들은 공비서 프로그램을 통해 매장 운영 노하우를 배우고 비즈니스 성장을 도모하며 매출 증대를 이끌어 낼 수 있습니다.), 해당 마케팅 전략은 어떻게 공비서 프로그램의 초기 전략인 '고객 확대'에 기여하며, 고객 만족으로 이어질 수 있을까요? (예: 네일샵 관련 커뮤니티 및 SNS 채널을 활용한 마케팅 전략은 타겟 고객에게 효과적으로 공비서 프로그램을 알릴 수 있으며, 프로그램 사용 후기를 공유하여 신뢰도를 높이고 고객 만족으로 이어질 수 있습니다.), 차별화된 기능 또는 서비스는 어떻게 고객 확대 목표에 기여하고, 공비서 프로그램의 경쟁력을 강화할 수 있을까요? (예: 고객 관리 시스템과 연동된 마케팅 자동화 기능은 원장님들의 마케팅 효율성을 높여주고, 고객 만족도를 향상시켜 고객 유지율을 높이고 새로운 고객 확보에도 기여할 수 있습니다.)",
        "input_sentence": "신규 고객 유치 (매출 300% 달성 목표)",
        "upper_objective": "공비서 초기 전략은 모든 매출은 고객에게서 나온다 임. 그래서, 고객만족을 위한 사용성 개선과 더불어 고객의 확장 전략에 집중. 이 OKR은 고객 확대에 집중하는 것임",
        "description": "고객확대 전략에 얼라인한 신규고객유치에 집중하는 것을 최우선순위로 잡는다",
        "score": "4.5",
    }
]

# 평가요소의 의미 설명
objEV_value_description = """
당신은 OKR(Objectives and Key Results) 평가 전문가입니다. 주어진 Objective(input_sentence)가 얼마나 고객에게 제공하는 가치를 언급하고 있는지 평가해야 합니다. 다음 평가 기준에 따라 단계적으로 사고하세요.

1. 점수별 기준 검토
   1점 기준 =
   - Objective가 고객 가치와 완전히 무관한가요?
   2점 기준 =
   - Objective에 고객에 관한 문제나 상황은 있지만, 제공하고자 하는 가치가 나타나지 않나요?
   3점 기준 =
   - Objective에서 고객에게 제공하고자 하는 가치는 분명하지만, 전략적으로 고객의 필요와의 일치 여부가 다소 모호한가요?
   4점 기준 =
   - Objective에서 고객에게 제공하고자 하는 가치가 현재 고객의 필요와 대체로 일치하지만, 일부 측면에서 명확성이나 구체성이 부족한가요?
   5점 기준 =
   - Objective의 고객에게 제공하고자 하는 가치 혹은 고객이 겪는 문제에 대한 해결이 현재 고객에게 필요한 것과 일치하고, 이를 명확하게 표현하고 있나요?
2. 산업 및 조직 특성 고려
   - 주어진 회사, 업종, 팀 정보를 고려할 때, 이 objective의 고객 가치 지향성은 어떻게 평가되나요?
3. 종합 평가
   위의 분석을 바탕으로, 1-5점 척도에서 어떤 점수가 가장 적절한가요? 그 이유는 무엇인가요?

위의 단계별 사고 과정을 거친 후, 종합적으로 평가하여 다음 두 가지 결과를 제시하세요.

1. description: 평가 기준에 따른 구체적인 평가 (위의 사고 과정을 반영하여 작성)
2. score: 최종 평가 점수 (1-5점)

주의사항.
- 평가는 객관적이고 전문적이어야 하며, 주어진 회사, 업종, 팀 정보를 고려하여 맥락에 맞는 평가를 제공하세요.
- 확신에 찬 톤으로 답변하되, 합리적이고 구체적인 근거를 제시하세요.
- 산업과 조직의 특성을 고려하여 평가에 반영하세요.

{prefix_guideline}
{prefix_example}

이제 주어진 input_sentence에 대해 위의 단계를 따라 사고하고, 요청된 형식으로 결과를 제시하세요.
"""

# fewshot
objEV_value_examples = [
    {
        "guideline": "이 기능적인 개선은 원장님과 손님의 어떤 불편함을 해결하여 어떤 가치를 제공할 수 있을까요? (예: 예약 시스템 개선은 원장님들의 예약 관리 부담을 줄이고, 손님들은 원하는 시간에 쉽게 예약을 할 수 있어 편리성을 높일 수 있습니다.), 이 기술적인 개선은 원장님과 손님의 어떤 불안감을 해소하여 어떤 가치를 제공할 수 있을까요? (예: 데이터 백업 시스템 구축은 프로그램 오류 발생 시 데이터 손실에 대한 원장님들의 불안감을 해소하고, 손님들의 정보 유출에 대한 우려를 줄여 안전한 서비스 이용 환경을 제공합니다.), 이 새로운 기능은 원장님과 손님에게 어떤 새로운 가치를 제공할 수 있을까요? (예: 고객 관리 기능 추가는 원장님들이 고객과의 소통을 강화하고, 손님들에게 맞춤형 서비스를 제공할 수 있도록 지원하여 만족도를 높일 수 있습니다.)",
        "input_sentence": "서비스 품질 및 사용성 제고 (서비스 편의성, 직관성, 안정성 개선)",
        "upper_objective": "공비서는 뷰티서비스를 제공하는 원장님과 샵을 이용하는 손님의 불편을 IT 기술로 해결하여, 원장님들의 비즈니스 성장을 촉진한다. 이를 위해서 IT기술을 발전시켜 서비스 사용성을 높여간다.",
        "description": "고객에게 제공하고자 하는 가치인 편의성/직관성/안정성은 분명하지만, 구체적인 고객 니즈가 모호하다",
        "score": "3",
    }
]

objEV_align_examples_1 = [
    {
        "guideline": "이 질문을 통해 도출된 타겟 고객과 그들의 니즈는 어떻게 '고객 확대 전략'에 연결될까요? (예: 타겟 고객을 20~30대 여성 원장님으로 설정하고, 이들의 주요 니즈가 예약 관리 자동화와 마케팅 지원이라는 결과를 도출했다면, 이를 기반으로 예약 시스템 개선과 마케팅 기능 추가를 통해 공비서 프로그램의 매력도를 높여 고객 확대를 목표로 설정할 수 있습니다.), 이 차별화된 가치는 어떻게 공비서 프로그램의 '고객 확대' 목표 달성에 기여할까요? (예: 경쟁 서비스와 달리 고객 맞춤형 마케팅 기능을 제공하여 고객 확보 및 유지에 효과를 높일 수 있다는 차별점을 발견했다면, 이를 기반으로 마케팅 기능 강화를 통해 고객 확대를 목표로 설정할 수 있습니다.), 이 홍보 전략은 어떻게 '고객 확대' 목표 달성에 기여할까요? (예: 네일샵 관련 온라인 커뮤니티에 공비서 프로그램 광고를 게재하여 타겟 고객에게 효과적으로 홍보하는 전략을 수립했다면, 이를 통해 신규 고객 유입을 증가시켜 고객 확대 목표를 달성할 수 있습니다.)",
        "input_sentence": "신규 고객 유치 (매출 300% 달성 목표)",
        "upper_objective": "(최상위) 공비서 초기 전략은 모든 매출은 고객에게서 나온다 임. 그래서, 고객만족을 위한 사용성개선과 더불어 고객의 확대 전략에 집중. 이 OKR은 고객확대에 집중하는 것임",
        "description": "고객확대 전략에 얼라인한 신규고객유치에 집중하는 것을 최우선순위로 잡는다",
        "score": "4.5",
    },
    {
        "guideline": "이 연계 마케팅 전략은 어떻게 원장님들의 비즈니스 성장을 가속화하는 IT 기술 고도화 목표와 연결될 수 있을까요? (예: 앱에서 스토어 상품 추천을 통해 원장님들의 제품 판매를 증진시키고, 이는 원장님들의 수익 증대에 기여할 수 있습니다.), 이 사용자 경험 개선 전략은 어떻게 IT 기술 고도화를 통해 서비스 사용성을 높이는 목표와 부합할 수 있을까요? (예: 사용자 인터페이스 개선은 앱 이용 편의성을 증대시켜 고객 만족도를 높이고, 더 많은 고객이 앱을 지속적으로 사용하도록 유도하여 서비스 사용성을 높일 수 있습니다.), 이 상품 경쟁력 강화 전략은 어떻게 IT 기술 고도화를 통해 서비스 사용성을 높이는 목표와 연관될 수 있을까요? (예: 상품 데이터 분석을 통한 트렌드 상품 발굴은 고객의 선호도를 파악하여 맞춤형 상품을 제공하고, 원장님들의 제품 선택을 돕는 IT 기술을 활용하여 서비스 사용성을 향상시킬 수 있습니다.)",
        "input_sentence": "서비스 연계 마케팅 강화 (공비서, 공비서 스토어, 네일아트앱)",
        "upper_objective": "(최상위) 공비서는 뷰티서비스를 제공하는 원장님과 샵을 이용하는 손님의 불편을 IT 기술로 해결하여, 원장님들의 비스니스 성장을 가속화한다. 이를 위해서 IT기술을 고도화하여 서비스 사용성을 높여간다.",
        "description": "비즈니스 성장 가속화라는 점과 연관성은 있지만, 비즈니스 성장과 마케팅 강화사이의 연결성을 설명할 초점이 모호하다",
        "score": "4",
    },
]

objEV_align_examples_2 = [
    {
        "guideline": "스마트 러닝 사업의 핵심 경쟁력은 어떻게 국내 온라인 교육시장을 선도하고, 업계 선두를 유지하는 목표 달성에 기여할 수 있을까요? (예: AI 기반 개인 맞춤형 학습 시스템은 학습 효과를 극대화하여 고객 만족도를 높이고, 경쟁사와 차별화된 강점을 제공하여 시장 지배력을 확보할 수 있습니다.), 온라인 교육 서비스의 개선 방향은 어떻게 빠르게 변화하는 고객 학습 방식에 대응하고, 온 오프라인을 아우르는 블렌디드 러닝 서비스를 넘어 스마트 러닝 사업으로 나아가는 목표 달성에 기여할 수 있을까요? (예: 모바일 친화적인 학습 환경 구축은 고객의 시간과 장소 제약 없이 편리한 학습을 가능하게 하고, 꾸준한 학습 참여를 유도하여 스마트 러닝 사업 성공에 기여할 수 있습니다.), 블렌디드 러닝 서비스는 어떻게 온라인 교육 서비스를 발전시키고, 스마트 러닝 사업으로의 전환을 위한 발판 역할을 할 수 있을까요? (예: 오프라인 강의와 온라인 학습 콘텐츠를 연계하여 학습 효과를 극대화하고, 고객의 학습 참여도를 높여 스마트 러닝 사업으로의 자연스러운 전환을 유도할 수 있습니다.)",
        "input_sentence": "에듀테크 기업으로 변모한다.",
        "upper_objective": "(최상위) 국내 온라인 교육시장을 이끌며 사업시작 일 년 만에 업계 선두로 올라서고 유지해 왔다. 코로나 이후 빠르게 변하고 있는 고객 학습방식과 시장 변화에 따라, 온라인 교육 서비스로 발전시키고, 온 오프라인을 아우르는 블렌디드 러닝 서비스를 넘어 스마트 러닝 사업에 힘을 쏟고 있다.",
        "description": "코로나 이후 달라진 환경에 적응하기 위한 전략과 연관되어 있다",
        "score": "4",
    }
]

objEV_align_examples_3 = [
    {
        "guideline": "새로운 기획 개발은 어떻게 시장의 기회를 살리고 다양한 콘텐츠 소비 확장에 기여할까요? (예:  온라인 콘텐츠 소비 증가를 반영하여,  웹툰, 웹소설 등 디지털 콘텐츠 기획 개발을 통해 시장 경쟁력을 확보할 수 있습니다.), 독자 충성도 증진은 어떻게 다양한 콘텐츠 소비 확장과 시장 기회 포착에 기여할까요? (예:  독자 커뮤니티 운영을 통해 콘텐츠 관련 정보 공유와 소통 기회 제공,  독자 맞춤형 콘텐츠 추천 서비스를 제공하여 독자 만족도를 높일 수 있습니다.), 제휴 및 협업은 어떻게 시장의 기회를 포착하고 다양한 콘텐츠 소비 확장에 기여할까요? (예:  웹툰 플랫폼,  온라인 서점 등 다른 플랫폼과의 제휴를 통해 홍보 및 판매 채널 확대,  콘텐츠 제작 및 유통 분야의 전문 기업과 협력하여 시너지 효과 창출 가능합니다.)",
        "input_sentence": "2021년 시장 전망을 토대로, 팀별 타깃 독자에게 꼭 필요한 기획을 충분히 확보한다.",
        "upper_objective": "(최상위)코비드로 사람들의 라이프스타일이 달라지고 있고, 다양한 콘텐츠 소비가 확장되고 있는 상황에서 시장의 기회를 살릴 수 있는 다양한 기획 확보가 매우 중요함",
        "description": "코비드로 인한 고객의 라이프스타일 변화가 창출하는 기회와 얼라인되는 내용이 없다",
        "score": "2",
    }
]

objEV_value_examples_1 = [
    {
        "guideline": "이 질문을 통해 파악된 고객 니즈는 어떻게 '고객 만족'으로 이어질 수 있을까요? (예: 20~30대 여성 원장님들의 주요 니즈가 예약 관리 자동화라는 결과를 도출했다면, 자동 예약 시스템을 통해 원장님들이 시간 관리를 효율적으로 할 수 있도록 돕고, 여가 시간을 확보할 수 있도록 지원하여 고객 만족도를 높일 수 있습니다.), 이 차별화된 가치는 어떤 고객 문제를 해결하여 '고객 만족'으로 이어질 수 있을까요? (예: 경쟁 서비스와 달리 고객 데이터 분석 기능을 제공하여 개인 맞춤형 마케팅 전략 수립을 지원한다는 차별점을 발견했다면, 이는 원장님들의 마케팅 효율성을 높여 매출 증진에 기여하고, 고객 만족도를 높일 수 있습니다.), 이 홍보 전략은 어떻게 '고객 만족'에 기여할까요? (예: 네일샵 관련 박람회에 참여하여 공비서 프로그램을 직접 시연하고, 원장님들의 궁금증을 해소하는 홍보 전략을 수립했다면, 이를 통해 프로그램에 대한 이해도를 높이고, 만족도를 향상시켜 고객 만족으로 이어질 수 있습니다.)",
        "input_sentence": "신규 고객 유치 (매출 300% 달성 목표)",
        "upper_objective": "(최상위) 공비서 초기 전략은 모든 매출은 고객에게서 나온다 임. 그래서, 고객만족을 위한 사용성개선과 더불어 고객의 확대 전략에 집중. 이 OKR은 고객확대에 집중하는 것임",
        "description": "고객 제공 가치는 없다",
        "score": "1",
    },
    {
        "guideline": "이 연계 마케팅 전략은 고객들에게 어떤 가치를 제공하고, 어떤 불편함을 해소할 수 있을까요? (예: 앱에서 손쉽게 필요한 네일 용품을 구매할 수 있도록 연결하여 고객의 편의성을 높이고, 원장님의 추천 상품을 통해 고객의 선택 폭을 넓힐 수 있습니다.), 이 사용자 경험 개선은 고객들에게 어떤 가치를 제공하고, 어떤 불편함을 해소할 수 있을까요? (예: 앱 내 검색 기능 강화는 고객이 원하는 정보를 빠르고 쉽게 찾도록 도와 앱 사용 만족도를 높이고, 개인 맞춤형 콘텐츠 제공은 고객의 니즈를 충족시켜 앱 이용 시간을 늘리고 유지율을 높일 수 있습니다.), 이 상품 경쟁력 강화 전략은 원장님과 고객들에게 어떤 가치를 제공하고, 어떤 불편함을 해소할 수 있을까요? (예: 품질 좋은 네일 용품을 경쟁력 있는 가격에 제공하여 고객 만족도를 높이고, 원장님들에게는 다양한 상품 선택지를 제공하여 사업 운영 효율성을 높일 수 있습니다.)",
        "input_sentence": "서비스 연계 마케팅 강화 (공비서, 공비서 스토어, 네일아트앱)",
        "upper_objective": "(최상위) 공비서는 뷰티서비스를 제공하는 원장님과 샵을 이용하는 손님의 불편을 IT 기술로 해결하여, 원장님들의 비스니스 성장을 가속화한다. 이를 위해서 IT기술을 고도화하여 서비스 사용성을 높여간다.",
        "description": "고객에게 무엇을 제공할지 고객이 무엇을 원하는지도 표현되지 않았다",
        "score": "1",
    },
]

objEV_value_examples_2 = [
    {
        "guideline": "확보된 데이터는 어떻게 PC방 이용자들에게 더 나은 서비스를 제공하는 데 활용될 수 있을까요? (예: 게임 선호도 데이터를 기반으로 PC방 이용자들에게 맞춤형 게임 추천 및 할인 정보를 제공하여 만족도를 높일 수 있습니다.), 해당 데이터 수집 방식은 PC방 이용자들의 데이터 활용에 대한 우려를 어떻게 해소하고, 데이터 보안 및 개인정보 보호를 어떻게 확보할 수 있을까요? (예: 익명화 처리 및 개인정보 보호 정책 명시를 통해 이용자들의 데이터 활용에 대한 불안감을 해소하고, 안전한 데이터 수집 환경을 구축할 수 있습니다.), 데이터 분석 결과는 PC방 이용자들에게 어떤 유용한 정보를 제공하고, 어떤 문제 해결에 도움을 줄 수 있을까요? (예: PC방 이용 패턴 분석 결과를 토대로, 이용자들에게 적합한 PC방 추천 및 할인 정보를 제공하여 이용자 편의성을 높일 수 있습니다.)",
        "input_sentence": "오거나이저 기능 고도화 및 운영 지원을 통해 오거나이저를 만족시킨다",
        "upper_objective": "PC방 Lvup.gg 샘플 데이터 확보",
        "description": "오거나이저 기능 고도화를 가치로 하고 있으나, 기능 고도화가 구체적으로 무엇인지에 대해서는 모호하다",
        "score": "2",
    }
]

objEV_value_examples_3 = [
    {
        "guideline": "스마트 러닝 사업의 핵심 경쟁력은 어떻게 고객에게 새로운 학습 경험과 가치를 제공하여 만족도를 높일 수 있을까요? (예: AI 기반 개인 맞춤형 학습 시스템은 학습자의 수준과 목표에 맞춰 개인화된 학습 콘텐츠와 피드백을 제공하여, 효율적이고 흥미로운 학습 경험을 선사할 수 있습니다.), 온라인 교육 서비스의 개선은 고객에게 어떤 편리성과 효율성을 제공하고, 학습 만족도를 높일 수 있을까요? (예: 모바일 친화적인 학습 환경 구축은 언제 어디서든 학습 콘텐츠에 접근하고 학습 진행 상황을 확인할 수 있도록 편리성을 제공하고, 다양한 학습 자료와 커뮤니티 기능을 활용하여 학습 효과를 극대화할 수 있습니다.), 블렌디드 러닝 서비스는 고객에게 어떤 새로운 학습 경험을 제공하고, 기존 온라인 교육 서비스와 차별화된 가치를 제공할 수 있을까요? (예: 오프라인 강의와 온라인 학습 콘텐츠를 연계하여 실시간 질의응답, 그룹 스터디 등 다양한 학습 활동을 제공하고, 학습자 간의 교류와 협력을 증진시켜 학습 효과를 극대화할 수 있습니다.)",
        "input_sentence": "에듀테크 기업으로 변모한다.",
        "upper_objective": "(최상위) 국내 온라인 교육시장을 이끌며 사업시작 일 년 만에 업계 선두로 올라서고 유지해 왔다. 코로나 이후 빠르게 변하고 있는 고객 학습방식과 시장 변화에 따라, 온라인 교육 서비스로 발전시키고, 온 오프라인을 아우르는 블렌디드 러닝 서비스를 넘어 스마트 러닝 사업에 힘을 쏟고 있다.",
        "description": "에듀테크로의 변모는 학습방식이 달라진 고객들에게 주는 가치라고 볼 수 있다",
        "score": "3",
    }
]
