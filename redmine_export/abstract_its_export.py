from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import Element
from redminelib.resources import Issue

class AbstractItsExport(metaclass=ABCMeta):
    def __init__(self) -> None:
        """コンストラクタ
        """
        pass

    def __del__(self) -> None:
        """デストラクタ
        """
        pass

    @abstractmethod
    def set_header(self, element:Element) -> None:
        """Header(Column)の設定

        Args:
            element (Element): HeaderのNode Element
        """
        pass

    @abstractmethod
    def set_body(self, element:Element, issue:Issue, dict) -> None:
        """Body(Data)の設定

        Args:
            element (Element): BodyのNode Element
            issue : redmine.issues
            dict : redmine.issueの親チケット情報
        """
        pass
