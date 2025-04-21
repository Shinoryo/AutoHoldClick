import threading
import tkinter as tk
import json
import atexit
from pynput import keyboard, mouse

# --- グローバル変数 ---
mouse_controller = mouse.Controller()
clicking = False
notification_window = None
toggle_key = keyboard.Key.f6  # デフォルト
show_notification_flag = True
mouse_button = mouse.Button.left  # デフォルトは左クリック

# --- 設定ファイル読み込み ---
def load_config():
    global toggle_key, show_notification_flag, mouse_button
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

            # キー設定
            key_name = config.get("toggle_key", "f6").lower()
            toggle_key = getattr(keyboard.Key, key_name, keyboard.Key.f6)

            # 通知フラグ設定
            show_notification_flag = config.get("show_notification", True)

            # マウスボタン設定
            button = config.get("mouse_button", "left").lower()
            if button == "right":
                mouse_button = mouse.Button.right
            else:
                mouse_button = mouse.Button.left

            print(f"[設定] トグルキー：{toggle_key}")
            print(f"[設定] 通知表示：{show_notification_flag}")
            print(f"[設定] マウスボタン：{mouse_button}")

    except Exception as e:
        print(f"[設定エラー] {e}。デフォルト設定を使用します。")

# --- GUI通知表示 ---
def show_notification():
    global notification_window
    notification_window = tk.Tk()
    notification_window.title("通知")
    notification_window.attributes('-topmost', True)
    notification_window.geometry("200x50+1700+950")  # 右下（適宜調整）
    notification_window.overrideredirect(True)
    notification_window.attributes('-alpha', 0.85)
    label = tk.Label(notification_window, text="🖱️ クリック中！", bg="red", fg="white", font=("Arial", 14))
    label.pack(expand=True, fill="both")
    notification_window.mainloop()

def close_notification():
    global notification_window
    if notification_window:
        notification_window.destroy()
        notification_window = None

# --- トグル処理 ---
def toggle_click():
    global clicking
    if not clicking:
        mouse_controller.press(mouse_button)
        clicking = True
        print(f"[{mouse_button.name}クリック開始]")
        if show_notification_flag:
            threading.Thread(target=show_notification, daemon=True).start()
    else:
        mouse_controller.release(mouse_button)
        clicking = False
        print(f"[{mouse_button.name}クリック解除]")
        if show_notification_flag:
            close_notification()

# --- キー押下イベント処理 ---
def on_press(key):
    if key == toggle_key:
        toggle_click()

# --- 終了時にクリックを解除する関数 ---
def release_click():
    global clicking
    if clicking:
        mouse_controller.release(mouse_button)
        clicking = False
        print(f"[{mouse_button.name}クリック解除] (atexitで実行)")

# --- メイン関数 ---
def main():
    load_config()
    print("トグルキーでクリックON/OFFします（Ctrl+Cで終了）")
    
    # 終了時にクリック解除を実行する
    atexit.register(release_click)
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        listener.join()
    except KeyboardInterrupt:
        print("\n[終了要求] Ctrl+C を検出")
    finally:
        # 万が一のため、終了時にクリックを解除
        release_click()
        close_notification()

if __name__ == "__main__":
    main()
