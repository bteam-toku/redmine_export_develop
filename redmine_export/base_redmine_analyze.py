from redmine_export.abstract_its_export import AbstractItsExport
from bteam_utils import CommonCalendar, CommonEVM
from bteam_utils.common_evm import CommonEVMInput
from datetime import datetime, timedelta
import datetime as dt
from xml.etree.ElementTree import Element, SubElement

class BaseRedmineAnalyze(AbstractItsExport):
    # カレンダーインスタンス
    calendar:CommonCalendar = None
    # DATE
    _as_of_date = None # 基準日
    # Issue Data
    _start_date = None # 開始日
    _due_date = None # 期日
    _actual_start_date = None # 実開始日
    _actual_due_date = None # 実終了日
    _done_ratio:float = 0 # 進捗率
    _estimated_hours:float = 0 # 予定工数
    _spent_hours:float = 0 # 作業工数
    # Analysis Data
    _status_ended:bool = False # 終了
    _status_ongoing:bool = False # 作業中
    _status_notyet:bool = False # 未着手
    _status_onhold:bool = False # 保留
    _status_reject:bool = False # 却下
    _analyze_notassigned:bool = False # 担当未割当
    _analyze_unplaned:bool = False # 日程未計画
    _analyze_startdate_delayed:bool = False # 開始遅延
    _analyze_duedate_past:bool = False # 期日超過
    _analyze_manhour_delayed:bool = False # 工数超過
    # Calculate Data
    _totaol_days:int = 0 # 総作業日数
    _spent_days:int = 0 # 当日作業日数
    _expect_estimated_hours:float = 0 # 予測必要工数
    _expect_spent_hours:float = 0 # 予測実績工数
    _expect_remain_hours:float = 0 # 予測残工数

    #
    # コンストラクタ/デストラクタ
    #
    def __init__(self):
        """コンストラクタ
        """
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
        # 終了
        el_ended = SubElement(element, "status_ended")
        el_ended.set("name", r'終了')
        # 作業中
        el_ongoing = SubElement(element, "status_ongoing")
        el_ongoing.set("name", r'作業中')
        # 未着手
        el_notyet = SubElement(element, "status_notyet")
        el_notyet.set("name", r'未着手')
        # 保留
        el_onhold = SubElement(element, "status_ohold")
        el_onhold.set("name", r'保留')
        # 却下
        el_reject = SubElement(element, "status_reject")
        el_reject.set("name", r'却下')

        # 担当未割当
        el_notassigned = SubElement(element, "status_notassigned")
        el_notassigned.set("name", r'担当者未割当')
        # 日程未計画
        el_unplaned = SubElement(element, "status_unplaned")
        el_unplaned.set("name", r'日程未計画')
        # 開始遅延
        el_startdate_delayed = SubElement(element, "status_startdate_delayed")
        el_startdate_delayed.set("name", r'開始遅延')
        # 期日超過
        el_duedate_past = SubElement(element, "status_duedate_past")
        el_duedate_past.set("name", r'期日超過')
        # 工数遅延
        el_manhour_delayed = SubElement(element, "status_manhour_delayed")
        el_manhour_delayed.set("name", r'工数遅延')

        # bac
        el_bac = SubElement(element, "bac")
        el_bac.set("name", r'BAC(完成時総予算)')
        # pv
        el_pv = SubElement(element, "pv")
        el_pv.set("name", r'PV(出来高計画値)')
        # ev
        el_ev = SubElement(element, "ev")
        el_ev.set("name", r'EV(出来高実績値)')
        # ac
        el_ac= SubElement(element, "ac")
        el_ac.set("name", r'AC(コスト実績値)')
        # sv
        el_sv= SubElement(element, "sv")
        el_sv.set("name", r'SV(スケジュール差異)')
        # cv
        el_cv= SubElement(element, "cv")
        el_cv.set("name", r'CV(コスト差異)')
        # spi
        el_spi= SubElement(element, "spi")
        el_spi.set("name", r'SPI(スケジュール効率指数)')
        # cpi
        el_cpi= SubElement(element, "cpi")
        el_cpi.set("name", r'CPI(コスト効率指数)')
        # etc
        el_etc= SubElement(element, "etc")
        el_etc.set("name", r'ETC(残コスト予測)')
        # eac
        el_eac= SubElement(element, "eac")
        el_eac.set("name", r'EAC(完成時コスト予測)')
        # vac
        el_vac= SubElement(element, "vac")
        el_vac.set("name", r'VAC(完成時コスト差異)')
    
    def set_body(self, element: Element, issue, dict, date, calendar):
        """Body(Data)の設定

        Args:
            element (Element): BodyのNode Element
            issue : redmine.issues
            dict : redmine.issueの親チケット情報
            date : 基準日(データ取得日の前日)
            calendar : 休日情報
        """
        # パラメータを設定
        self._as_of_date = date
        self.calendar = calendar
        # Issueの情報を取得
        self._get_issue_data(issue)
        # Issueの情報を分析
        self._analyze_status(issue) # ステータス分類
        self._calculate_progress_data(issue) # 進捗データ計算
        self._analyze_progress(issue) # 進捗分析

        # boolデータの代替え文字列を定義
        str_true = r"〇"
        str_false = r""

        # 終了
        el_ended = SubElement(element, "status_ended")
        el_ended.text = str_true if self._status_ended else str_false
        # 作業中
        el_ongoing = SubElement(element, "status_ongoing")
        el_ongoing.text = str_true if self._status_ongoing else str_false
        # 未着手
        el_notyet = SubElement(element, "status_notyet")
        el_notyet.text = str_true if self._status_notyet else str_false
        # 保留
        el_onhold = SubElement(element, "status_ohold")
        el_onhold.text = str_true if self._status_onhold else str_false
        # 却下
        el_reject = SubElement(element, "status_reject")
        el_reject.text = str_true if self._status_reject else str_false

        # 担当未割当
        el_notassigned = SubElement(element, "status_notassigned")
        el_notassigned.text = str_true if self._analyze_notassigned else str_false
        # 日程未計画
        el_unplaned = SubElement(element, "status_unplaned")
        el_unplaned.text = str_true if self._analyze_unplaned else str_false
        # 開始遅延
        el_startdate_delayed = SubElement(element, "status_startdate_delayed")
        el_startdate_delayed.text = str_true if self._analyze_startdate_delayed else str_false
        # 期日超過
        el_duedate_past = SubElement(element, "status_duedate_past")
        el_duedate_past.text = str_true if self._analyze_duedate_past else str_false
        # 工数遅延
        el_manhour_delayed = SubElement(element, "status_manhour_delayed")
        el_manhour_delayed.text = str_true if self._analyze_manhour_delayed else str_false

        # 入力データ作成
        evm_input = CommonEVMInput(
            status_ended=self._status_ended,
            status_ongoing=self._status_ongoing,
            status_notyet=self._status_notyet,
            status_onhold=self._status_onhold,
            status_reject=self._status_reject,
            start_date=self._start_date,
            due_date=self._due_date,
            estimated_hours=self._estimated_hours,
            spent_hours=self._spent_hours,
            actual_start_date=self._actual_start_date,
            actual_due_date=self._actual_due_date,
            done_ratio=self._done_ratio
        )
        # EVM計算実行
        common_evm = CommonEVM()
        # 却下ステータスは計算対象外
        if(self._status_reject is False):
            common_evm.set_input_data(evm_input, self._as_of_date, self.calendar)
            common_evm.calculate()
        # pv
        el_bac = SubElement(element, "bac")
        el_bac.text = str(common_evm.get_bac())
        # pv
        el_pv = SubElement(element, "pv")
        el_pv.text = str(common_evm.get_pv())
        # ev
        el_ev = SubElement(element, "ev")
        el_ev.text = str(common_evm.get_ev())
        # ac
        el_ac = SubElement(element, "ac")
        el_ac.text = str(common_evm.get_ac())
        # sv
        el_sv = SubElement(element, "sv")
        el_sv.text = str(common_evm.get_sv())
        # cv
        el_cv = SubElement(element, "cv")
        el_cv.text = str(common_evm.get_cv())
        # spi
        el_spi = SubElement(element, "spi")
        el_spi.text = str(common_evm.get_spi())
        # cpi
        el_cpi = SubElement(element, "cpi")
        el_cpi.text = str(common_evm.get_cpi())
        # etc
        el_etc= SubElement(element, "etc")
        el_etc.text = str(common_evm.get_etc())
        # eac
        el_eac= SubElement(element, "eac")
        el_eac.text = str(common_evm.get_eac())
        # vac
        el_vac= SubElement(element, "vac")
        el_vac.text = str(common_evm.get_vac())

    #
    # protected method
    #
    def _get_issue_data(self, issue):
        """redmine.issueの情報取得

        Args:
            issue : redmine.issue
        """
        # 開始日
        try:
            self._start_date = datetime.strptime(str(issue.start_date if hasattr(issue,"start_date") else None),"%Y-%m-%d").date()
        except:
            self._start_date = None
        # 期日
        try:
            self._due_date = datetime.strptime(str(issue.due_date if hasattr(issue,"due_date") else None),"%Y-%m-%d").date()
        except:
            self._due_date = None
        # 実開始日
        try:
            self._actual_start_date = datetime.strptime(str(issue.actual_start_date if hasattr(issue,"actual_start_date") else None),"%Y-%m-%d").date()
        except:
            self._actual_start_date = None
        # 実終了日
        try:
            self._actual_due_date = datetime.strptime(str(issue.actual_due_date if hasattr(issue,"actual_due_date") else None),"%Y-%m-%d").date()
        except:
            self._actual_due_date = None
        # 進捗率        
        try:
            self._done_ratio = float(issue.done_ratio)
        except:
            self._done_ratio = float(0)        
        # 予定工数
        try:
            self._estimated_hours = float(issue.total_estimated_hours) # 合計予定工数を使う
        except:
            self._estimated_hours = float(0)               
        # 作業工数
        try:
            self._spent_hours = float(issue.total_spent_hours) # 合計作業工数を使う
        except:
            self._spent_hours = float(0)
        
    def _analyze_status(self, issue):
        """ステータスの分類

        Args:
            issue : redmine.issue
        """
        status_dict = {
            '新規':'未着手',
            '担当者決定':'未着手',
            '設計中':'作業中',
            '作業中':'作業中',
            '対応中':'作業中',
            'レビュー待ち':'作業中',
            '指摘事項対応中':'作業中',
            'レビュー承認済み':'作業中',
            '内部レビュー待ち':'作業中',
            '内部指摘事項対応中':'作業中',
            '終了':'終了',
            '保留':'保留', 
            '却下':'却下' 
        }
        # ステータスを分類
        issue_status = str(issue.status)
        category_status = status_dict[issue_status] if issue_status in status_dict else '未着手'
        # ステータスのフラグを設定
        # 初期化
        self._status_notyet = False
        self._status_ongoing = False
        self._status_ended = False
        self._status_onhold = False
        self._status_reject = False
        # 分類したステータスからフラグ設定
        match category_status:
            case "未着手":
                self._status_notyet = True
            case "作業中":
                self._status_ongoing = True
            case "終了":
                self._status_ended = True
            case "保留":
                self._status_onhold = True
            case "却下":
                self._status_reject = True
            case _:
                pass

    def _analyze_progress(self, issue):
        """進捗状況の分析

        Args:
            issue : redmine.issue
        """
        self._analyze_progress_notassigned(issue) # 担当未割当
        self._analyze_progress_unplaned(issue) # 日程未計画
        self._analyze_progress_startdate_delayed(issue) # 開始遅延
        self._analyze_progress_duedate_past(issue) # 期日超過
        self._analyze_progress_manhour_delayed(issue) # 工数遅延

    def _analyze_progress_notassigned(self, issue):
        """担当未割当の判定

        Args:
            issue : redmine.issue
        """
        self._analyze_notassigned = False
        # 却下ステータスは対象外
        if(self._status_reject is True):return
        # 担当者名が空白は担当未割当
        assigned_to = str(issue.assigned_to.name if hasattr(issue,"assigned_to") else None)
        if(assigned_to is None) or (assigned_to == ""):
            self._analyze_notassigned = True
    
    def _analyze_progress_unplaned(self, issue):
        """日程未計画の判定

        Args:
            issue : redmine.issue
        """
        self._analyze_unplaned = False
        # 却下または終了ステータスは対象外
        if(self._status_ended is True) or (self._status_reject is True):return
        # 開始日または期日の未入力は日程未計画
        if(self._start_date is None) or (self._due_date is None):
            self._analyze_unplaned = True

    def _analyze_progress_startdate_delayed(self, issue):
        """開始遅延の判定

        Args:
            issue : redmine.issue
        """
        self._analyze_startdate_delayed = False
        # 却下または終了ステータスは対象外
        if(self._status_ended is True) or (self._status_reject is True):return
        # 開始日の未入力は対象外
        if(self._start_date is None):return
        # 開始日が基準日以前で、未着手ステータスまたは実開始日が未入力または作業工数がゼロ
        # →　調査作業で進捗率が出ないケースも想定して進捗率を判定しない
        if(self._start_date <= self._as_of_date) and \
          ((self._status_notyet is True) or (self._actual_start_date is None) or (self._spent_hours == 0)):
            self._analyze_startdate_delayed = True

    def _analyze_progress_duedate_past(self, issue):
        """期日超過の判定

        Args:
            issue : redmine.issue
        """
        self._analyze_duedate_past = False
        # 却下または終了ステータスは対象外
        if(self._status_ended is True) or (self._status_reject is True):return
        # 期日の未入力は対象外
        if(self._due_date is None):return
        # 期日が基準日以前で、実終了日が未入力または進捗率が100%でない
        if(self._due_date <= self._as_of_date) and \
          ((self._actual_due_date is None) or (self._done_ratio<100)):
              self._analyze_duedate_past = True

    def _analyze_progress_manhour_delayed(self, issue):
        """工数超過の判定
           前提条件：期日超過判定を事前に実行すること

        Args:
            issue : redmine.issue
        """
        self._analyze_manhour_delayed = False
        # 作業中ステータス以外は対象外
        if(self._status_ongoing is not True):return
        # 期日の未入力は対象外
        if(self._due_date is None):return
        # 期日超過は対象外
        if(self._analyze_duedate_past is True):return
        # 残工数が期日におさまらない
        if(self._expect_remain_hours > \
          (self.calendar.count_businessday(self._as_of_date+timedelta(days=1), self._due_date))*float(8)):
            self._analyze_manhour_delayed = True

    def _calculate_progress_data(self, issue):
        """作業日数と作業工数の算出

        Args:
            issue : redmine.issue
        """
        # 初期化
        self._totaol_days = 0 # 総作業日数
        self._spent_days = 0 # 当日作業日数
        self._expect_estimated_hours = 0 # 予測必要工数
        self._expect_spent_hours = 0 # 予測実績工数
        self._expect_remain_hours = 0 # 予測残工数
        # 却下ステータスは対象外
        if(self._status_reject is True): return

        # 日程計画がある場合に作業日数を計算する
        if(self._start_date is None) or (self._due_date is None):
            # 総作業日数
            self._totaol_days = 0
            # 当日作業日数
            self._spent_days = 0
        else:                        
            # 総作業日数
            self._totaol_days = self.calendar.count_businessday(self._start_date, self._due_date)
            # 当日作業日数
            self._spent_days = self.calendar.count_businessday(self._start_date, self._as_of_date)
        
        # 作業工数を計算する
        # 予測実績工数は作業時間そのまま
        self._expect_spent_hours = self._spent_hours
        # 終了ステータスの場合は実績になるので、予測必要工数に作業工数を設定
        if(self._status_ended is True):
            self._expect_estimated_hours = self._expect_spent_hours  
        # 作業工数がゼロまたは進捗率がゼロの場合は未着手なので、予測必要工数に予定工数を設定
        elif(self._spent_hours == 0) or (self._done_ratio == 0):
            self._expect_estimated_hours = self._estimated_hours
        # 上記以外は作業中なので進捗率から予測して、予測必要工数を設定
        else:
            self._expect_estimated_hours = \
                self._spent_hours + self._spent_hours * (100-self._done_ratio) / self._done_ratio
        # 予測残工数を設定
        self._expect_remain_hours = self._expect_estimated_hours - self._expect_spent_hours

