import time
import csv
from turtle import mode
from ollama import Client
import matplotlib.pyplot as plt  # 新增导入
from matplotlib import rcParams
import os
from datetime import datetime

def generate_input_text(length):
    """生成更接近真实场景的多样化文本"""
    topics = [
        "人工智能在医疗领域的应用前景",
        "气候变化对经济的全球影响分析",
        "量子计算技术的最新研究进展",
        "区块链技术在金融行业的创新应用",
        "5G网络如何改变物联网发展格局",
        "深度学习模型优化方法比较",
        "自动驾驶汽车的安全挑战与解决方案",
        "元宇宙概念下的虚拟现实技术发展",
        "大数据分析在企业决策中的作用",
        "可再生能源技术的现状与未来"
    ]
    
    sentences = [
        "近年来，{topic}已经成为了学术界和工业界的热门研究方向。",
        "关于{topic}，专家们提出了多种不同的理论框架和实践方法。",
        "表明为，{topic}将对未来社会发展产生深远影响。",
        "在{topic}方面，最新的技术突破包括以下几个方面：",
        "针对{topic}，我们可以从多个角度进行分析和探讨。"
    ]
    
    text = ""
    while len(text) < length:
        topic = topics[len(text) % len(topics)]
        sentence = sentences[len(text) % len(sentences)].format(topic=topic)
        text += sentence
        
    return text[:length]

def generate_input_text_static(length):
    """静态重复的文本"""
    text = "这是一个重复的文本片段，用于测试模型的输入长度对响应时间的影响。"
    return text * (length // len(text) + 1)

def test_model_performance():
    client = Client(host='http://localhost:11434')
    # model_name = "qwen2.5:14b"
    # model_name = "yasserrmd/Qwen2.5-7B-Instruct-1M"
    model_name = "qwen2.5:7b"
    # model_name = "llama3.2:latest"
    # / -> _, : -> _
    model_name_fn = model_name.replace('/', '_').replace(':', '_')
    min_length = 10  # 最小输入长度
    max_length = 150000  # 最大输入长度
    test_points = 10
    fixed_output_length = 10
    
    # 生成指数级增长的测试点
    test_lengths = [int(min_length * (max_length/min_length)**(i/(test_points-1))) 
                   for i in range(test_points)]
    
    results = []
    
    for length in test_lengths:
        input_text = generate_input_text_static(length)
        
        print(f"\n测试轮次: 输入长度={length}")
        print(f"输入片段: {input_text[:50]}...")

        # 如果是第一轮，先执行一次预热
        if length == test_lengths[0]:
            print("执行预热轮次...")
            client.generate(
                model=model_name,
                prompt=input_text,
                options={'num_predict': fixed_output_length}
            )
        
        start_time = time.time()
        response = client.generate(
            model=model_name,
            prompt=input_text,
            options={'num_predict': fixed_output_length}
        )
        elapsed_time = time.time() - start_time
        
        output_text = response['response']
        print(f"输出片段: {output_text[:50]}...")
        
        results.append({
            'input_length': length,
            'response_time': elapsed_time,
            'output_length': len(output_text)
        })
        
        print(f"耗时: {elapsed_time:.2f}s")
        
        print(f"测试完成: 输入长度={length}, 输出长度={len(output_text)} 耗时={elapsed_time:.2f}s")
    
    # 创建output目录
    os.makedirs('output', exist_ok=True)
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%m%d-%H%M")
    csv_filename = f"output/perf_results_{timestamp}.csv"
    plot_filename = f"output/{model_name_fn}_performance_plot_{timestamp}.png"
    
    # 保存结果到CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['input_length', 'response_time', 'output_length'])
        writer.writeheader()
        writer.writerows(results)
    
    # 新增绘图代码
    plt.rcParams['font.sans-serif'] = ['Songti SC']  # 设置支持中文的字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    plt.figure(figsize=(12, 6))
    plt.plot([r['input_length'] for r in results], 
             [r['response_time'] for r in results], 
             'bo-', label='响应时间')
    
    # 在每个数据点上添加x轴数值标签（增大字体并调整位置）
    for r in results:
        plt.text(r['input_length'], r['response_time'] * 1.1,  # 在y轴方向上增加10%距离
                 f"{r['input_length']}", 
                 ha='center', va='bottom', fontsize=10,  # 增大字体到10
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))  # 添加白色背景
    
    plt.xscale('log')
    plt.xlabel('输入长度(log scale)')
    plt.ylabel('响应时间(秒)')
    plt.title(f'{model_name}模型输入长度与响应时间关系')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig(plot_filename)
    print(f"已生成性能图表: {plot_filename}")

def main():
    print("开始测试模型性能...")
    test_model_performance()
    print("测试完成，结果已保存到perf_results.csv和performance_plot.png")  # 更新提示信息

if __name__ == "__main__":
    main()
