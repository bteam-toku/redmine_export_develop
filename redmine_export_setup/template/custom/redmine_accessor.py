from its_accessor import BaseRedmineAccessor
from redminelib.resources import Issue
from redminelib.resultsets import ResourceSet
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RedmineAccessor(BaseRedmineAccessor):
    """Redmineアクセスクラス
    """
    #
    # constructor/destructor
    #
    def __init__(self, project_name:str, url:str, key_string:str) -> None:
        """コンストラクタ
        """
        super().__init__(project_name, url, key_string)

    def __del__(self) -> None:
        """デストラクタ
        """
        pass
    
    #
    # protected methods
    #
    def _set_issue_payload(self, input_issue:Issue, input_data:dict) -> Issue:
        """Issue作成ペイロード設定

        Args:
            input_issue (Issue): 入力Issue情報
            input_data (dict): 入力データ

        Returns:
            Issue: Issue作成ペイロード
        """
        output_issue = super()._set_issue_payload(input_issue, input_data)
        # 以下、Redmine固有のフィールド設定
        return output_issue
    