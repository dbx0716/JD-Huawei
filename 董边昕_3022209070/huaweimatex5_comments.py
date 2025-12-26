import requests
import json
import time
import pandas as pd

# 通过api获取数据
def start(page, productId, sortType):
    url = f'https://club.jd.com/comment/productPageComments.action?productId={productId}&score=0&sortType={sortType}&page={page}&pageSize=10&isShadowSku=0&fold=1&#39;';
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text.replace('fetchJSON_comment98(', '').replace(')', ''))
    return data

# 从return的data解析并提取信息
def parse(data):
    items = data['comments']
    for i in items:
        yield {
            '商品名称': f"{i.get('productColor', '未知颜色')} {i.get('productSize', '未知尺寸')}",
            '评论内容': i['content'],
            '评论地点': i.get('location', '未知'),
            '评论用户': i['nickname'],
            '评论用户ID': i['id'],
            '发表日期': i['creationTime'],
            '点赞数': i['usefulVoteCount']
        }


# 将数据写入CSV文件
def csv(items, file_path='huaweimatex5_commentdetails.csv'):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=['商品名称', '评论内容', '评论地点', '评论用户名', '评论用户ID', '发表日期', '点赞数'])

    # 存储数据到DataFrame
    new_df = pd.DataFrame(items)
    df = pd.concat([df, new_df], ignore_index=True)

    # 转换日期格式并按时间降序排列
    df['发表日期'] = pd.to_datetime(df['发表日期'])
    df.sort_values(by='发表日期', ascending=False, inplace=True)

    # 数据写入文件
    df.to_csv(file_path, index=False, encoding='utf-8')

    # 提取信息达到5k则退出循环
    if df.shape[0] > 5000:
        exit()


# 爬取过程主函数
def main():
    product_ids = [
        # 商品ID列表
        '10113373860114', '10088369404368', '10118391471502', '10087923467939',
        '10116649133930', '10122583315631', '10119950262980', '10115221243358',
        '10098706860634', '10115808917896', '10115808917909', '10105632271749',
        '10116647292848', '10097469402518', '10098706860645', '10107148592622',
        '10115221243368', '10122020074077', '10119950263003', '10122020074072',
        '100066168958', '10085427987172', '10085257755991', '10085387091002',
        '100099449994', '100066168990', '100094163709', '100069221844',
        '100105688600', '10088354410994', '10085430077558', '10089434051506',
        '10085437764733', '100117023841', '100067230652', '100139842854',
        '100099449996', '10089434051484', '100094112159', '10085605941406',
        '10085429761970', '10101532624261', '10088354410938', '100093812789',
        '10085446322682', '10085429925731', '100076021553', '10105632271742',
        '10098706860634', '100076021547', '100099983230', '10089434051488',
        '10111201527739', '10092334329126', '10089434051508', '100066168990',
        '10088354410968']
    total_comments = 0
    comments_needed = 100000
    sort_types = [1, 2, 3, 4, 5, 6]

    # 对不同排序的数据进行爬取并去重
    for productId in product_ids:
        for sortType in sort_types:
            total_pages = 0
            while total_comments < comments_needed:
                data = start(total_pages + 1, productId, sortType)
                if not data or not data.get('comments'):
                    break
                parsed_data = list(parse(data))
                if not parsed_data:
                    break
                csv(parsed_data)
                total_comments += len(parsed_data)
                df = pd.read_csv('huaweimatex5_commentdetails.csv')
                row_count = len(df)
                print(
                    f'商品ID：{productId}，第{total_pages + 1}页抓取完毕，已抓取评论数：{total_comments}，排序方式：{sortType}, 去重后评论数:{row_count}')
                total_pages += 1
                if total_comments >= comments_needed:
                    break
                    sleep(random.random() * 3)

if __name__ == '__main__':
    main()
