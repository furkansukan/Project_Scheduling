import streamlit as st
import networkx as nx

# Başlık ve açıklama
st.title('Proje Zamanlama ve Optimizasyon')

st.header('Görevleri Girin:')

# Kullanıcıdan görev sayısını alıyoruz
num_tasks = st.number_input('Kaç görev gireceksiniz?', min_value=1, max_value=10, step=1)

# Boş sözlük oluşturuyoruz (Session State kullanmıyoruz artık)
tasks = {}

for i in range(int(num_tasks)):
    st.write(f"### Görev {i+1}")

    # Görev bilgileri inputları - her input için benzersiz key oluşturuyoruz
    task_name = st.text_input(f"Task {i+1} Adı", key=f"task_name_{i}")
    task_duration = st.number_input(f"Süresi (gün)", min_value=1, key=f"task_duration_{i}")
    task_cost = st.number_input(f"Maliyeti ($)", min_value=1, key=f"task_cost_{i}")
    dependencies = st.text_input(
        f"Bağımlılıklar (Virgülle ayırın, örn: Task2, Task3)", key=f"task_deps_{i}"
    )

    # Eğer tüm bilgiler sağlanmışsa, sözlüğe ekleyelim
    if task_name and task_duration > 0 and task_cost > 0:
        dependencies_list = [dep.strip() for dep in dependencies.split(',')] if dependencies else []
        tasks[task_name] = {
            "duration": int(task_duration),
            "cost": int(task_cost),
            "dependencies": dependencies_list
        }

# Optimize Et butonu
if st.button('Optimize Et'):
    st.write("### Projenin sıralaması")

    def project_scheduling(tasks):
        G = nx.DiGraph()

        # Grafik oluşturuyoruz ve bağlılıkları ekleyiyoruz
        for task in tasks:
            G.add_node(task)

        for task, info in tasks.items():
            for dep in info['dependencies']:
                if dep in tasks:
                    G.add_edge(dep, task)

        try:
            # Bağımlılıkları sıralama işlemi
            sorted_tasks = list(nx.topological_sort(G))
            st.write(f"Projenin sıralaması: {sorted_tasks}")

            total_cost = sum(tasks[task]['cost'] for task in sorted_tasks)
            st.write(f"Toplam maliyet: ${total_cost}")

        except nx.NetworkXUnfeasible:
            st.write("Bağımlılık grafiği döngü içeriyor, sıralama yapılamıyor.")

    project_scheduling(tasks)
