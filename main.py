import json
import TkEasyGUI as eg
from datetime import datetime, timedelta

def main():
    """献立作成ツール - TkEasyGUI版"""
    
    # 初期データ設定
    today = datetime.today().strftime("%Y-%m-%d")
    rows = 7
    columns = ["朝食", "昼食A", "昼食B", "夕食"]
    
    # レイアウト定義
    layout = [
        # 開始日入力行
        [
            eg.Text("週の開始日 (YYYY-MM-DD):"),
            eg.Input(today, key="start_date", size=(12, 1)),
            eg.Button("JSON作成", key="create_json")
        ],
        [eg.HSeparator()],
        
        # ヘッダー行
        [eg.Text("日付", size=(8, 1))] + [eg.Text(col, size=(15, 1)) for col in columns],
        
        # 入力行（7日分）
        *[
            [eg.Text(f"Day {i+1}", size=(8, 1))] + 
            [eg.Input("", key=f"day{i}_{j}", size=(15, 1)) for j in range(len(columns))]
            for i in range(rows)
        ]
    ]
    
    # ウィンドウ作成とイベントループ
    window = eg.Window("献立作成ツール", layout)
    
    while True:
        event, values = window.read()
        
        if event in [eg.WIN_CLOSED, None]:
            break
        elif event == "create_json":
            if create_json_file(values, rows):
                eg.popup("完了", "menu.json を作成しました！")
    
    window.close()

def create_json_file(values, rows):
    """JSONファイルを作成"""
    try:
        start_date_str = values["start_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        meals_list = []
        
        for i in range(rows):
            day_date = start_date + timedelta(days=i)
            
            # 各日の献立データ作成
            day_data = {
                "date": str(day_date),
                "breakfast": {
                    "menu": values.get(f"day{i}_0", ""),
                    "start_time": "07:00",
                    "end_time": "08:00",
                    "location": "寮食堂"
                },
                "lunch": {
                    "A": {
                        "menu": values.get(f"day{i}_1", ""),
                        "start_time": "12:00",
                        "end_time": "13:00",
                        "location": "寮食堂"
                    },
                    "B": {
                        "menu": values.get(f"day{i}_2", ""),
                        "start_time": "12:00",
                        "end_time": "13:00",
                        "location": "寮食堂"
                    }
                },
                "dinner": {
                    "menu": values.get(f"day{i}_3", ""),
                    "start_time": "18:00",
                    "end_time": "19:00",
                    "location": "寮食堂"
                }
            }
            meals_list.append(day_data)
        
        # JSON出力
        data = {"week_start": start_date_str, "meals": meals_list}
        with open("menu.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
            
    except ValueError as e:
        eg.popup_error("エラー", f"日付形式が正しくありません: {e}")
        return False
    except Exception as e:
        eg.popup_error("エラー", f"JSONファイル作成に失敗しました: {e}")
        return False

if __name__ == "__main__":
    main()
