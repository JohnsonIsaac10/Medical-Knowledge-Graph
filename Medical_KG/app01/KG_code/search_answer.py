from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")
        self.num_limit = 20

    '''搜索疾病实体，知识图谱可视化'''
    def search_entity(self, name):
        rels = self.g.schema.relationship_types
        json_list = []
        for rel in rels:
            result = {}
            end_name = self.g.run(
                'match p=(d:Disease)-[r:{0}]->(n:Entity) where d.name = "{1}" return n.name'.format(rel, name)).data()
            if len(end_name) != 0:
                result['rel_type'] = rel
                result['source'] = name
                result['target'] = end_name[0]['n.name']
                json_list.append(result)
        return json_list

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, searches, entity):
        final_answers = []
        for search_ in searches:
            question_type = search_['question_type']
            queries = search_['search']
            answers = []
            for query in queries:
                # print(query)
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_search(question_type, answers, entity)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_search(self, question_type, answers, entity):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            # subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format('、'.join(list(entity)[:self.num_limit]), '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'cause_disease':
            desc = [i['m.name'] for i in answers]
            final_answer = '{0}可能会导致的疾病有：{1}等'.format('、'.join(list(entity)[:self.num_limit]), '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'disease_cureway':
            desc = ['；'.join(i['n.name']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'disease_desc':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}忌吃的食物包括有：{1}'.format(subject, '；'.join(list(set(desc[0]))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}宜吃的食物包括有：{1}'.format(subject, '；'.join(list(set(do_desc[0]))[:self.num_limit]))

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc[0]))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            # subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有：{1}'.format('、'.join(list(entity)[:self.num_limit]), '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
