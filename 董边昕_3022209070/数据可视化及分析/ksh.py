import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei' 是黑体的字体名
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 指定CSV文件路径
input_file_path = "F:\\Python1\\PaChongJD\\.venv\\huaweimatex5_comments.csv"

# 读取CSV文件
df = pd.read_csv(input_file_path)

# 确保“评论地点”列不包含NaN值
df['评论地点'] = df['评论地点'].fillna('未知')

# 统计不同评论地点的数量
location_counts = df['评论地点'].value_counts()

# 绘制柱状图
plt.figure(figsize=(10, 8))  # 设置图形大小
location_counts.plot(kind='bar')  # 绘制柱状图
plt.title('不同评论地点的数量')  # 设置图形标题
plt.xlabel('评论地点')  # 设置x轴标签
plt.ylabel('数量')  # 设置y轴标签
plt.xticks(rotation=45)  # 旋转x轴标签，以便更好地显示
plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域

# 显示图形
plt.show()