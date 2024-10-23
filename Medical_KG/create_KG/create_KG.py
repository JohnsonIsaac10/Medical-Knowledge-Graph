from pymongo import MongoClient
from py2neo import Node, Relationship, NodeMatcher, Graph, RelationshipMatch, RelationshipMatcher
import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mongo_url", type=str, default="localhost")
parser.add_argument("--neo4j_url", type=str, default="bolt://localhost:7687")
parser.add_argument("--neo4j_name", type=str, default="neo4j")
parser.add_argument("--neo4j_password", type=str, default="123456")

args = parser.parse_args()

client = MongoClient(args.mongo_url)
graph = Graph(args.neo4j_url, auth=(args.neo4j_name, args.neo4j_password))

matcher = NodeMatcher(graph)

# 百度百科数据库
db = client.MedicalKG
collection = db.MedicalKG
triples = collection.find({})
nodes = []
disease_nodes = []

for triple in triples:
    nodes.append(triple['tail'])
    disease_nodes.append(triple['head'])

nodes = list(set(nodes))
disease_nodes = list(set(disease_nodes))
#
print('there are {} entities in database'.format(len(nodes)))
print('start creating nodes in neo4j knowledge graph')
for node in tqdm.tqdm(nodes):
    graph.merge(Node('Entity', name=node), 'Entity', 'name')

for disease_node in tqdm.tqdm(disease_nodes):
    graph.merge(Node('Disease', name=disease_node), 'Disease', 'name')

print('start creating relations in neo4j knowledge graph')
triples = collection.find({})
for triple in tqdm.tqdm(triples):
    head_node = matcher.match('Disease').where('_.name = "%s" '%triple['head']).first()
    new = triple['tail'].replace("\'", "\\'").replace("\"", "\\\"")
    tail_node = matcher.match('Entity').where("_.name = '%s' "% new).first()
    graph.create(Relationship(head_node, triple['relation'], tail_node))

"""数据融合"""
"""连接寻医问药数据库"""
addition_rel = {}
db_xywy = client.medical
collection_xywy = db_xywy.handled_data
print('start data fusion')
for dis in tqdm.tqdm(disease_nodes):
    rel_dic = {}
    # print(triple['head'])
    triple_xywy = collection_xywy.find({"name": "%s" % dis})
    for item in triple_xywy:
        if 'recommand_drug' in item and item['recommand_drug'] is not None:
            rel_dic['推荐药物'] = item['recommand_drug']

        if 'do_eat' in item and item['do_eat'] is not None:
            rel_dic["宜吃"] = item["do_eat"]

        if 'not_eat' in item and item['not_eat'] is not None:
            rel_dic["忌吃"] = item["not_eat"]

        if 'prevent' in item and item['prevent'] is not None:
            rel_dic["预防方法"] = item["prevent"]

        if 'cure_way' in item and item['cure_way'] is not None:
            rel_dic["治疗手段"] = item["cure_way"]

        if 'desc' in item and item['desc'] is not None:
            rel_dic['简介'] = item['desc']

    head_node = matcher.match('Disease').where('_.name = "%s" ' % dis).first()

    for rel in rel_dic:
        tail_node = Node('Entity', name=rel_dic[rel])
        graph.merge(tail_node, 'Entity', 'name')
        graph.create(Relationship(head_node, rel, tail_node))

    addition_rel[dis] = rel_dic