
class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        searches = []
        for question_type in question_types:
            search_ = {}
            search_['question_type'] = question_type
            search = []
            if question_type == 'disease_symptom':
                search = self.search_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                search = self.search_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                search = self.search_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'cause_disease':
                search = self.search_transfer(question_type, entity_dict.get('cause'))

            elif question_type == 'disease_not_food':
                search = self.search_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                search = self.search_transfer(question_type, entity_dict.get('disease'))


            elif question_type == 'disease_drug':
                search = self.search_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                search = self.search_transfer(question_type, entity_dict.get('drug'))


            elif question_type == 'disease_prevent':
                search = self.search_transfer(question_type, entity_dict.get('disease'))


            elif question_type == 'disease_cureway':
                search = self.search_transfer(question_type, entity_dict.get('disease'))


            elif question_type == 'disease_desc':
                search = self.search_transfer(question_type, entity_dict.get('disease'))

            if search:
                search_['search'] = search
                searches.append(search_)

        return searches

    '''针对不同的问题，分开进行处理'''
    def search_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        search = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            search = ["MATCH (m:Disease)-[r:常见病因]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        elif question_type == 'cause_disease':
            base = "MATCH (m:Disease)-[r:常见病因]->(n:Entity) where n.name contains '{}' "
            for i in range(1, len(entities)):
                base = base + " or n.name contains '{}' "
            base = base + " return m.name, n.name"
            search = [base.format(*entities)]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            search = ["MATCH (m:Disease)-[r:预防方法]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            search = ["MATCH (m:Disease)-[r:治疗手段]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            search = ["MATCH (m:Disease)-[r:简介]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            search = ["MATCH (m:Disease)-[r:常见症状]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            base = "MATCH (m:Disease)-[r:常见症状]->(n:Entity) where n.name contains '{}' "
            for i in range(1, len(entities)):
                base = base + " and n.name contains '{}' "
            base = base + " return m.name, n.name"
            search = [base.format(*entities)]
            # search = ["MATCH (m:Disease)-[r:常见症状]->(n:Entity) where n.name contains '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            search = ["MATCH (m:Disease)-[r:忌吃]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            search = ["MATCH (m:Disease)-[r:宜吃]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]


        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            search = ["MATCH (m:Disease)-[r:推荐药物]->(n:Entity) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            # search = ["MATCH (m:Disease)-[r:推荐药物]->(n:Entity) where n.name = '{0}' return m.name, n.name".format(i) for i in entities]
            search = ["MATCH p=(m:Disease)-[r:推荐药物]->(n:Entity) where any (x IN n.name WHERE x = '{0}')  RETURN m.name, n.name".format(i) for i in entities]

        return search


if __name__ == '__main__':
    handler = QuestionPaser()
