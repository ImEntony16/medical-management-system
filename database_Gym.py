from tkinter import ttk, messagebox
import tkinter as tk
import mysql.connector


try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="74970216",
        database="FITNESS_CENTER"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")
    exit()

root = tk.Tk()
root.title("Система керування фітнес-центром")
root.geometry("1200x700")
root.config(bg="#fff0e6")  # Світлий фон, ніжний персиковий відтінок

# Видалення фокусу для всіх елементів вікна
root.option_add("*TButton.highlightThickness", 0)
root.option_add("*TEntry.highlightThickness", 0)


style = ttk.Style()

style.configure("TNotebook", background="#fff0e6")
style.configure("TNotebook.Tab", font=("Comic Sans MS", 14, "bold"), padding=[15, 5], background="#ffcc99", foreground="#5a3d3a")

style.map("TNotebook.Tab",
          background=[("selected", "#ffb3b3"), ("!selected", "#ffcc99")],
          foreground=[("selected", "#5a3d3a"), ("!selected", "#5a3d3a")])

style.configure("TFrame", background="#fff0e6")


style.configure("TButton", font=("Comic Sans MS", 12), padding=10, relief="flat", background="#ff7f50", foreground="#ffffff",
                borderwidth=2, highlightthickness=0, takefocus=False, focuscolor="#ff6347")  # Видалено focuscolor, додано highlightthickness=0
style.map("TButton", background=[("active", "#ff6347")])


style.configure("TLabel", font=("Comic Sans MS", 16), background="#fff0e6", foreground="#5a3d3a")
style.configure("TEntry", font=("Comic Sans MS", 12), padding=5, relief="solid", borderwidth=2, background="#ffffff",
                foreground="#5a3d3a", highlightthickness=0, highlightbackground="none", highlightcolor="none")  # Видалено фокусні контури


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=20)


tab_client = ttk.Frame(notebook, style="TFrame")
tab_trainer = ttk.Frame(notebook, style="TFrame")
tab_membership = ttk.Frame(notebook, style="TFrame")
tab_payments = ttk.Frame(notebook, style="TFrame")


notebook.add(tab_client, text="Клієнт")
notebook.add(tab_trainer, text="Тренер")
notebook.add(tab_payments, text="Платежі")  # Вкладка "Платежі" додана після "Тренер"
notebook.add(tab_membership, text="Абонемент")


label = ttk.Label(tab_client, text="Інформація про клієнта")
label.pack(pady=20)

entry = ttk.Entry(tab_client)
entry.pack(pady=10, fill="x", padx=50)


button = ttk.Button(tab_client, text="Зберегти")
button.pack(pady=20)

# Додаткові компоненти на інших вкладках
label_trainer = ttk.Label(tab_trainer, text="Інформація про тренера")
label_trainer.pack(pady=20)

entry_trainer = ttk.Entry(tab_trainer)
entry_trainer.pack(pady=10, fill="x", padx=50)

# Кнопка на іншій вкладці з округленими кутами без білого фону
button_trainer = ttk.Button(tab_trainer, text="Зберегти")
button_trainer.pack(pady=20)

