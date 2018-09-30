import xlrd
import pymysql
from datetime import datetime
from xlrd import xldate_as_tuple
#打开数据所在的工作簿，以及选择存有数据的工作表
book = xlrd.open_workbook("../data/beijing.xls")
book.sheet_names()        # 获取xls文件中所有sheet的名称
sheet = book.sheets()[0]  # 获取xls文件第一个工作表
#sheet = book.sheet_by_name("@beijing")
#建立一个MySQL连接
conn = pymysql.connect(
        host='127.0.0.1',
        user='root', 
        passwd='123.com',
        db='testdata',
        port=3306,  
        charset='utf8'
        )
# 获得游标
cur = conn.cursor()
# 创建插入SQL语句
sql = 'insert into air_data (date,quality_grade, AQI, AQI_ranking, PM25, PM10, So2, No2, Co, O3) values (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)'
# 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
for r in range(1, sheet.nrows):
      # 转成datetime对象
      date1 = sheet.cell(r, 0).value
      date = datetime(*xldate_as_tuple(date1, 0))
      quality_grade = sheet.cell(r,1).value
      AQI = sheet.cell(r,2).value
      AQI_ranking = sheet.cell(r,3).value
      PM25 = sheet.cell(r,4).value
      PM10  = sheet.cell(r,5).value
      So2 = sheet.cell(r,6).value
      No2 = sheet.cell(r, 7).value
      Co = sheet.cell(r, 8).value
      O3 = sheet.cell(r, 9).value
      values = (date, quality_grade
                , AQI, AQI_ranking, PM25, PM10, So2, No2, Co, O3)
      # 执行sql语句
      cur.execute(sql, values)
cur.close()
conn.commit()
conn.close()
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print ("导入 " +columns + " 列 " + rows + " 行数据到MySQL数据库!")
