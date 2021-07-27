import plac
from elasticsearch import AsyncElasticsearch
from utils.runner import ClinicalTrialsExecutor
from utils.parsers import CDS2021_Parser
from utils.query import TestTrialsQuery
import asyncio

@plac.opt('addr', "Elasticsearch Address", type=str)
@plac.opt('es_port', "Elasticsearch Port Number", type=int)
@plac.opt('topics_path', "Path to query topics", type=str)
@plac.opt('index_name', "Name of Elasticsearch Index", type=str)
@plac.opt('output_file', "Output file name and/or path", type=str)
@plac.opt('size', "Retrieved Input Size", type=int)
def main(addr, es_port, topics_path, index_name, output_file, size=1000):
    topics = CDS2021_Parser.get_topics(csvfile=open(topics_path))
    es = AsyncElasticsearch([{'host': addr, 'port': es_port}], timeout=600)
    query = TestTrialsQuery(topics=topics, mappings_path="./assets/mapping.json")

    ex = ClinicalTrialsExecutor(topics=topics, client=es,
                           index_name=index_name, output_file=output_file,
                           return_size=size, query=query)

    asyncio.run(ex.run_all_queries(serialize=True))

    asyncio.run(es.close())


if __name__ == "__main__":
    plac.call(main)

