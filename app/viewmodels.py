#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-27 16:43:13
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-27 17:21:49
#
from collections import OrderedDict


class TalkViewModel(object):
    def __init__(self, talk):
        """
        :type talk: Talk
        :rtype: None
        """
        createTime = talk.createDatetime
        date = createTime.split()[0].split('-', 1)
        self.year = date[0]
        self.date = date[1].replace('-', '/')
        self.content = talk.content


class TalksViewModel(object):
    def __init__(self, talks):
        """
        :type talks: List[TalkViewModel]
        :rtype: None
        """
        self.res = {}

        for t in talks:
            if not self.res.get(t.year):
                self.res[t.year] = []
            self.res[t.year].append(t)

        self.res = OrderedDict(sorted(self.res.items(), reverse=True))
