import streamlit as st
import networkx as nx

st.title('Proje Zamanlama ve Optimizasyon')

st.header('Görevleri Girin:')

if "tasks" not in st.session_state:
    st.session_state.tasks = {}

num_tasks = st.number_input('Kaç görev gireceksiniz?', min_value=1, max_value=10, step=1)

for i in range(int(num_tasks)):
    st.write(f"### Görev {i+1}")
    task_name = st.text_input(f"Task {i+1} Adı", key=f"task_{i}")
    task_duration = st.number_input(f"Süresi (gün)", min_value=1, key=f"duration_{i}")
    task_cost = st.number_input(f"Maliyeti ($)", min_value=1, key=f"cost_{i}")
    dependencies = st.text_input(
        f"Bağımlılıklar (Virgülle ayırın, örn: Task2, Task3)", key=f"deps_{i}"
    )

    if task_name and task_duration > 0 and task_cost > 0:
        dependencies_list = [dep.strip() for dep in dependencies.split(',')] if dependencies else []
        st.session_state.tasks[task_name] = {
            "duration": int(task_duration),
            "cost": int(task_cost),
            "dependencies": dependencies_list
        }
    else:
        st.write(f"[DEBUG] Task {i+1} verileri geçerli değil!")

# Optimize Et butonu
if st.button('Optimize Et'):
    st.write("### Projenin sıralaması")

    def project_scheduling(tasks):
        G = nx.DiGraph()

        for task in tasks:
            G.add_node(task)

        for task, info in tasks.items():
            for dep in info['dependencies']:
                if dep in tasks:
                    G.add_edge(dep, task)

        try:
            sorted_tasks = list(nx.topological_sort(G))
            st.write(f"Projenin sıralaması: {sorted_tasks}")

            total_cost = sum(tasks[task]['cost'] for task in sorted_tasks)
            st.write(f"Toplam maliyet: ${total_cost}")

        except nx.NetworkXUnfeasible:
            st.write("Bağımlılık grafiği döngü içeriyor, sıralama yapılamıyor.")

    valid_tasks = {k: v for k, v in st.session_state.tasks.items() if k}
    project_scheduling(valid_tasks)