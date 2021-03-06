from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import request
from source_checker.source_checker import SourceChecker

app = Flask(__name__)
api = Api(app)

# users = [
#     {
#         "name": "Nicholas",
#         "age": 42,
#         "occuptaion": "Network Engineer"
#     },
#     {
#         "name": "Elvin",
#         "age": 35,
#         "occuptaion": "Doctor"
#     }
# ]


class Message(Resource):
    # def get(self, name):
    #     for user in users:
    #         if name == user["name"]:
    #             return user, 200
    #     return "User not found", 404

    def post(self):

        data = request.get_json()

        body = data['messages'][0]['body']
        chatId = data['messages'][0]['chatId']
        language = 'english'

        #text = sys.argv[1]
        # try:
        #     language = sys.argv[2]
        # except IndexError:
        #     language = 'english'
        sc = SourceChecker(body, language)
        queries = sc.get_queries()
        domains = sc.get_urls(queries)
        sc.load_domains()
        output = sc.render_output(domains)
        sc.render_graph(domains)

        return output, 201


api.add_resource(Message, "/webhook/")
app.run(host="0.0.0.0", debug=True)