def create_trainer_interface():

    for widget in tab_trainer.winfo_children():
        widget.destroy()

    trainer_name = ttk.Entry(tab_trainer)
    trainer_name.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_trainer, text="Ім'я").grid(row=0, column=0, pady=10, padx=10)

    trainer_email = ttk.Entry(tab_trainer)
    trainer_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_trainer, text="Email").grid(row=1, column=0, pady=10, padx=10)

    trainer_phone = ttk.Entry(tab_trainer)
    trainer_phone.grid(row=2, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_trainer, text="Телефон").grid(row=2, column=0, pady=10, padx=10)

    trainer_specialty = ttk.Entry(tab_trainer)
    trainer_specialty.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_trainer, text="Спеціальність").grid(row=3, column=0, pady=10, padx=10)

    trainer_salary = ttk.Entry(tab_trainer)
    trainer_salary.grid(row=4, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_trainer, text="Зарплата").grid(row=4, column=0, pady=10, padx=10)

    def add_trainer():
        try:
            cursor.execute("""
                INSERT INTO trainers (name, email, phone, specialty, salary)
                VALUES (%s, %s, %s, %s, %s)
            """, (trainer_name.get(), trainer_email.get(), trainer_phone.get(), trainer_specialty.get(), trainer_salary.get()))
            db.commit()
            messagebox.showinfo("Успіх", "Тренера додано успішно.")
            refresh_trainer_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка", f"Помилка при додаванні тренера: {err}")

    def delete_trainer():
        trainer_id = trainer_id_entry_delete.get()  # Отримуємо ID тренера для видалення
        if not trainer_id:
            messagebox.showwarning("Помилка вводу", "Будь ласка, введіть ID тренера для видалення.")
            return

        try:
            query = "DELETE FROM trainers WHERE trainer_id = %s"
            cursor.execute(query, (trainer_id,))
            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Успіх", "Тренера видалено успішно.")
            else:
                messagebox.showwarning("Не знайдено", "Тренера з вказаним ID не знайдено.")
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка бази даних", f"Помилка при видаленні тренера: {err}")

    def refresh_trainer_data():
        for item in trainer_tree.get_children():
            trainer_tree.delete(item)
        try:
            # Вибираємо стовпці в правильному порядку
            cursor.execute("SELECT trainer_id, name, email, phone, specialty, salary FROM trainers")
            for row in cursor.fetchall():
                # Вставляємо значення в правильному порядку
                trainer_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка", f"Помилка при оновленні даних тренерів: {err}")
    control_frame_trainer = tk.Frame(tab_trainer, bg="#f4f4f9")
    control_frame_trainer.grid(row=5, column=0, columnspan=2, pady=20)

    ttk.Button(control_frame_trainer, text="Додати тренера", command=add_trainer, style="TButton").grid(row=0, column=0, padx=10, pady=10)
    ttk.Button(control_frame_trainer, text="Видалити тренера", command=delete_trainer, style="TButton").grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(control_frame_trainer, text="Оновити дані тренера", command=refresh_trainer_data, style="TButton").grid(row=0, column=2, padx=10, pady=10)

    delete_trainer_frame = tk.Frame(tab_trainer, bg="#f4f4f9")
    delete_trainer_frame.grid(row=6, column=0, columnspan=2, pady=10)

    tk.Label(delete_trainer_frame, text="ID тренера (для видалення)").grid(row=0, column=0, padx=10, pady=10)
    trainer_id_entry_delete = ttk.Entry(delete_trainer_frame, width=10)
    trainer_id_entry_delete.grid(row=0, column=1, pady=10, padx=10)

    trainer_tree = ttk.Treeview(tab_trainer, columns=("ID", "Ім'я", "Email", "Телефон", "Спеціальність", "Зарплата"), show="headings")
    trainer_tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    trainer_tree.heading("ID", text="ID")
    trainer_tree.heading("Ім'я", text="Ім'я")
    trainer_tree.heading("Email", text="Email")
    trainer_tree.heading("Телефон", text="Телефон")
    trainer_tree.heading("Спеціальність", text="Спеціальність")
    trainer_tree.heading("Зарплата", text="Зарплата")

    refresh_trainer_data()




