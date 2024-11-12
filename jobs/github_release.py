import os
import json
import scrapy
import requests
import logging
from scrapy.crawler import CrawlerProcess
from typing import Dict
from src.job import AbstractJob
from src.notifier.email_notifier import send_code_template, send_error

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

TO_EMAIL_ADDRESS = os.environ.get("TO_EMAIL_ADDRESS")


class GitHubRelease(scrapy.Spider):
    name = "GitHubRelease"

    def start_requests(self):
        urls = [
            'https://api.github.com/repos/huakunshen/wol-web/releases/latest',
            'https://api.github.com/repos/fmtree-dev/fmtree/releases/latest',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        error = response.status != 200
        msg = "" if not error else "Request failed"
        data = response.json()
        tag = data['tag_name'] if not error else ""
        repo = data['url'].split("/")[-3] if not error else ""
        return {"repo": repo, "tag": tag, "msg": msg, "error": error}


class Job(AbstractJob):
    name = "GitHub Release Monitor"

    def __init__(self) -> None:
        super().__init__()
        self.result_filename = "result.json"

    def run(self):
        process = CrawlerProcess(settings={
            "FEEDS": {
                self.result_filename: {"format": "json"},
            },
        })
        try:
            process.crawl(GitHubRelease)
            process.start()
            with open(self.result_filename, "r") as f:
                result = json.load(f)
            self.success(result)
        except Exception as e:
            self.fail(str(e))
        finally:
            os.remove(self.result_filename)

    def success(self, result: Dict):
        # TODO: send_code_template(self.name, code, TO_EMAIL_ADDRESS)
        print("Success: In practice, to send an email, comment out the line above")
        for row in result:
            if row['error']:
                raise ValueError(row["msg"])
            print(f"Repo {row['repo']} has release {row['tag']}")

    def fail(self, msg: str):
        subject = f"Error from Cron Crawler: {self.name}"
        print(subject)
        print(msg)
        # send_error(subject, msg, TO_EMAIL_ADDRESS)
