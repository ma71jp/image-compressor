# image_compressor_app.py
import streamlit as st
from PIL import Image
import io

st.title("画像圧縮ツール（保存なし・解像度維持）")
st.markdown("""
画像をアップロードすると、圧縮後のファイルサイズを表示します。
JPEG、PNG、BMP、TIFF、WebP に対応。
""")

uploaded_file = st.file_uploader("画像ファイルを選択してください", type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"])

if uploaded_file:
    quality = st.slider("圧縮品質（JPEG/WebP用）", 10, 95, 70)

    try:
        image = Image.open(uploaded_file)
        format = image.format or "JPEG"

        # RGBAやPをRGBに変換（JPEGなどで透明度が扱えないため）
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        original_size_kb = len(uploaded_file.getvalue()) // 1024

        output = io.BytesIO()

        save_kwargs = {}
        if format.upper() in ["JPEG", "JPG"]:
            save_kwargs = {'quality': quality, 'optimize': True}
        elif format.upper() == "PNG":
            save_kwargs = {'optimize': True, 'compress_level': 9}
        elif format.upper() == "WEBP":
            save_kwargs = {'quality': quality}

        image.save(output, format=format, **save_kwargs)
        output_size_kb = output.tell() // 1024

        st.image(image, caption="圧縮プレビュー", use_column_width=True)
        st.success(f"✅ 圧縮完了: {original_size_kb}KB → {output_size_kb}KB")
    except Exception as e:
        st.error(f"⚠ 圧縮エラー: {e}")
