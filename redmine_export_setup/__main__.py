import os
import sys
import shutil

def main():
    """Main処理
    """
    # テンプレート取得要求
    folder_names = ['inifile', 'holiday', 'custom']
    for folder_name in folder_names:
        output_path = os.path.join(os.getcwd(), folder_name)
        template_path = os.path.join(os.path.dirname(__file__), 'template', folder_name)                
        # 出力先が存在する場合のみ実行
        if os.path.exists(output_path):
            # フォルダ内のファイルを複写
            for file_name in os.listdir(template_path):
                src_file = os.path.join(template_path, file_name)
                dst_file = os.path.join(output_path, file_name)
                # 既に存在する場合は上書きしない
                if not os.path.exists(dst_file):
                    shutil.copyfile(src_file, dst_file)
    print('テンプレートファイルを作成しました。')
    sys.exit()

if __name__ == '__main__':
    main()