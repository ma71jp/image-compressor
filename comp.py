import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import io
import os


def compress_image(input_path, quality=75):
    try:
        with Image.open(input_path) as img:
            format = img.format  # 元のフォーマットを保持

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output_io = io.BytesIO()

            # JPEG以外の形式にも対応
            save_kwargs = {}
            if format == "JPEG":
                save_kwargs = {'quality': quality, 'optimize': True}
            elif format == "PNG":
                save_kwargs = {'optimize': True, 'compress_level': 9}
            elif format == "WEBP":
                save_kwargs = {'quality': quality}
            else:
                format = "JPEG"  # その他形式はJPEGとして保存
                save_kwargs = {'quality': quality, 'optimize': True}

            img.save(output_io, format=format, **save_kwargs)
            return output_io.getvalue(), format
    except Exception as e:
        messagebox.showerror("エラー", f"画像の圧縮中にエラーが発生しました:\n{e}")
        return None, None


def select_and_compress():
    file_path = filedialog.askopenfilename(
        filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
    )

    if not file_path:
        return

    compressed_data, fmt = compress_image(file_path, quality=70)

    if compressed_data:
        original_size = os.path.getsize(file_path)
        compressed_size = len(compressed_data)

        size_info = f"元のサイズ: {original_size // 1024} KB\n圧縮後のサイズ: {compressed_size // 1024} KB\n形式: {fmt}"
        messagebox.showinfo("圧縮完了", size_info)


def create_gui():
    root = tk.Tk()
    root.title("画像圧縮ツール")
    root.geometry("300x150")
    root.resizable(False, False)

    label = tk.Label(root, text="画像ファイルを選択して圧縮")
    label.pack(pady=20)

    compress_btn = tk.Button(root, text="画像を選択して圧縮", command=select_and_compress)
    compress_btn.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
