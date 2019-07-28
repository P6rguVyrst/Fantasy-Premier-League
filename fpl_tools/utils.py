#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import requests


LOGGER = logging.getLogger(__name__)


class APIClient:

    def __init__(self, api_url):
        self.api = api_url

    def __request(self, method: str, endpoint: str):
        url = self.api + endpoint
        LOGGER.debug("{}::{}".format(method, url))
        return requests.request(method, url)

    def get(self, endpoint):
        return self.__request("GET", endpoint)


def assert_folder_exists(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
