# improved_image_compressor.py
import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="画像一括圧縮ツール", layout="wide")
st.title("📷 画像一括圧縮ツール")
st.caption("※ 画像は保存されません。最大30枚、解像度そのまま。JPEG/PNG/BMP/WebP対応")

uploaded_files = st.file_uploader(
    "📁 圧縮したい画像ファイルを選んでください（複数選択可）",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 30:
        st.error("⚠ 画像は最大30枚までにしてください。")
    else:
        quality = st.slider("🔧 JPEG/WebP 圧縮品質", min_value=10, max_value=95, value=70)

        zip_buffer = io.BytesIO()
        total_original_kb = 0
        total_compressed_kb = 0

        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            cols = st.columns(3)
            for i, uploaded_file in enumerate(uploaded_files):
                with cols[i % 3]:
                    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

                original_data = uploaded_file.getvalue()
                original_size_kb = len(original_data) // 1024
                total_original_kb += original_size_kb

                try:
                    image = Image.open(io.BytesIO(original_data))
                    format = image.format or "JPEG"

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
                    st.write(f"✅ {uploaded_file.name}: {original_size_kb}KB → {compressed_size_kb}KB")
                except Exception as e:
                    st.error(f"❌ {uploaded_file.name}: 圧縮エラー - {e}")

        zip_buffer.seek(0)
        st.markdown("---")
        st.success(f"🎉 圧縮完了: 合計 {total_original_kb}KB → {total_compressed_kb}KB")

        st.download_button(
            label="📦 圧縮済みZIPファイルをダウンロード",
            data=zip_buffer,
            file_name="compressed_images.zip",
            mime="application/zip"
        )
