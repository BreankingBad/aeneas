#!/usr/bin/env python
# coding=utf-8

# aeneas is a Python/C library and a set of tools
# to automagically synchronize audio and text (aka forced alignment)
#
# Copyright (C) 2012-2013, Alberto Pettarin (www.albertopettarin.it)
# Copyright (C) 2013-2015, ReadBeyond Srl   (www.readbeyond.it)
# Copyright (C) 2015-2016, Alberto Pettarin (www.albertopettarin.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function

from aeneas.syncmap.smfbase import SyncMapFormatBase
from aeneas.timevalue import TimeValue
import aeneas.globalfunctions as gf


class SyncMapFormatTextGrid(SyncMapFormatBase):

    TAG = u"SyncMapFormatTextGrid"

    DEFAULT = "textgrid"
    """
    Praat full TextGrid format::

        File type = "ooTextFile"
        Object class = "TextGrid"

        xmin = 0.0
        xmax = 7.89
        tiers? <exists>
        size = 1
        item []:
            item [1]:
                class = "IntervalTier"
                name = "Token"
                xmin = 0.0
                xmax = 7.89
                intervals: size = 3
                intervals [1]:
                    xmin = 0.0
                    xmax = 1.234
                    text = "First fragment text"
                intervals [2]:
                    xmin = 1.234
                    xmax = 5.678
                    text = "Second fragment text"
                intervals [3]:
                    xmin = 5.678
                    xmax = 7.89
                    text = "Third fragment text"

    * Multiple levels: no (not yet)
    * Multiple lines: no

    See also 

    Note that at the moment reading support is limited
    to the first tier in the TextGrid file.

    .. versionadded:: 1.6.1
    """

    SHORT = "textgrid_short"
    """
    Praat short TextGrid format::

        File type = "ooTextFile"
        Object class = "TextGrid"

        0.0
        7.89
        <exists>
        1
        "IntervalTier"
        "Token"
        0.0
        7.89
        3
        0.0
        1.234
        "First fragment text"
        1.234
        5.678
        "Second fragment text"
        5.678
        7.89
        "Third fragment text"

    * Multiple levels: no (not yet)
    * Multiple lines: no

    See also 

    Note that at the moment reading support is limited
    to the first tier in the TextGrid file.

    .. versionadded:: 1.6.1
    """

    def parse(self, input_text, syncmap):
        try:
            import tgt
        except ImportError as exc:
            self.log_exc(u"Python module tgt is not installed", exc, True, ImportError)

        # from https://github.com/hbuschme/TextGridTools/blob/master/tgt/io.py
        # get all non-empty lines
        lines = [l.strip() for l in input_text.splitlines()]
        lines = [l for l in lines if l not in ["", "\""]]
        # long format => has "xmin = 0.0" in its 3rd line
        if lines[2].startswith("xmin"):
            read_function = tgt.io.read_long_textgrid
        else:
            read_function = tgt.io.read_short_textgrid
        textgrid = read_function(
            filename="Dummy TextGrid file",
            stg=lines,
            include_empty_intervals=True
        )
        if len(textgrid.tiers) == 0:
            # no tiers => nothing to read => empty sync map
            return
        # TODO at the moment we support only one tier, the first
        for i, interval in enumerate(textgrid.tiers[0].intervals, 1):
            self._add_fragment(
                syncmap=syncmap,
                identifier=u"f%06d" % i,
                lines=[interval.text],
                begin=TimeValue(interval.start_time.real),
                end=TimeValue(interval.end_time.real)
            )

    def format(self, syncmap):
        try:
            import tgt
        except ImportError as exc:
            self.log_exc(u"Python module tgt is not installed", exc, True, ImportError)
        # from https://github.com/hbuschme/TextGridTools/blob/master/tgt/io.py
        textgrid = tgt.TextGrid()
        tier = tgt.IntervalTier(name="Token")
        for fragment in syncmap.fragments:
            begin = float(fragment.begin)
            end = float(fragment.end)
            text = fragment.text_fragment.text
            if text == u"":
                text = u"SIL"
            interval = tgt.Interval(begin, end, text=text)
            tier.add_interval(interval)
        textgrid.add_tier(tier)
        if self.variant == self.DEFAULT:
            msg = tgt.io.export_to_long_textgrid(textgrid)
        else:
            msg = tgt.io.export_to_short_textgrid(textgrid)
        return gf.safe_unicode(msg)
