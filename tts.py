import configparser
import requests
import argparse
import pygame
import io
import os
import sys

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='GSV-API-ADAPT')
    parser.add_argument('-text', required=True, help='要合成的文本')
    parser.add_argument('-language', required=True, help='文本的语言')
    args = parser.parse_args()

    text = args.text
    text_language = args.language

    # 获取配置文件路径
    config_path = "./tts_config.ini"

    # 读取配置文件
    config = configparser.ConfigParser()

    # 检查配置文件是否存在
    if os.path.exists(config_path):
        config.read(config_path, encoding='utf-8')
        print(f"成功读取配置文件: {config_path}")
    else:
        print(f"配置文件不存在: {config_path}，将使用默认值")

    # 获取配置项，如果不存在则提供默认值
    prompt_text = config.get('DEFAULT', 'prompt_text')
    refer_wav = config.get('DEFAULT', 'refer_wav')
    cut_punc = config.get('DEFAULT', 'cut_punc', fallback='0.不切')
    prompt_language = config.get('DEFAULT', 'prompt_language', fallback='中文')

    print(f"使用配置 - prompt_text: {prompt_text}")
    print(f"使用配置 - refer_wav: {refer_wav}")
    print(f"使用配置 - cut_punc: {cut_punc}")
    print(f"使用配置 - prompt_language: {prompt_language}")

    # 构造请求 URL
    url = (
        f"http://127.0.0.1:9880/?"
        f"refer_wav_path={refer_wav}&"
        f"prompt_text={prompt_text}&"
        f"prompt_language={prompt_language}&"
        f"text={text}&"
        f"text_language={text_language}&"
        f"cut_punc={cut_punc}&"
        f"top_k=15&"
        f"top_p=1&"
        f"temperature=1&"
        f"speed=1&"
        f"sample_steps=32&"
        f"if_sr=false"
    )

    try:
        # 发送 HTTP GET 请求
        response = requests.get(url)

        if response.status_code == 200:
            # 将返回的音频数据保存为临时文件
            audio_data = response.content

            # 初始化pygame mixer
            pygame.mixer.init()

            # 从字节流加载音频
            sound_buffer = io.BytesIO(audio_data)
            pygame.mixer.music.load(sound_buffer)

            # 播放音频
            pygame.mixer.music.play()

            # 等待播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
