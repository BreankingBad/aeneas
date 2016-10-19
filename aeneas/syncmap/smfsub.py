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

from aeneas.syncmap.smfgsubtitles import SyncMapFormatGenericSubtitles
import aeneas.globalfunctions as gf


class SyncMapFormatSUB(SyncMapFormatGenericSubtitles):

    TAG = u"SyncMapFormatSUB"

    SUB = "sub"
    """
    SubViewer (SBV/SUB) caption/subtitle format,
    with multiple lines per fragment are separated by [br]::

        [SUBTITLE]
        00:00:00.000,00:00:01.234
        First fragment text

        00:00:01.234,00:00:05.678
        Second fragment text[br]Second line of second fragment

        00:00:05.678,00:00:07.890
        Third fragment text[br]Second line of third fragment

    * Multiple levels: no
    * Multiple lines: yes

    See also https://wiki.videolan.org/SubViewer/

    Note that the ``[INFORMATION]`` header is ignored when reading,
    and it is not produced when writing.
    Moreover, extensions
    (i.e., ``[COLF]``, ``[SIZE]``, ``[FONT]``)
    are not supported.

    .. versionadded:: 1.4.1
    """

    SBV = "sbv"
    """
    SubViewer (SBV/SUB) caption/subtitle format,
    with multiple lines per fragment are separated by a newline character::

        [SUBTITLE]
        00:00:00.000,00:00:01.234
        First fragment text

        00:00:01.234,00:00:05.678
        Second fragment text
        Second line of second fragment

        00:00:05.678,00:00:07.890
        Third fragment text
        Second line of third fragment

    * Multiple levels: no
    * Multiple lines: yes

    See also https://wiki.videolan.org/SubViewer/

    Note that the ``[INFORMATION]`` header is ignored when reading,
    and it is not produced when writing.
    Moreover, extensions
    (i.e., ``[COLF]``, ``[SIZE]``, ``[FONT]``)
    are not supported.
    """

    DEFAULT = SUB

    def __init__(self, variant=DEFAULT, parameters=None, rconf=None, logger=None):
        super(SyncMapFormatSUB, self).__init__(variant=variant, parameters=parameters, rconf=rconf, logger=logger)
        self.header_string = u"[SUBTITLE]"
        self.header_might_not_have_trailing_blank_line = True 
        self.footer_string = u"[END SUBTITLE]"
        self.cue_has_identifier = False
        self.cue_has_optional_identifier = False
        self.time_values_separator = u","
        if self.variant == self.DEFAULT:
            self.line_break_symbol = u"[br]"
        else:
            self.line_break_symbol = u"\n"
        self.parse_time_function = gf.time_from_hhmmssmmm
        self.format_time_function = gf.time_to_hhmmssmmm
