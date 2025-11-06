from modules.performance_analysis import run_performance_analysis
from modules.task_solutions import demonstrate_solutions
from modules.plot_generator import generate_all_plots

def main():
    """Основная функция приложения"""
    print("Лабораторная работа 2: Анализ структур данных")
    print("=" * 50)
    
    # Запуск анализа производительности
    print("Запуск анализа производительности...")
    insertion_data, queue_data = run_performance_analysis()
    
    # Генерация графиков
    print("\nГенерация графиков...")
    generate_all_plots(insertion_data, queue_data)
    
    # Демонстрация решений задач
    print("\nДемонстрация решений задач...")
    demonstrate_solutions()
    
    print("\n" + "=" * 50)
    print("Все задачи выполнены успешно!")
    print("Результаты сохранены в папке 'lab2/report/'")

if __name__ == "__main__":
    main()