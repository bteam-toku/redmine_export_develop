from redmine_export.base_redmine_export import BaseRedmineExport
from custom.redmine_accessor import RedmineAccessor
from xml.etree.ElementTree import Element, SubElement
from redminelib.resources import Issue

class RedmineExport(BaseRedmineExport):
    """Redmine_exportの具象化クラス
    """
    __accessor: RedmineAccessor = None

    #
    # コンストラクタ・デストラクタ
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
    # public methods
    #
    def set_header(self, element:Element):
        """Header(Column)の設定

        Args:
            element (Element): HeaderのNode Element
        """
        super().set_header(element)
        # ユーザー固有のコードを以下に追加

    def set_body(self, element: Element, issue: Issue, dict):
        """Body(Data)の設定

        Args:
            element (Element): BodyのNode Element
            issue : redmine.issues
            dict : redmine.issueの親チケット情報
        """
        super().set_body(element, issue, dict)
        # ユーザー固有のコードを以下に追加
