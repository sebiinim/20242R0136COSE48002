from flask import Flask, request
from flask_restx import Resource, Namespace, fields

### Flask 관련 코드
Evaluation = Namespace(name='polyglot-ko', description='evaluation')

evaluation_fields = Evaluation.model('Evaluation', {
    'isObjective' : fields.Boolean(required=True, description='The objective', example=True),
    'upper_objective': fields.String(required=True, description='The upper objective', example='고객이 하루에 한 끼는 요리를 하고 싶게 한다.'),
    'input_sentence' : fields.String(required=True, description='The input sentence', example='일상 요리들의 조리 과정을 50% 줄일 수 있는 제품+요리법을 연구, 개발한다.'),
    'company' : fields.String(required=True, description='The company', example='회사명'),
    'field' : fields.String(required=True, description='The field', example='식품'),
    'team' : fields.String(required=True, description='The team', example='조직명'),
})

keyresult_template = """
<입력>
상위목표 = {upper_objective}
핵심결과 = {input_sentence}
기업명 = {company}
업종 = {field}
조직명 = {team}
</입력>
"""

@Evaluation.route('')
class EvaluationResource(Resource):
    @Evaluation.expect(evaluation_fields)
    def post(self):
        request_data = request.json
        if request_data["isObjective"] == True:
          text = keyresult_template.format(upper_objective=request_data["upper_objective"], input_sentence=request_data["input_sentence"], company = request_data["company"], field = request_data["field"], team = request_data["team"])
          #modeloutput = evaluation(text)
          modeloutput = text
          return {"model_output": modeloutput}
        else:
          return "keyresult는 아직 구현되지 않았습니다."

