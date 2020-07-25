from elasticsearch import Elasticsearch

class ReportRemoteEs():
    '''报表类的elasticsearch操作'''
    def __init__(self, url, http_auth, index="",port=9200, use_ssl=False):
        self.mapbody = {
            "mappings": {
                "properties": {
                    "code": {
                        "type": "text"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    },
                    "date": {
                        "type": "float"
                    },
                    "link": {
                        "type": "text"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    },

                }
            }
        }

        self.es = Elasticsearch([url], http_auth=http_auth, port=port,use_ssl=use_ssl)

        #不存在则创建
        if len(index) and not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, body=self.mapbody)

    def tcbody_init(self, title_code):
        tcbody = {
            "bool": {
                "should": [{
                    "match_phrase": {
                        "title": title_code
                    }
                }, {
                    "match_phrase": {
                        "code": title_code
                    }
                }]
            }
        }
        return tcbody

    def contentbody_init(self, content):
        contentbody = {
            "match_phrase": {
                "content": content
            }
        }
        return contentbody

    def linkbody_init(self, link):
        linkbody = {
            "match_phrase": {
                "link": link
            }
        }
        return linkbody

    def qbody_init(self, title_code="", content="", link="", start="", size="", highlight=True):
        qbody = {
            "query": {
                "bool": {
                    "must": [
                    ]
                }
            },
        }

        if highlight:
            qbody['highlight'] = {
                "pre_tags": "<span style='color: red'>",
                "post_tags": "</span>",
                "fields": {
                }
            }

        if len(title_code):
            qbody["query"]["bool"]["must"].append(self.tcbody_init(title_code=title_code))
            if highlight:
                qbody["highlight"]["fields"]['title'] = {}
                qbody["highlight"]["fields"]['code'] = {}

        if len(content):
            qbody["query"]["bool"]["must"].append(self.contentbody_init(content=content))
            if highlight:
                qbody["highlight"]["fields"]['content'] = {}

        if len(link):
            qbody["query"]["bool"]["must"].append(self.linkbody_init(link=link))

        if len(start):
            qbody['from'] = int(start)

        if len(size):
            qbody['size'] = int(size)

        return qbody

    #增加
    def add(self, index, body):
        self.es.index(index=index, body=body)

    #删除
    def delete(self):
        pass

    #修改
    def updata(self):
        pass

    #查找
    def search(self, index, title_code="", content="",content_max_length=300, link="",
               start='', size='10', highlight=True, raw = False):

        qbody = self.qbody_init(title_code=title_code, content=content, link=link,
                                start=start, size=size, highlight=highlight)

        searchs = self.es.search(body=qbody, index = index)

        if not raw:
            dics = []
            for search in searchs['hits']['hits']:
                body = {
                    "code": "",
                    "title": "",
                    "date": "",
                    "link": "",
                    "content": ""
                }
                body['code'] = search['_source']['code']
                body['title'] = search['_source']['title']
                body['date'] = search['_source']['date']
                body['link'] = search['_source']['link']
                body['content'] = search['_source']['content'][0:content_max_length]

                if "highlight" in search.keys():

                    for key, value in search['highlight'].items():
                        if type(value) == type(list()):
                            body[key] = value[0]
                        else:
                            body[key] = value

                dics.append(body)

                # print("body" , body)

            return dics  # 在ES中查找

        else:
            return searchs




import pprint
import time
if __name__ == "__main__":
    es = ReportRemoteEs('es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                        http_auth=('elastic', 'HYS526956h'))

    search = es.search(index="sh_annual", title_code="包钢", content="分红", raw=False, highlight=False, content_max_length=300)
    pprint.pprint(search)
    remotees = ReportRemoteEs(url='es-cn-oew1qr55r000dbtk6.public.elasticsearch.aliyuncs.com',
                        http_auth=('elastic', "HYS526956h"), index='test')
    body = {}
    body['code'] = "600000"
    body['title'] = "浦发银行"
    body['date'] = time.time()
    body['link'] = "www.pufa.com"
    body['content'] = "测试内容"
    remotees.add(index='test', body=body)