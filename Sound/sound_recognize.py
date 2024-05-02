import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import librosa
import csv

# 加载预训练模型
model = hub.load('https://tfhub.dev/google/yamnet/1')

# 加载YAMNet类别标签
def load_yamnet_classes(csv_path='yamnet_class_map.csv'):
    class_map = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue  # Skip header if there is one
            class_map[int(row[0])] = row[2]  # Assuming the format is: index, display_name, class_name
    return class_map

# 加载类别标签
class_names = load_yamnet_classes()

def predict_sound(file_path, class_names):
    # 加载音频文件，确保采样率为16kHz
    waveform, sample_rate = librosa.load(file_path, sr=16000)
    # 如果音频文件是立体声，取均值转为单声道
    if waveform.ndim > 1:
        waveform = np.mean(waveform, axis=1)
    # 确保传递的波形是适合模型的格式
    waveform = tf.convert_to_tensor(waveform, dtype=tf.float32)
    scores, embeddings, spectrogram = model(waveform)
    # 使用softmax函数处理模型的输出得到概率分布
    scores = tf.nn.softmax(scores).numpy()
    # 获取概率最高的预测结果
    predicted_label_index = np.argmax(scores)
    # 检查索引是否在有效范围内
    if predicted_label_index in class_names:
        predicted_label = class_names[predicted_label_index]
    else:
        predicted_label = f'Unknown index: {predicted_label_index}'
    return predicted_label

# 使用文件路径
file_path = 'clearing-throat.wav'
predicted_sound = predict_sound(file_path, class_names)
print(f"The sound is predicted as: {predicted_sound}")













