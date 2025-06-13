# image_compressor_batch.py
import streamlit as st
from PIL import Image
import io
import zipfile

st.title("画像一括圧縮ツール（最大30枚）")
st.markdown("""
複数画像を一度にアップロードして、圧縮してZIP形式でまとめてダウンロードできます。
JPEG、PNG、BMP、TIFF、WebP に対応。
""")

uploaded_files = st.file_uploader(
    "画像ファイルを選択してください（最大30枚）",
    type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 30:
        st.error("⚠ 最大30枚までアップロードできます。")
    else:
        quality = st.slider("圧縮品質（JPEG/WebP用）", 10, 95, 70)
        zip_buffer = io.BytesIO()
        total_original_kb = 0
        total_compressed_kb = 0

        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for uploaded_file in uploaded_files:
                try:
                    image = Image.open(uploaded_file)
                    format = image.format or "JPEG"
                    original_data = uploaded_file.getvalue()
                    original_size_kb = len(original_data) // 1024
                    total_original_kb += original_size_kb

                    if image.mode in ("RGBA", "P"):
                        image = image.convert("RGB")

                    output = io.BytesIO()
                    save_format = format.upper()
                    save_kwargs = {}

                    if save_format in ["JPEG", "JPG"]:
                        save_kwargs = {'quality': quality, 'optimize': True}
                    elif save_format == "PNG":
                        save_kwargs = {'optimize': True, 'compress_level': 9}
                    elif save_format == "WEBP":
                        save_kwargs = {'quality': quality}
                    elif save_format in ["TIFF", "BMP"]:
                        save_format = "JPEG"
                        save_kwargs = {'quality': quality, 'optimize': True}

                    image.save(output, format=save_format, **save_kwargs)
                    compressed_data = output.getvalue()
                    compressed_size_kb = len(compressed_data) // 1024
                    total_compressed_kb += compressed_size_kb

                    zipf.writestr(f"compressed_{uploaded_file.name}", compressed_data)

                    st.write(
                        f"🖼️ {uploaded_file.name}: {original_size_kb}KB → {compressed_size_kb}KB"
                    )
                except Exception as e:
                    st.error(f"{uploaded_file.name}: 圧縮エラー - {e}")

        zip_buffer.seek(0)
        st.success(f"✅ 圧縮完了: 合計 {total_original_kb}KB → {total_compressed_kb}KB")
        st.download_button(
            label="📦 圧縮画像（ZIP）をダウンロード",
            data=zip_buffer,
            file_name="compressed_images.zip",
            mime="application/zip"
        )
