from redmine_export.base_redmine_analyze import BaseRedmineAnalyze
from custom.redmine_accessor import RedmineAccessor
from xml.etree.ElementTree import Element, SubElement

class RedmineAnalyze(BaseRedmineAnalyze):
    """Redmine分析クラス
    """
    __accessor: RedmineAccessor = None

    #
    # コンストラクタ/デストラクタ
    #
    def __init__(self, accessor: RedmineAccessor):
        """コンストラクタ
        """
        self.__accessor = accessor
        super().__init__()
    
    def __del__(self):
        """デストラクタ
        """
        super().__del__()

        #
    # public method
    #
    def set_header(self, element: Element):
        """Header(Column)の設定

        Args:
            element (Element): HeaderのNode Element
        """
        super().set_header(element)
        # ユーザー固有のコードを以下に追加
    
    def set_body(self, element: Element, issue, dict, date, calendar):
        """Body(Data)の設定

        Args:
            element (Element): BodyのNode Element
            issue : redmine.issues
            dict : redmine.issueの親チケット情報
            date : 基準日(データ取得日の前日)
            calendar : 休日情報
        """
        super().set_body(element, issue, dict, date, calendar)
        # ユーザー固有のコードを以下に追加
