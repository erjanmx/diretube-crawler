# -*- coding: utf-8 -*-
import scrapy
from ..models.models import Video, Tag, VideoTag


class DiretubeSpider(scrapy.Spider):
    name = 'diretube'

    def start_requests(self):
        urls = ['https://www.diretube.com/browse-comedy-videos-{}-date.html'.format(i) for i in range(1, 77)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        video_urls = [url for url in self.extract_video_thumb(response) if str(url).startswith('https://www.diretube.com/')]

        for url in video_urls:
            yield scrapy.Request(url=url, callback=self.parse_description)


    def parse_description(self, response):
        url = response.url
        tags = self.extract_tags(response)
        title = self.extract_title(response)
        views = self.extract_views(response)
        added_at = self.extract_time(response)
        added_by = self.extract_author(response)
        categories = ', '.join(self.extract_categories(response))

        video = Video.first_or_create(url=url, title=title, added_by=added_by, views=views, added_at=added_at, categories=categories)
        tag_ids = []
        for tag in tags:
            tag = Tag.first_or_create(name=str(tag).lower())
            tag_ids.append(tag.id)

        video.tags().sync(tag_ids)

        request = scrapy.Request(url=self.extract_video_url(response), callback=self.parse_video)
        request.meta['video'] = video
        yield request

    def parse_video(self, response):
        video = response.meta['video']
        video.video_url = str(response.xpath('//meta[@property="og:video"]/@content').extract_first())
        video.preview_url = response.xpath('//meta[@property="og:image"]/@content').extract_first()
        video.save()

    # extractors
    def extract_video_thumb(self, response):
        return response.xpath('//div[@class="pm-video-thumb"]/a/@href').extract()

    def extract_title(self, response):
        return response.css('title::text').extract_first()

    def extract_author(self, response):
        return response.xpath('//div[@class="pm-video-posting-info"]/a/text()').extract_first()

    def extract_time(self, response):
        return response.xpath('//div[@class="pm-video-posting-info"]/time/@datetime').extract_first()

    def extract_tags(self, response):
        return response.xpath('//div[@class="pm-video-description"]/dl/dd[2]/a/text()').extract()

    def extract_categories(self, response):
        return response.xpath('//div[@class="pm-video-description"]/dl/dd[1]/a/text()').extract()

    def extract_views(self, response):
        return response.xpath('//span[@class="pm-video-views"]/strong/text()').extract_first()

    def extract_video_url(self, response):
        return 'https:' + str(response.xpath('//div[@id="Playerholder"]//iframe/@src').extract_first())