def create_client_interface():
    for widget in tab_client.winfo_children():
        widget.destroy()


    client_name = ttk.Entry(tab_client)
    client_name.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_client, text="Ім'я").grid(row=0, column=0, pady=10, padx=10)

    client_email = ttk.Entry(tab_client)
    client_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_client, text="Email").grid(row=1, column=0, pady=10, padx=10)

    client_phone = ttk.Entry(tab_client)
    client_phone.grid(row=2, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_client, text="Телефон").grid(row=2, column=0, pady=10, padx=10)

    client_membership = ttk.Combobox(tab_client, values=['Basic', 'Premium', 'VIP'])
    client_membership.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
    client_membership.set('Basic')  # За замовчуванням 'Basic'
    tk.Label(tab_client, text="Тип абонемента").grid(row=3, column=0, pady=10, padx=10)

    client_address = ttk.Entry(tab_client)
    client_address.grid(row=4, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_client, text="Адреса").grid(row=4, column=0, pady=10, padx=10)

    def add_client():
        def get_membership_types():
            try:
                cursor.execute("SELECT Membership_Name FROM memberships")
                # Strip spaces and convert to lowercase for consistent comparison
                return [row[0].strip().lower() for row in cursor.fetchall()]
            except mysql.connector.Error as err:
                messagebox.showerror("Помилка бази даних", f"Не вдалося отримати список абонементів: {err}")
                return []

        valid_membership_types = get_membership_types()

        # Get the selected membership type and strip spaces
        membership_type = client_membership.get().strip().lower()

        # Check if the selected type is in the valid list
        if membership_type not in valid_membership_types:
            messagebox.showwarning("Помилка", "Некоректний тип абонемента!")
            return

        try:
            # Додавання клієнта до бази даних
            cursor.execute(""" 
                INSERT INTO clients (name, email, phone, membership_type, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (client_name.get(), client_email.get(), client_phone.get(), membership_type, client_address.get()))
            db.commit()
            messagebox.showinfo("Успіх", "Клієнта додано успішно.")
            refresh_client_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка", f"Помилка при додаванні клієнта: {err}")
    def delete_client():
        client_id = client_id_entry_delete.get()  # Отримуємо ID клієнта для видалення
        if not client_id:
            messagebox.showwarning("Помилка вводу", "Будь ласка, введіть ID клієнта для видалення.")
            return

        try:
            query = "DELETE FROM clients WHERE client_id = %s"
            cursor.execute(query, (client_id,))
            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Успіх", "Клієнта видалено успішно.")
            else:
                messagebox.showwarning("Не знайдено", "Клієнта з вказаним ID не знайдено.")
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка бази даних", f"Помилка при видаленні клієнта: {err}")

    def refresh_client_data():
        for item in client_tree.get_children():
            client_tree.delete(item)
        try:
            # Вибираємо всі необхідні стовпці у правильному порядку
            cursor.execute("SELECT client_id, name, email, phone, membership_type, address FROM clients")
            for row in cursor.fetchall():
                # У рядку має бути правильний порядок значень
                client_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка", f"Помилка при оновленні даних клієнтів: {err}")
    control_frame_client = tk.Frame(tab_client, bg="#f4f4f9")
    control_frame_client.grid(row=5, column=0, columnspan=2, pady=20)

    ttk.Button(control_frame_client, text="Додати клієнта", command=add_client, style="TButton").grid(row=0, column=0,
                                                                                                      padx=10, pady=10)
    ttk.Button(control_frame_client, text="Видалити клієнта", command=delete_client, style="TButton").grid(row=0,
                                                                                                           column=1,
                                                                                                           padx=10,
                                                                                                           pady=10)
    ttk.Button(control_frame_client, text="Оновити дані клієнта", command=refresh_client_data, style="TButton").grid(
        row=0, column=2, padx=10, pady=10)

    delete_client_frame = tk.Frame(tab_client, bg="#f4f4f9")
    delete_client_frame.grid(row=6, column=0, columnspan=2, pady=10)

    tk.Label(delete_client_frame, text="ID клієнта (для видалення)").grid(row=0, column=0, padx=10, pady=10)
    client_id_entry_delete = ttk.Entry(delete_client_frame, width=10)
    client_id_entry_delete.grid(row=0, column=1, pady=10, padx=10)

    client_tree = ttk.Treeview(tab_client, columns=("ID", "Ім'я", "Email", "Телефон", "Тип абонемента", "Адреса"),
                               show="headings")
    client_tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    client_tree.heading("ID", text="ID")
    client_tree.heading("Ім'я", text="Ім'я")
    client_tree.heading("Email", text="Email")
    client_tree.heading("Телефон", text="Телефон")
    client_tree.heading("Тип абонемента", text="Тип абонемента")
    client_tree.heading("Адреса", text="Адреса")
    client_tree.column("ID", width=50)
    client_tree.column("Ім'я", width=150)
    client_tree.column("Email", width=200)
    client_tree.column("Телефон", width=150)
    client_tree.column("Тип абонемента", width=120)
    client_tree.column("Адреса", width=200)
    refresh_client_data()


# Виклик функцій для створення інтерфейсів
create_trainer_interface()
create_client_interface()

def create_membership_interface():
    # Очищаємо вкладку
    for widget in tab_membership.winfo_children():
        widget.destroy()

    # Поля для введення нового абонемента
    membership_type = ttk.Entry(tab_membership)
    membership_type.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="Тип абонемента").grid(row=0, column=0, pady=10, padx=10)

    membership_duration = ttk.Entry(tab_membership)
    membership_duration.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="Тривалість (міс.)").grid(row=1, column=0, pady=10, padx=10)

    membership_price = ttk.Entry(tab_membership)
    membership_price.grid(row=2, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="Ціна").grid(row=2, column=0, pady=10, padx=10)

    # Поле для введення ID абонемента для видалення
    membership_id_entry_delete = ttk.Entry(tab_membership)
    membership_id_entry_delete.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="ID абонемента для видалення").grid(row=3, column=0, pady=10, padx=10)

    # Функція для додавання абонемента
    for widget in tab_membership.winfo_children():
        widget.destroy()

    # Поля для введення нового абонемента
    membership_type = ttk.Entry(tab_membership)
    membership_type.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="Тип абонемента").grid(row=0, column=0, pady=10, padx=10)

    membership_price = ttk.Entry(tab_membership)  # Переміщено поле для ціни
    membership_price.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="Ціна").grid(row=1, column=0, pady=10, padx=10)

    membership_duration = ttk.Entry(tab_membership)  # Переміщено поле для тривалості
    membership_duration.grid(row=2, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="Тривалість (міс.)").grid(row=2, column=0, pady=10, padx=10)

    # Поле для введення ID абонемента для видалення
    membership_id_entry_delete = ttk.Entry(tab_membership)
    membership_id_entry_delete.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_membership, text="ID абонемента для видалення").grid(row=3, column=0, pady=10, padx=10)

    # Функція для додавання абонемента
    def add_membership():
        try:
            # Отримання даних із полів введення
            membership_name = membership_type.get().strip()  # Ім'я абонемента
            if not membership_name:
                raise ValueError("Тип абонемента не може бути порожнім.")
            price = float(membership_price.get().strip())  # Ціна абонемента (тепер з 2-го поля)
            duration_months = int(membership_duration.get().strip())  # Тривалість у місяцях (тепер з 3-го поля)

            # SQL-запит для вставки даних
            cursor.execute("""
                INSERT INTO Memberships (Membership_Name, Duration_Months, Price)
                VALUES (%s, %s, %s)
            """, (membership_name, duration_months, price))

            # Збереження змін у базі даних
            db.commit()

            # Повідомлення про успіх
            messagebox.showinfo("Успіх", f"Абонемент '{membership_name}' додано успішно.")
            refresh_membership_data()

            # Очищення полів після додавання
            membership_type.delete(0, 'end')
            membership_price.delete(0, 'end')
            membership_duration.delete(0, 'end')
        except ValueError as e:
            messagebox.showerror("Помилка вводу", f"Помилка у введених даних: {e}")
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка бази даних", f"Помилка при додаванні абонемента: {err}")

    # Функція для видалення абонемента
    def delete_membership():
        try:
            membership_id = membership_id_entry_delete.get().strip()  # Отримуємо ID абонемента для видалення
            if not membership_id:
                raise ValueError("ID абонемента не може бути порожнім.")

            # SQL-запит для видалення абонемента за ID
            cursor.execute("DELETE FROM Memberships WHERE ID = %s", (membership_id,))

            # Збереження змін у базі даних
            db.commit()

            # Повідомлення про успіх
            messagebox.showinfo("Успіх", f"Абонемент з ID '{membership_id}' видалено успішно.")
            refresh_membership_data()

            # Очищення поля для ID після видалення
            membership_id_entry_delete.delete(0, 'end')

        except ValueError as e:
            messagebox.showerror("Помилка вводу", f"Помилка у введених даних: {e}")
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка бази даних", f"Помилка при видаленні абонемента: {err}")

    # Функція для оновлення даних абонементів
    def refresh_membership_data():
        for item in membership_tree.get_children():
            membership_tree.delete(item)
        try:
            if db.is_connected():
                cursor.execute("SELECT * FROM Memberships")
                for row in cursor.fetchall():
                    membership_tree.insert("", tk.END, values=row)
            else:
                messagebox.showerror("Помилка", "З'єднання з базою даних втрачено!")
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка", f"Помилка при оновленні даних абонементів: {err}")

    # Інтерфейс керування
    control_frame_membership = tk.Frame(tab_membership, bg="#f4f4f9")
    control_frame_membership.grid(row=4, column=0, columnspan=2, pady=20)

    ttk.Button(control_frame_membership, text="Додати абонемент", command=add_membership, style="TButton").grid(row=0,
                                                                                                                column=0,
                                                                                                                padx=10,
                                                                                                                pady=10)
    ttk.Button(control_frame_membership, text="Видалити абонемент", command=delete_membership, style="TButton").grid(
        row=0, column=1, padx=10, pady=10)
    ttk.Button(control_frame_membership, text="Оновити дані абонемента", command=refresh_membership_data,
               style="TButton").grid(row=0, column=2, padx=10, pady=10)

    # Відображення даних абонементів у таблиці
    membership_tree = ttk.Treeview(tab_membership, columns=("ID", "Тип абонемента", "Ціна", "Тривалість"),
                                   show="headings")
    membership_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    membership_tree.heading("ID", text="ID")
    membership_tree.heading("Тип абонемента", text="Тип абонемента")
    membership_tree.heading("Ціна", text="Ціна")
    membership_tree.heading("Тривалість", text="Тривалість")

    refresh_membership_data()


def create_payment_interface():
    # Очищаємо вкладку
    for widget in tab_payments.winfo_children():
        widget.destroy()

    # Поля для введення платежу
    payment_amount = ttk.Entry(tab_payments)
    payment_amount.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_payments, text="Сума платежу").grid(row=0, column=0, pady=10, padx=10)

    payment_date = ttk.Entry(tab_payments)
    payment_date.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_payments, text="Дата платежу").grid(row=1, column=0, pady=10, padx=10)

    # Використовуємо комбобокс для типу абонемента
    payment_membership_type = ttk.Combobox(tab_payments, values=["Basic", "Premium", "VIP"], state="readonly")
    payment_membership_type.set("Basic")  # Встановлюємо значення за замовчуванням
    payment_membership_type.grid(row=2, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_payments, text="Тип абонемента").grid(row=2, column=0, pady=10, padx=10)

    # Поле для введення ID клієнта
    payment_client_id = ttk.Entry(tab_payments)
    payment_client_id.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
    tk.Label(tab_payments, text="ID Клієнта").grid(row=3, column=0, pady=10, padx=10)

    # Функція для додавання платежу
    def add_payment():
        client_id = payment_client_id.get()  # Отримуємо ID клієнта
        if not client_id:
            messagebox.showwarning("Помилка вводу", "Будь ласка, введіть ID клієнта.")
            return
        try:
            cursor.execute("""
                INSERT INTO payments (client_id, amount, payment_date, membership_type)
                VALUES (%s, %s, %s, %s)
            """, (client_id, payment_amount.get(), payment_date.get(), payment_membership_type.get()))
            db.commit()
            messagebox.showinfo("Успіх", "Платіж додано успішно.")
            refresh_payment_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка", f"Помилка при додаванні платежу: {err}")

    # Функція для видалення платежу
    def delete_payment():
        payment_id = payment_id_entry_delete.get()  # Отримуємо ID платежу для видалення
        if not payment_id:
            messagebox.showwarning("Помилка вводу", "Будь ласка, введіть ID платежу для видалення.")
            return

        try:
            query = "DELETE FROM payments WHERE payment_id = %s"
            cursor.execute(query, (payment_id,))
            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Успіх", "Платіж видалено успішно.")
            else:
                messagebox.showwarning("Не знайдено", "Платіж з вказаним ID не знайдено.")
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка бази даних", f"Помилка при видаленні платежу: {err}")

    def refresh_payment_data():
        for item in payment_tree.get_children():
            payment_tree.delete(item)
        try:
            # Вибираємо тільки необхідні стовпці: payment_id, client_id, amount, payment_date, membership_type
            cursor.execute("SELECT payment_id, client_id, amount, payment_date, membership_type FROM payments")
            for row in cursor.fetchall():
                # Вставляємо значення у правильному порядку
                payment_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))
        except mysql.connector.Error as err:
            messagebox.showerror("Помилка", f"Помилка при оновленні даних платежів: {err}")

    # Контрольна панель для платежів
    control_frame_payment = tk.Frame(tab_payments, bg="#f4f4f9")
    control_frame_payment.grid(row=4, column=0, columnspan=2, pady=20)

    ttk.Button(control_frame_payment, text="Додати платіж", command=add_payment, style="TButton").grid(row=0, column=0, padx=10, pady=10)
    ttk.Button(control_frame_payment, text="Видалити платіж", command=delete_payment, style="TButton").grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(control_frame_payment, text="Оновити дані платежів", command=refresh_payment_data, style="TButton").grid(row=0, column=2, padx=10, pady=10)

    # Поле для видалення платежу за ID
    delete_payment_frame = tk.Frame(tab_payments, bg="#f4f4f9")
    delete_payment_frame.grid(row=5, column=0, columnspan=2, pady=10)

    tk.Label(delete_payment_frame, text="ID платежу (для видалення)").grid(row=0, column=0, padx=10, pady=10)
    payment_id_entry_delete = ttk.Entry(delete_payment_frame, width=10)
    payment_id_entry_delete.grid(row=0, column=1, pady=10, padx=10)

    # Відображення даних платежів у таблиці
    payment_tree = ttk.Treeview(tab_payments, columns=("ID", "Клієнт ID", "Сума", "Дата", "Тип абонемента"), show="headings")
    payment_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    payment_tree.heading("ID", text="ID")
    payment_tree.heading("Клієнт ID", text="Клієнт ID")
    payment_tree.heading("Сума", text="Сума")
    payment_tree.heading("Дата", text="Дата")
    payment_tree.heading("Тип абонемента", text="Тип абонемента")

    refresh_payment_data()

# Викликаємо функцію для створення інтерфейсу платежів
create_payment_interface()
create_membership_interface()
# Запускаємо головний цикл програми
root.mainloop()