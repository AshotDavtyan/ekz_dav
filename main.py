import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox, QGridLayout, QInputDialog
from PyQt5.QtCore import pyqtSignal
import datetime


class Database:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='ekz_dav')
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def add_job(self, worker_id, job_name, payment, start_date, end_date=None):
        query = "INSERT INTO jobs (worker_id, job_name, payment, start_date, end_date) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (worker_id, job_name, payment, start_date, end_date))
        self.conn.commit()

    def edit_job(self, job_id, worker_id, job_name, payment, start_date, end_date=None):
        query = "UPDATE jobs SET worker_id = %s, job_name = %s, payment = %s, start_date = %s, end_date = %s WHERE id = %s"
        self.cursor.execute(query, (worker_id, job_name, payment, start_date, end_date, job_id))
        self.conn.commit()

    def delete_job(self, job_id):
        query = "DELETE FROM jobs WHERE id = %s"
        self.cursor.execute(query, (job_id,))
        self.conn.commit()

    def search_jobs_by_worker_id(self, worker_id):
        query = "SELECT * FROM jobs WHERE worker_id = %s"
        self.cursor.execute(query, (worker_id,))
        return self.cursor.fetchall()

    def search_task_by_name(self, task_name):
        query = "SELECT * FROM tasks WHERE task_name LIKE %s"
        self.cursor.execute(query, (f"%{task_name}%",))
        return self.cursor.fetchall()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления Ekz_Dav")
        self.setGeometry(100, 100, 800, 600)

        self.db = Database()

        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        add_job_btn = QPushButton("Добавить работу")
        add_job_btn.clicked.connect(self.add_job_clicked)
        layout.addWidget(add_job_btn)

        edit_job_btn = QPushButton("Редактировать работу")
        edit_job_btn.clicked.connect(self.edit_job_clicked)
        layout.addWidget(edit_job_btn)

        delete_job_btn = QPushButton("Удалить работу")
        delete_job_btn.clicked.connect(self.delete_job_clicked)
        layout.addWidget(delete_job_btn)

        search_by_worker_btn = QPushButton("Поиск работ по ID работника")
        search_by_worker_btn.clicked.connect(self.search_jobs_by_worker_id)
        layout.addWidget(search_by_worker_btn)

        search_task_btn = QPushButton("Поиск задания по названию")
        search_task_btn.clicked.connect(self.search_task_by_name)
        layout.addWidget(search_task_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_job_clicked(self):
        self.dialog = AddEditJobDialog(self.db)
        self.dialog.data_changed.connect(self.show_jobs)
        self.dialog.exec_()

    def edit_job_clicked(self):
        row = self.result_table.currentRow()
        if row != -1:
            job_id = self.result_table.item(row, 0).text()
            self.dialog = AddEditJobDialog(self.db, job_id)
            self.dialog.data_changed.connect(self.show_jobs)
            self.dialog.exec_()

    def delete_job_clicked(self):
        row = self.result_table.currentRow()
        if row != -1:
            job_id = self.result_table.item(row, 0).text()
            reply = QMessageBox.question(self, 'Удаление работы', 'Вы уверены, что хотите удалить эту работу?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.delete_job(job_id)
                self.show_jobs()

    def search_jobs_by_worker_id(self):
        worker_id, ok = QInputDialog.getInt(self, 'Поиск работ', 'Введите ID работника:')
        if ok:
            result = self.db.search_jobs_by_worker_id(worker_id)
            self.display_result(result)

    def search_task_by_name(self):
        task_name, ok = QInputDialog.getText(self, 'Поиск задания', 'Введите название задания:')
        if ok:
            result = self.db.search_task_by_name(task_name)
            self.display_result(result)

    def display_result(self, result):
        self.result_table.setRowCount(len(result))
        self.result_table.setColumnCount(len(result[0]))
        self.result_table.setHorizontalHeaderLabels(
            ['ID', 'ID работника', 'Название работы', 'Зарплата', 'Дата начала', 'Дата окончания'])
        for i, row in enumerate(result):
            for j, cell in enumerate(row):
                self.result_table.setItem(i, j, QTableWidgetItem(str(cell)))

    def show_jobs(self):
        result = self.db.cursor.execute("SELECT * FROM jobs")
        self.display_result(self.db.cursor.fetchall())

    def closeEvent(self, event):
        self.db.close_connection()
        event.accept()


class AddEditJobDialog(QDialog):
    data_changed = pyqtSignal()

    def __init__(self, db, job_id=None):
        super().__init__()
        self.db = db
        self.job_id = job_id

        self.setWindowTitle("Добавить/Редактировать работу")

        layout = QGridLayout()

        self.worker_id_edit = QLineEdit()
        self.job_name_edit = QLineEdit()
        self.payment_edit = QLineEdit()
        self.start_date_edit = QLineEdit()
        self.end_date_edit = QLineEdit()

        layout.addWidget(QLabel("ID работника:"), 0, 0)
        layout.addWidget(self.worker_id_edit, 0, 1)

        layout.addWidget(QLabel("Название работы:"), 1, 0)
        layout.addWidget(self.job_name_edit, 1, 1)

        layout.addWidget(QLabel("Зарплата:"), 2, 0)
        layout.addWidget(self.payment_edit, 2, 1)

        layout.addWidget(QLabel("Дата начала (дд-мм-гггг):"), 3, 0)
        layout.addWidget(self.start_date_edit, 3, 1)

        layout.addWidget(QLabel("Дата окончания (дд-мм-гггг):"), 4, 0)
        layout.addWidget(self.end_date_edit, 4, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 5, 0, 1, 2)

        self.setLayout(layout)

        if job_id is not None:
            self.load_data()

    def load_data(self):
        query = "SELECT * FROM jobs WHERE id = %s"
        self.db.cursor.execute(query, (self.job_id,))
        job = self.db.cursor.fetchone()
        if job:
            self.worker_id_edit.setText(str(job[1]))
            self.job_name_edit.setText(job[2])
            self.payment_edit.setText(str(job[3]))
            self.start_date_edit.setText(job[4].strftime('%d-%m-%Y'))
            if job[5]:
                self.end_date_edit.setText(job[5].strftime('%d-%m-%Y'))

    def accept(self):
        try:
            worker_id = int(self.worker_id_edit.text())
            job_name = self.job_name_edit.text()
            payment = float(self.payment_edit.text())


            try:
                start_date = self.start_date_edit.text()
                start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Некорректный формат даты начала")
                return

            end_date = self.end_date_edit.text() or None
            if end_date:
                try:
                    end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Некорректный формат даты окончания")
                    return

            if self.job_id is None:
                self.db.add_job(worker_id, job_name, payment, start_date, end_date)
            else:
                self.db.edit_job(self.job_id, worker_id, job_name, payment, start_date, end_date)
            self.data_changed.emit()
            super().accept()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод данных")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении работы: {e}")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
