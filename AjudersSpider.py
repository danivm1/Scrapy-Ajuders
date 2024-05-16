from typing import Iterable

import scrapy
from scrapy.http import Request, Response, FormRequest
from scrapy.crawler import CrawlerProcess

from urllib.parse import urlencode



class AjudersSpider(scrapy.Spider):
    name = "ajuders"
    formBody = {"query":""
               ,"page":"0"
               ,"attributesToRetrieve":["uniqueid"]
               ,"sortFacetValuesBy":"count"
               ,"filters":"(ImageT:\"true\" OR ImageT:\"false\") AND (EnderecoT:\"true\" OR EnderecoT:\"false\") AND (TelefoneT:\"true\" OR TelefoneT:\"false\")"
               ,"optionalFilters":""}
    
    headers = {"Accept": "*/*"
              ,"Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
              ,"Connection": "keep-alive"
              ,"Origin": "https://app.ajuders.com.br"
              ,"Referer": "https://app.ajuders.com.br/"
              ,"Sec-Fetch-Dest": "empty"
              ,"Sec-Fetch-Mode": "cors"
              ,"Sec-Fetch-Site": "cross-site"
              ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
              ,"content-type": "application/x-www-form-urlencoded"
              ,"sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\""
              ,"sec-ch-ua-mobile": "?0"
              ,"sec-ch-ua-platform": "\"Windows\""
              ,"x-algolia-api-key": "673c9fb9403cfbab6c423dbfd2899902"
              ,"x-algolia-application-id": "ILXUNWWLGR"}
    
    queryParams = {
        "x-algolia-agent": "Algolia%20for%20JavaScript%20(4.22.1)%3B%20Browser"
    }


    def start_requests(self) -> Iterable[Request]:
        yield FormRequest("https://ilxunwwlgr-dsn.algolia.net/1/indexes/LiveReports/query?" + urlencode(self.queryParams)
                     ,headers=self.headers
                     ,formdata=self.formBody #TODO: Adicionar paginacao -> formbody[page]
                     ,callback=self.parse
                     )
        
    def parse(self, response: Response) -> None:
        with open("./data.json", mode="bw") as f:
            #TODO: (Parse) Salvar apenas os campos com os dados das pessoas
            f.write(response.body)
            f.flush()


process = CrawlerProcess()
process.crawl(AjudersSpider)
process.start()