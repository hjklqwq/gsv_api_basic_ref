import configparser
import requests

def main():
    # 创建配置文件解析器
    config = configparser.ConfigParser()

    # 读取同目录下的 model_config.ini 文件
    config.read('model_config.ini')

    # 获取 GPT_dir 和 SOVITS_dir 字段的值
    GPT_dir = config.get('DEFAULT', 'GPT_dir')
    SOVITS_dir = config.get('DEFAULT', 'SOVITS_dir')

    # 构造请求 URL
    url = f"http://127.0.0.1:9880/set_model?gpt_model_path={GPT_dir}&sovits_model_path={SOVITS_dir}"
    print(url)
    # 发送 HTTP GET 请求
    response = requests.get(url)

    # 输出响应状态码和内容（可选）
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
