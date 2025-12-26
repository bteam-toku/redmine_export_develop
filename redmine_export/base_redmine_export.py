from .abstract_its_export import AbstractItsExport
from xml.etree.ElementTree import Element, SubElement
from redminelib.resources import Issue
from datetime import datetime

class BaseRedmineExport(AbstractItsExport):
    def __init__(self):
        """コンストラクタ
        """
        super().__init__()
    
    def __del__(self):
        """デストラクタ
        """
        super().__del__()
    
    def set_information(self, element, project_name:str, issue_update:datetime):
        """Informationの設定

        Args:
            element : redmine.issue
            project_name (str): プロジェクト名
        """
        el_info = SubElement(element, "information")
        el_info.set("project", project_name)
        # 日付の設定
        self.date = datetime.today()
        el_info.set("date", self.date.strftime('%Y/%m/%d'))
        el_info.set("time", self.date.strftime('%H:%M:%S'))
        # issues更新日付の設定
        self.updated_on = datetime.fromisoformat(issue_update)
        date_only = self.updated_on.date()
        time_only = self.updated_on.time()
        el_info.set("updated_on_date", date_only.strftime('%Y/%m/%d'))
        el_info.set("updated_on_time", time_only.strftime('%H:%M:%S'))

    def set_header(self, element:Element):
        """Header(Column)の設定

        Args:
            element (Element): HeaderのNode Element
        """
        # url
        el_url = SubElement(element, "url")
        el_url.set("name", r'URL')
        # id
        el_id = SubElement(element, "id")
        el_id.set("name", r'#')
        # プロジェクト
        el_project = SubElement(element, "project")
        el_project.set("name", r'プロジェクト')
        # トラッカー
        el_tracker = SubElement(element, "tracker")
        el_tracker.set("name", r'トラッカー')
        # ステータス
        el_status = SubElement(element, "status")
        el_status.set("name", r'ステータス')
        # 優先度
        el_priority = SubElement(element, "priority")
        el_priority.set("name", r'優先度')
        # 担当者
        el_assigned_to = SubElement(element, "assigned_to")
        el_assigned_to.set("name", r'担当者')
        # 親チケット
        el_parent = SubElement(element, "parent")
        el_parent.set("name", r'親チケット')
        # 親の題名
        el_parent_subject = SubElement(element, "parent_subject")
        el_parent_subject.set("name", r'親の題名')
        # 題名
        el_subject = SubElement(element, "subject")
        el_subject.set("name", r'題名')
        # 対象バージョン
        el_fixed_version = SubElement(element, "fixed_version")
        el_fixed_version.set("name", r'対象バージョン')
        # 開始日
        el_start_date = SubElement(element, "start_date")
        el_start_date.set("name", r'開始日')
        # 期日
        el_due_date = SubElement(element, "due_date")
        el_due_date.set("name", r'期日')
        # 実開始日
        el_actual_start_date = SubElement(element, "actual_start_date")
        el_actual_start_date.set("name", r'実開始日')
        # 実終了日
        el_actual_due_date = SubElement(element, "actual_due_date")
        el_actual_due_date.set("name", r'実終了日')
        # 進捗率
        el_done_ratio = SubElement(element, "done_ratio")
        el_done_ratio.set("name", r'進捗率')
        # 予定工数
        el_estimated_hours = SubElement(element, "estimated_hours")
        el_estimated_hours.set("name", r'予定工数')
        # 作業工数
        el_spent_hours = SubElement(element, "spent_hours")
        el_spent_hours.set("name", r'作業工数')
        # 合計予定工数
        el_total_estimated_hours = SubElement(element, "total_estimated_hours")
        el_total_estimated_hours.set("name", r'合計予定工数')
        # 合計作業工数
        el_total_spent_hours = SubElement(element, "total_spent_hours")
        el_total_spent_hours.set("name", r'合計作業工数')
        # 作成日
        el_created_on = SubElement(element, "created_on")
        el_created_on.set("name", r'作成日')
        # 更新日
        el_updated_on = SubElement(element, "updated_on")
        el_updated_on.set("name", r'更新日')
        # 終了日
        el_closed_on = SubElement(element, "closed_on")
        el_closed_on.set("name", r'終了日')
    
    def set_body(self, element: Element, issue: Issue, dict):
        """Body(Data)の設定

        Args:
            element (Element): BodyのNode Element
            issue : redmine.issues
            dict : redmine.issueの親チケット情報
        """
        # url
        el_url = SubElement(element, "url")
        el_url.text = str(issue.url if hasattr(issue,"url") else None)
        # id
        el_id = SubElement(element, "id")
        el_id.text = str(issue.id if hasattr(issue,"id") else None)
        # プロジェクト
        el_project = SubElement(element, "project")
        el_project.text = str(issue.project.name if hasattr(issue,"project") else None)
        # トラッカー
        el_tracker = SubElement(element, "tracker")
        el_tracker.text = str(issue.tracker.name if hasattr(issue,"tracker") else None)
        # ステータス
        el_status = SubElement(element, "status")
        el_status.text = str(issue.status.name if hasattr(issue,"status") else None)
        # 優先度
        el_priority = SubElement(element, "priority")
        el_priority.text = str(issue.priority.name if hasattr(issue,"priority") else None)
        # 担当者
        el_assigned_to = SubElement(element, "assigned_to")
        el_assigned_to.text = str(issue.assigned_to.name if hasattr(issue,"assigned_to") else None)
        # 親チケット
        el_parent = SubElement(element, "parent")
        el_parent.text = str(issue.parent if hasattr(issue,"parent") else None)
        # 親の題名
        el_parent_subject = SubElement(element, "parent_subject")
        if(el_parent.text == 'None'):
            el_parent_subject.text = 'None'
        else:
            if(dict.get(int(issue.parent)) != None):
                el_parent_subject.text = dict[int(issue.parent)]
            else:
                el_parent_subject.text = 'None'
        # 題名
        el_subject = SubElement(element, "subject")
        el_subject.text = str(issue.subject if hasattr(issue,"subject") else None)
        # 対象バージョン
        el_fixed_version = SubElement(element, "fixed_version")
        el_fixed_version.text = str(issue.fixed_version if hasattr(issue,"fixed_version") else None)
        # 開始日
        el_start_date = SubElement(element, "start_date")
        el_start_date.text = str(issue.start_date if hasattr(issue,"start_date") else None)
        # 期日
        el_due_date = SubElement(element, "due_date")
        el_due_date.text = str(issue.due_date if hasattr(issue,"due_date") else None)
        # 実開始日
        el_actual_start_date = SubElement(element, "actual_start_date")
        el_actual_start_date.text = str(issue.actual_start_date if hasattr(issue,"actual_start_date") else None)
        # 実終了日
        el_actual_due_date = SubElement(element, "actual_due_date")
        el_actual_due_date.text = str(issue.actual_due_date if hasattr(issue,"actual_due_date") else None)
        # 進捗率
        el_done_ratio = SubElement(element, "done_ratio")
        el_done_ratio.text = str(issue.done_ratio if hasattr(issue,"done_ratio") else None)
        # 予定工数
        el_estimated_hours = SubElement(element, "estimated_hours")
        el_estimated_hours.text = str(issue.estimated_hours if hasattr(issue,"estimated_hours") else None)
        # 作業工数
        el_spent_hours = SubElement(element, "spent_hours")
        el_spent_hours.text = str(issue.spent_hours if hasattr(issue,"spent_hours") else None)
        # 合計予定工数
        el_total_estimated_hours = SubElement(element, "total_estimated_hours")
        el_total_estimated_hours.text = str(issue.total_estimated_hours if hasattr(issue,"total_estimated_hours") else None)
        # 合計作業工数
        el_total_spent_hours = SubElement(element, "total_spent_hours")
        el_total_spent_hours.text = str(issue.total_spent_hours if hasattr(issue,"total_spent_hours") else None)
        # 作成日
        el_created_on = SubElement(element, "created_on")
        el_created_on.text = str(issue.created_on if hasattr(issue,"created_on") else None)
        # 更新日
        el_updated_on = SubElement(element, "updated_on")
        el_updated_on.text = str(issue.updated_on if hasattr(issue,"updated_on") else None)
        # 終了日
        el_closed_on = SubElement(element, "closed_on")
        el_closed_on.text = str(issue.closed_on if hasattr(issue,"closed_on") else None)

