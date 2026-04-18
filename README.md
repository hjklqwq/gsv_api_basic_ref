# GPT-SoVITS API Basic Reference  
面向新手的GPT-SoVITS API参考，仍在更新中，尚未全部完成
## 写在前面  
> 本参考文档面向纯新手，内容有限，各位大佬请移步其它教程。  

以防你不知道，其实GPT-SoVITS提供了API接口供其它程序调用。具体而言，就是根目录下的api.py。    
什么？你说GPT-SoVITS是啥？它是一个低成本音色克隆软件，具体可以看花儿不哭大佬的<a href="https://www.bilibili.com/video/BV12g4y1m7Uw/">这期视频</a>。<a href="https://github.com/RVC-Boss/GPT-SoVITS/releases">软件下载</a>  
我们只需用/runtime/python.exe启动api.py即可启动API。为了方便，可以仿照go-webui.bat写出go-api.bat。   
```bat
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
cd /d "%SCRIPT_DIR%"
set "PATH=%SCRIPT_DIR%\runtime;%PATH%"
runtime\python.exe -I api.py 
pause
```
出现提示INFO:Uvicorn running on http://0.0.0.0:9880 代表API服务已经启动了。第一次启动需要安装<a href="https://aka.ms/vc14/vc_redist.x64.exe">vc运行库。</a>   
GPT-SoVITS的API通过HTTP传输数据，只需要向 http://127.0.0.1:9880 发送请求即可。  
## API用法  
0. 官方教程和工具  
确保API启动后，访问http://127.0.0.1:9880/docs 即可获得API用法（英文）和链接构造测试一条龙服务，可以作为参考和测试工具。  
1. 设置模型  
想必各位应该是训练了模型再来找API用法的吧。假如你没有训练模型，可以忽略此步（让GPT-SoVITS直接推模型，效果较差），或移步文章开头的<a href="https://www.bilibili.com/video/BV12g4y1m7Uw/">这期视频</a>。  
用法如下：
```url
http://127.0.0.1:9880/set_model?gpt_model_path={GPT_dir}&sovits_model_path={SOVITS_dir}
```
向这个地址发送GET请求，将{GPT_dir}和{SOVITS_dir}换成你的GPT模型（* .ckpt）和SoVITS模型（* .pth）的绝对路径（不建议用反斜杠，不建议带中文）（模型文件默认保存在/GPT_weights_模型版本/ 和 /SoVITS_weights_模型版本/）。如果成功，会返回：
```
Status Code: 200
Response: {"code":0,"message":"Success"}
```
示例代码：（使用了model_config.ini）  
model_config.ini：  
```config
[DEFAULT]
GPT_dir=D:/ABS/PATH/TO/FILE.ckpt
SOVITS_dir=D:/ABS/PATH/TO/FILE.pth
```
需要安装Requests库  
```pip
pip install requests
```
Python：  
``` python
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
```
撒花！  
2. TTS  
终于到了最重要的部分。用法如下：
```url
http://127.0.0.1:9880/?refer_wav_path={refer_wav}&prompt_text={prompt_text}&prompt_language={prompt_language}&text={text}&text_language={text_language}&cut_punc={cut_punc}&top_k=15&top_p=1&temperature=1&speed=1&sample_steps=32&if_sr=false
```
其中：  
refer_wav_path=主参考音频绝对路径  
prompt_text=主参考音频文本  
prompt_language=主参考音频语言（中文、英文等，详见webui中的选项）  
text=要合成的文本  
text_language=合成文本语言  
cut_punc=切分方式（例如0.不切，详见webui中的选项）  
其余参数在webui推理界面均有介绍，一般保持默认即可。  
如果成功，返回一段wav音频。  
示例代码：  
tts_config.ini
```config
[DEFAULT]
prompt_text = 请输入文本
refer_wav = D:/ABS/PATH/TO/FILE.wav
cut_punc = 0.不切
prompt_language = 中文
```
需要安装Requests和Pygame-ce（在较高Python版本，如3.14.0，可能无法安装Pygame，可以用Pygame-ce替代）
```pip
pip install requests
pip install pygame-ce
```
Python（tts.py）：
```python
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
```
（代码使用QWEN-coder生成，人工修改）  
用法：
```bash
python tts.py -text 要合成的文本 -language 语言
```
撒花！  
（如果要使用pyinstaller打包的话，可能会出现config路径问题，请自行修改）  
那么最基础的API用法已经实现了，剩下的请各位发挥创意自行探索。
