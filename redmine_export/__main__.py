from custom import RedmineExport
from custom import RedmineAnalyze
from custom import RedmineAccessor
from bteam_utils import CommonCalendar, CommonXML 
import configparser
import argparse
import os
import sys
import glob
import pathlib
import shutil
from datetime import datetime, timedelta
import pandas as pd
from xml.etree.ElementTree import Element, SubElement


def main():
    """Main処理
    """
    progress:int = 0
    # argument取得
    parser = argparse.ArgumentParser()
    parser.add_argument('project_name', type=str, help='プロジェクト名。')
    parser.add_argument('--output_path', type=str, default='', help='出力先フォルダパス(デフォルト:./output/プロジェクト名)')
    parser.add_argument('--holiday', type=str, default='./holiday/*.csv', help='祝日ファイルのパス(デフォルト:./holiday/*.csv)')
    parser.add_argument('--config', type=str, default='./inifile/config.ini', help='configファイルのパス. デフォルト:./inifile/config.ini')
    parser.add_argument('--redmine_key', type=str, default='./inifile/.redmine_key', help='redmine_keyファイルのパス. デフォルト:./inifile/.redmine_key')  
    # プロジェクト名と出力先パスの設定
    args = parser.parse_args()
    project_name = args.project_name
    output_path = args.output_path if args.output_path else os.path.join(os.getcwd(), 'output', project_name)

    # プログレス表示
    progress = 0
    show_progress(progress, project_name, '初期化中...')
    # 出力先フォルダ作成
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # config取得
    config = configparser.ConfigParser()
    try:
        config.read(args.config, encoding='utf-8')
        its_url = config.get('ITS','URL')
    except Exception as e:
        print('config file error.')
        sys.exit()
    # RedmineのURLをチェック
    if its_url == '':
        print('URL missing error.')
        sys.exit()
    # RedmineのAPI-KEYを取得
    if os.path.exists(args.redmine_key):
        # ファイルが存在する場合はファイルから読み込み
        with open(args.redmine_key, 'r', encoding='utf-8') as f:
            its_key = f.read().strip()
            if its_key == '':
                print('Redmine API-KEY missing error.')
                sys.exit()
    else:
        # ファイルが存在しない場合はユーザ入力から取得
        its_key = input('Redmine API-KEY:').strip()
        if its_key == '':
            print('Redmine API-KEY missing error.')
            sys.exit()
        else:
            # ファイルに保存
            with open(args.redmine_key, 'w', encoding='utf-8') as f:
                f.write(its_key)
    # 休日リストの取得
    holidaylist = list()
    files = glob.glob(args.holiday)
    for file in files:
        holidaylist = holidaylist + pd.read_csv(file, header=None).values.tolist()
    # Commcalendarの生成
    if len(holidaylist) > 0:
        holidaylist = pd.DataFrame(holidaylist).T.values.tolist()
        temp_list = [pd.to_datetime(d).date() for d in holidaylist[0]]
        i_calendar = CommonCalendar(temp_list)
    else:
        i_calendar = CommonCalendar()
    # 基準日を取得
    base_date = datetime.now().date() + timedelta(days=-1)

    # プログレス表示
    progress += 10
    show_progress(progress, project_name, 'Redmineデータ取得中...')
    # RedmineAccessorのインスタンス生成
    i_accessor = RedmineAccessor(project_name, its_url, its_key)
    # Issue情報を取得
    issues = i_accessor.load_issues()
    issues_num = len(issues)
    issue_update = i_accessor.latest_update()
    id_subject_dict = i_accessor.idtosubject_dict()

    # プログレス表示
    progress += 40
    show_progress(progress, project_name, 'Redmineデータ解析中...')
    # XML作成
    root = Element("root")
    # RedmineExport、redmineAnalyzeのインスタンス生成
    i_exporter = RedmineExport(i_accessor)
    i_analyzer = RedmineAnalyze(i_accessor)
    # Information設定
    i_exporter.set_information(root, project_name, issue_update) # redmineExportのInformation設定
    # Header設定
    element = SubElement(root, "header")
    i_exporter.set_header(element) # redmineExportのHeader設定
    i_analyzer.set_header(element) # redmineAnalyzeのHeader設定
    # Body設定
    for issue in issues:
        element = SubElement(root, "ticket")
        element.set("id", str(issue.id))
        i_exporter.set_body(element, issue, id_subject_dict) # redmineExportのBody設定
        i_analyzer.set_body(element, issue, id_subject_dict, base_date, i_calendar) # redmineAnalyzeのBody設定
    root.set("num", str(issues_num))

    # プログレス表示
    progress += 40
    show_progress(progress, project_name, 'ファイル出力中...')
    # CommonXMLのインスタンス生成
    i_common_xml = CommonXML()
    # XMLファイル出力
    xml_filepath = os.path.join(output_path, f'{project_name}.xml')
    i_common_xml.save_xml(root, xml_filepath)
    # csvファイル出力
    outfile_name = pathlib.Path(xml_filepath).with_suffix('.csv')
    i_common_xml.save_csv(root, str(outfile_name), 'header', 'ticket')

    # プログレス表示
    progress = 100
    show_progress(progress, project_name, '完了しました。')

def show_progress(ratio: int, task: str = "", status: str = ""):
    """進捗表示
    Args:
        ratio (int): 進捗率 (0-100)
        task (str): 現在のタスク名
        status (str): 現在の状態メッセージ
    """
    block_num = 50
    ratio = min(max(ratio, 0), 100)
    int_ratio = int(ratio * (block_num / 100))
    
    bar = '[' + '#' * int_ratio + '-' * (block_num - int_ratio) + ']'
    output = f"\r{bar} {ratio:3}% | {task} : {status}"
    print(f"{output:<100}", end="", flush=True)

    if ratio >= 100:
        print()    

if __name__ == '__main__':
    main()