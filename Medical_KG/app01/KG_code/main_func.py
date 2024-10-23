from app01.KG_code.question_classify import *
from app01.KG_code.question_parse import *
from app01.KG_code.search_answer import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是健康智能管家，希望可以帮到您。如果没答上来，可联系jiankang@163.com。祝您身体健康！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer

        entity = []

        for key in res_classify['args'].keys():
            entity.append(key)
        # print(key[0])
        res_search = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_search, entity)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

    def search_entity_main(self, name):
        json_list = self.searcher.search_entity(name)
        return json_list

# if __name__ == '__main__':
#     handler = ChatBotGraph()
#     while 1:
#         question = input('用户:')
#         answer = handler.chat_main(question)
#         print(answer)

main_handler = ChatBotGraph()


