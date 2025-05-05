import json
import atexit
import time
from pynput import keyboard, mouse

# --- グローバル変数 ---
mouse_controller = mouse.Controller()
clicking = False
notification_window = None
toggle_key = keyboard.Key.f6  # デフォルト
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

            # マウスボタン設定
            button = config.get("mouse_button", "left").lower()
            if button == "right":
                mouse_button = mouse.Button.right
            else:
                mouse_button = mouse.Button.left

            print(f"[設定] トグルキー：{toggle_key}")
            print(f"[設定] マウスボタン：{mouse_button}")

    except Exception as e:
        print(f"[設定エラー] {e}。デフォルト設定を使用します。")

# --- トグル処理 ---
def toggle_click():
    global clicking
    if not clicking:
        mouse_controller.press(mouse_button)
        clicking = True
        print(f"[{mouse_button.name}クリック開始]")
    else:
        mouse_controller.release(mouse_button)
        clicking = False
        print(f"[{mouse_button.name}クリック解除]")

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

# --- メイン関数 ---
def main():
    load_config()
    print("トグルキーでクリックON/OFFします（Ctrl+Cで終了）")
    
    # 終了時にクリック解除を実行する
    atexit.register(release_click)
    
    with keyboard.Listener(on_press=on_press):
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[終了] Ctrl+C が押されました")
            release_click()

if __name__ == "__main__":
    main()
