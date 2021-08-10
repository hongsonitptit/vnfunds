from constants import BASE_INDEXES
from parsers.base_parser import BaseParser
from parsers.dragoncapital_parser import DragonCapitalParser
from parsers.baoviet_parser import BaoVietParser
from parsers.daichi_parser import DaichiParser
from parsers.vinacapital_parser import VinaCapitalParser
from parsers.vietcombank_parser import VietcombankParser
from parsers.ssi_parser import SSIParser
from parsers.vnindex_parser import VnIndexParser


class ParserFactory():
    @staticmethod
    def get_parser(symbol, group, url) -> BaseParser:
        if group == BASE_INDEXES:
            return VnIndexParser(symbol, url)
        if "dragoncapital.com.vn" in url:
            return DragonCapitalParser(symbol, url)
        if "baovietfund.com.vn" in url:
            return BaoVietParser(symbol, url)
        if "dfvn.com.vn" in url:
            return DaichiParser(symbol, url)
        if "vinacapital.com" in url:
            return VinaCapitalParser(symbol, url)
        if "vcbf.com" in url:
            return VietcombankParser(symbol, url)
        if "ssi.com.vn" in url:
            return SSIParser(symbol, url)

        raise Exception(f"Cannot get parser for url = {url}")
