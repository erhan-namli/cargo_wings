import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.animation import FuncAnimation

# Dronların görevlere yakınlığına göre görevleri kümelere ayıran fonksiyon
def assign_tasks_to_clusters(drones, tasks, k):
    kmeans = KMeans(n_clusters=k, random_state=0)
    clusters = kmeans.fit_predict(tasks)
    return clusters

# Her animasyon karesinde çizimi güncelleyen fonksiyon
def update(frame):
    global drones  # Dronları global olarak tanımla
    plt.clf()
    # Dronları rastgele hareket ettirme (animasyon amaçlı)
    drones += np.random.normal(0, 0.1, drones.shape)
    # Güncellenmiş dron pozisyonlarına göre görevleri kümelerine ayır
    clusters = assign_tasks_to_clusters(drones, tasks, num_clusters)
    # Güncellenmiş senaryoyu görselleştir
    plt.scatter(drones[:, 0], drones[:, 1], c='red', marker='D', label='Dronlar')
    plt.scatter(tasks[:, 0], tasks[:, 1], c=clusters, cmap='viridis', marker='o', label='Görevler')
    plt.title('Dronlar ve Görevler ile Kümeler')
    plt.xlabel('X-ekseni')
    plt.ylabel('Y-ekseni')
    plt.legend()

# Dron, görev ve küme sayıları
num_drones = 3
num_tasks = 18
num_clusters = 6

# Dron ve görev konumlarını rastgele oluştur
drones = np.random.rand(num_drones, 2) * 10  # 10x10 bir alanı varsayalım
tasks = np.random.rand(num_tasks, 2) * 10

# Çizim için bir figür ve eksen oluştur
fig, ax = plt.subplots()

# Belirli bir aralıkta (milisaniye cinsinden) ve güncelleme fonksiyonuyla bir animasyon oluştur
animation = FuncAnimation(fig, update, frames=range(100), interval=500)

# Animasyonu göster
plt.show()
