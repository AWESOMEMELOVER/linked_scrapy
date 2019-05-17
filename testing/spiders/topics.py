import scrapy
import string
from scrapy.shell import inspect_response


class TopicSpider(scrapy.Spider):
    name = "topics"
    start_urls = ['https://www.linkedin.com/uas/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={'session_key': 'mickaborscha@gmail.com',
                                                          'session_password': 'kjkszpj97'},
                                                callback=self.after_login)

    def after_login(self, response):

        topic_urls = ['https://www.linkedin.com/directory/topics-' + char + '/' for char in string.ascii_lowercase]

        if response.status == 200:
            return scrapy.Request(url='https://www.linkedin.com/directory/topics-a/', callback=self.parse_topics)
        else:
            self.logger.error('Error with authentication')

    def parse_topics(self, response):

        print("procesing:" + response.url)

        topics = response.xpath("//div[@class='columns']/ul//text()").extract()

        for index, topic in enumerate(topics[10:20]):
            subtopics = scrapy.Request(url='https://www.linkedin.com/directory/topics-a-' + str(index + 1) + '/',
                                       callback=self.parse_subtopics)
            yield {topic: subtopics}

    def parse_subtopics(self, response):
        subtopics = response.xpath("//div[@class='columns']/ul/li/a/text()").extract()
        print(subtopics)
        yield subtopics
