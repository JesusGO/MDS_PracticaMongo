import pymongo
from pymongo import MongoClient
from xml.dom import pulldom
import publication

main_nodes = {"article", "inproceedings", "incollection"}


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    database = client['mds']
    db_pb = database['publications']

    pbs = []
    total_pb = 0

    doc = pulldom.parse('dblp.xml')

    for event, node in doc:

        if event == pulldom.START_ELEMENT and node.tagName in main_nodes:
            doc.expandNode(node)
            pb = publication.Publication(node)
            pb.exec_node()
            pbs.append(pb.serialize())

            if len(pbs) > 10000:
                db_pb.insert_many(pbs)
                total_pb = total_pb + len(pbs)
                pbs = []

    if len(pbs) > 0:
        db_pb.insert_many(pbs)
        total_pb = total_pb + len(pbs)

    print("Total publicaciones: ", total_pb)
