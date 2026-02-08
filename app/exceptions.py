#!/usr/bin/env python
# -*- coding: utf-8 -*-


class NotFoundException(Exception):
    def __init__(self, identifier: int | str):
        self.identifier = identifier


class MissingIdOrNameException(Exception):
    def __init__(self, item: str):
        self.item = item
