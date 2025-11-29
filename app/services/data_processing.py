import pandas as pd
from io import BytesIO
from fastapi import UploadFile


class DataService:
    @staticmethod
    async def parse_excel(file: UploadFile) -> list[dict]:
        """读取上传的 Excel 并转为字典列表"""
        contents = await file.read()
        # 使用 pandas 读取二进制流
        df = pd.read_excel(BytesIO(contents))

        # 数据清洗：填充空值，转为字典
        df = df.fillna("")
        return df.to_dict(orient="records")

    @staticmethod
    def export_excel(data: list[dict]) -> BytesIO:
        """将字典列表导出为 Excel 二进制流"""
        df = pd.DataFrame(data)
        output = BytesIO()

        # 写入 Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        output.seek(0)
        return output