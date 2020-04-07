import json
from xml.dom import pulldom
import publication

main_nodes = ["article", "inproceedings", "incollection"]


if __name__ == "__main__":

    doc = pulldom.parse('dblp.xml')

    with open('parse_xml.json', 'w') as f:
        
        for event, node in doc:
            if event == pulldom.START_ELEMENT and node.tagName in main_nodes:
                doc.expandNode(node)
                pb = publication.Publication(node)
                pb.exec_node()
                
                f.write(json.dumps(pb.serialize()) + ' \n')
    f.close()