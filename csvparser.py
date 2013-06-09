# -*- coding: utf-8 -*-

BOL = 1 # beginning of line
BOC = 2 # beginning of column
IN_COL = 3
WAIT_LF = 4
IN_QUOT = 5
WAIT_QUOT = 6
WAIT_LF_IN_QUOT = 7

class CsvParser(object):

    def fin(self, c):
        self.doing = False

    def to_bol(self, c):
        self.status = BOL;

    def to_boc(self, c):
        self.status = BOC;

    def to_in_col(self, c):
        self.status = IN_COL

    def to_wait_lf(self, c):
        self.status = WAIT_LF

    def to_in_quot(self, c):
        self.status = IN_QUOT

    def to_wait_quot(self, c):
        self.status = WAIT_QUOT

    def to_wait_lf_in_quot(self, c):
        self.status = WAIT_LF_IN_QUOT

    def push_row(self, c):
        self.rows.append(self.row)
        self.row = []
        self.col = ''

    def push_col(self, c):
        self.row.append(self.col)
        self.col = ''

    def append_col(self, c):
        self.col += c

    def append_quote(self, c):
        self.col += '"'

    table = {
        BOL: [
            ('',   [fin]),
            ('\r', [to_wait_lf]),
            ('\n', [push_col, push_row]),
            (',',  [push_col, to_boc]),
            ('"',  [to_in_quot]),
            (None, [append_col, to_in_col])],
        BOC: [
            ('',   [push_col, push_row, fin]),
            ('\r', [to_wait_lf]),
            ('\n', [push_col, push_row, to_bol]),
            (',',  [push_col]),
            ('"',  [to_in_quot]),
            (None, [append_col, to_in_col])],
        IN_COL: [
            ('',   [push_col, push_row, fin]),
            ('\r', [to_wait_lf]),
            ('\n', [push_col, push_row, to_bol]),
            (',',  [push_col, to_boc]),
            (None, [append_col])],
        WAIT_LF: [
            ('',   [push_col, push_row, fin]),
            ('\r', [push_col, push_row]),
            ('\n', [push_col, push_row, to_bol]),
            (',',  [push_col, push_row, push_col, to_boc]),
            ('"',  [push_col, push_row, to_in_quot]),
            (None, [push_col, push_row, append_col, to_in_col])],
        IN_QUOT: [
            ('',   [push_col, push_row, fin]),
            ('"',  [to_wait_quot]),
            (None, [append_col])],
        WAIT_QUOT: [
            ('',   [push_col, push_row, fin]),
            ('\r', [to_wait_lf_in_quot]),
            ('\n', [push_col, push_row, to_bol]),
            (',',  [push_col, to_boc]),
            ('"',  [append_quote, to_in_quot]),
            (None, [append_col, to_in_quot])],
        WAIT_LF_IN_QUOT: [
            ('',   [push_col, push_row, fin]),
            ('\r', [push_col, push_row, to_wait_lf]),
            ('\n', [push_col, push_row, to_bol]),
            (',',  [push_col, push_row, push_col, to_boc]),
            ('"',  [push_col, push_row, to_in_quot]),
            (None, [push_col, push_row, append_col, to_in_col])]
        }

    def parse(self, src):

        self.rows = []
        self.row = []
        self.col = ''
        self.status = BOL
        self.doing = True

        while self.doing:
            c = src.read(1)
            for d, methods in self.table[self.status]:
                if d is None or c == d:
                    for method in methods:
                        method(self, c)
                    break

        return self.rows
