from datetime import datetime
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QLabel, QPushButton, \
    QDialog, QFormLayout, QWidget, QGridLayout, QLineEdit, \
    QMessageBox, QTextEdit, QTableWidget, QTableWidgetItem, QRadioButton, QInputDialog, \
    QToolTip, QComboBox, QMenu, QAction, QActionGroup
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtGui, QtCore, QtWebEngineWidgets
from PyQt5.QtGui import QCursor
from sqlite_code import (fake_data, display_table, search_employee, update_employee, insert_data,
                         create_employee_object, delete_employee, number_of_employee, total_salary, avg_salary_per_pos)

from authenticate import check_user

# send mail
from use_jet_mail import send_email_to_employee, validate_email

# Plotly
import plotly.graph_objects as go

search_values = []

header_dic = {'Employee ID': 'emp_id', 'Name': 'name', 'Lastname': 'lname', 'Age': 'age', 'Salary': 'salary',
              'Position': 'position', 'Email': 'email'}

widgets = {'tableWidget': [],
           'buttons': [],
           'radiobuttons': [],
           'searched_table': [],
           'employee_fields': [],
           'labels': [],
           'plots': [],
           'logo': []}

SIGNAL_FOR_TEST = True
CURRENT_PAGE = 'Login'

usr = ""


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'HT- Employee Management System'

        self.colors = {"background_color": "#161219", "button_color": "white", "table_color": "#161219",
                       'table_gridline_color': 'green', 'table_text_color': 'white',
                       'table_item_backgrond_color': 'gray', 'table_item_selected_background_color': '#161219',
                       'table_item_selected_color': 'white', 'button_border_color': '#660000',
                       'button_text_color': 'white', 'button_on_hover_bacground_color': '#660000',
                       'textbox_color': 'black', 'textbox_border': 'gray', 'textbox_background': 'white',
                       'label_color': 'white', 'radiobutton_text_color': 'white', 'popup_background_color': '#161219',
                       'popup_text_color': 'white', 'table_item_border_color': 'white',
                       'search_textbox_border_color': 'gray', 'input_dialog_background_color': '#161219',
                       'input_dialog_text_color': 'white'}

        self.font = "Bookman Old Style"
        self.width = 1200
        self.height = 800
        # self.layout=QGridLayout()
        widget = QWidget()
        self.layout = QGridLayout()
        self.font_size = "20px"

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # layout.addWidget(b1)
        self.timer = QtCore.QTimer()


        self.initui()

    def initui(self):
        self.setWindowTitle(self.title)

        # App Icon
        self.setWindowIcon(QtGui.QIcon('app-icon.ico'))

        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setGeometry(300, 300, 300, 200)
        self.move(420, 70)
        self.setWindowTitle(self.title)

        self.setStyleSheet("font-size:%s;background-color: %s;font-family:%s" % (
                           self.font_size, self.colors['background_color'], self.font))


        bar = self.menuBar()
        # Profile File Menu
        file_menu = bar.addMenu('Profile')
        display_profile_btn = QAction('Profile Info', self)
        # Theme File Menu
        file_menu3 = bar.addMenu('Theme')
        light_mode = QAction('Light Mode', checkable=True)
        dark_mode = QAction('Dark Mode', checkable=True)
        # Font File menu
        file_menu2 = bar.addMenu('Font')
        bookman_font = QAction('Bookman Old', checkable=True)
        arial_font = QAction('Arial', checkable=True)
        times_font = QAction('Times', checkable=True)
        comic_font = QAction('Comic', checkable=True)

        file_menu.addAction(display_profile_btn)
        file_menu3.addAction(light_mode)
        file_menu3.addAction(dark_mode)
        file_menu2.addAction(bookman_font)
        file_menu2.addAction(arial_font)
        file_menu2.addAction(times_font)
        file_menu2.addAction(comic_font)

        # Grouping Theme buttons
        action_group = QActionGroup(self)
        action_group.addAction(light_mode)
        action_group.addAction(dark_mode)

        # Grouping Font buttons
        action_group2 = QActionGroup(self)
        action_group2.addAction(bookman_font)
        action_group2.addAction(arial_font)
        action_group2.addAction(times_font)
        action_group2.addAction(comic_font)

        bar.setStyleSheet("*{color:'black';background-color:'white'}")

        # Connect Menu Bar buttons
        light_mode.triggered.connect(self.light_mode_screen)
        dark_mode.triggered.connect(self.dark_mode_screen)
        bookman_font.triggered.connect(self.use_bookman_font)
        arial_font.triggered.connect(self.use_arial_font)
        times_font.triggered.connect(self.use_times_font)
        comic_font.triggered.connect(self.use_comic_font)
        display_profile_btn.triggered.connect(self.display_profile_dialog)

        self.login_page()
        # to show window
        self.show()


    def use_comic_font(self):
        self.font = "Comic Sans MS"
        self.check_page()

    def use_bookman_font(self):
        self.font = "Bookman Old Style"
        self.check_page()

    def use_times_font(self):
        self.font = "Times"
        self.check_page()

    def use_arial_font(self):
        self.font = "Arial"
        self.check_page()

    def light_mode_screen(self):

        self.colors = {"background_color": "white", "button_color": "black", "table_color": "white",
                       'table_gridline_color': 'black', 'table_text_color': 'black',
                       'table_item_backgrond_color': 'skyblue', 'table_item_selected_background_color': '#F5F5F5',
                       'table_item_selected_color': 'black', 'bar_text_color': 'black', 'button_border_color': 'black',
                       'button_text_color': 'black', 'button_on_hover_bacground_color': 'skyblue',
                       'textbox_border': 'black', 'textbox_color': 'black', 'textbox_background': 'white',
                       'label_color': 'black', 'radiobutton_text_color': 'black', 'popup_background_color': 'white',
                       'popup_text_color': 'black', 'table_item_border_color': 'black',
                       'search_textbox_border_color': 'black', 'input_dialog_background_color': 'white',
                       'input_dialog_text_color': 'black'}
        self.setStyleSheet("font-size:%s;background-color: %s;font-family:%s" % (
                          self.font_size, self.colors['background_color'], self.font))
        self.check_page()

    def dark_mode_screen(self):
        self.colors = {"background_color": "#161219", "button_color": "white", "table_color": "#161219",
                       'table_gridline_color': 'green', 'table_text_color': 'white',
                       'table_item_backgrond_color': 'gray', 'table_item_selected_background_color': '#161219',
                       'table_item_selected_color': 'white', 'button_border_color': '#660000',
                       'button_text_color': 'white', 'button_on_hover_bacground_color': '#660000',
                       'textbox_border': 'gray', 'textbox_color': 'black', 'textbox_background': 'white',
                       'label_color': 'white', 'radiobutton_text_color': 'white', 'popup_background_color': '#161219',
                       'popup_text_color': 'white', 'table_item_border_color': 'white',
                       'search_textbox_border_color': 'gray', 'input_dialog_background_color': '#161219',
                       'input_dialog_text_color': 'white'}
        self.setStyleSheet("font-size:%s;background-color: %s;font-family:%s" % (
                          self.font_size, self.colors['background_color'], self.font))
        self.check_page()

    # start of Fake Data Generator methods
    def generator(self, sql_list):
        for q in sql_list:
            yield q

    def prepare_data_from_sql(self):
        global SIGNAL_FOR_TEST
        if SIGNAL_FOR_TEST:
            fake_data()
            SIGNAL_FOR_TEST = False
        sql_list = display_table()
        gen = self.generator(sql_list)
        return gen, len(sql_list)

    # end of Fake Data Generator methods

    # Start of Drawing Methods
    def draw_table(self, row_numbers):
        tablewidget = QTableWidget()
        tablewidget.setStyleSheet("QTableView{color: %s;" % (self.colors['table_text_color']) +
                                  "border: 1px solid gray;" +
                                  "background-color: %s;" % (self.colors['table_color']) +
                                  "gridline-color: %s;" % (self.colors['table_gridline_color']) +

                                  "font-family:'%s';}" % self.font +
                                  "QTableView::item:focus{background-color:%s;border: 1px solid %s;"
                                  "margin-left: 10px;margin-right: 10px;}" % (
                                  self.colors['table_item_backgrond_color'], self.colors['table_item_border_color']) +
                                  "QHeaderView::section{background-color:%s;font-family:%s;" % (
                                  self.colors['table_item_selected_background_color'], self.font) +

                                  "color:%s}" % (self.colors['table_item_selected_color']))

        tablewidget.verticalHeader().hide()
        tablewidget.setEditTriggers(tablewidget.NoEditTriggers)
        tablewidget.setRowCount(row_numbers)
        tablewidget.setColumnCount(7)
        tablewidget.setFixedWidth(1170)
        header = tablewidget.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        tablewidget.setHorizontalHeaderLabels(['Employee ID', 'Name', 'Lastname', "Age", "Salary", 'Position', 'Email'])
        tablewidget.cellDoubleClicked.connect(self.display_update_query_popup)
        tablewidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tablewidget.customContextMenuRequested.connect(self.display_right_clicked_menu)
        widgets['tableWidget'].append(tablewidget)
        return tablewidget

    def draw_form_dialog(self, employee_name, employee_lname, email_address):
        box = QDialog()
        box.setStyleSheet("font-size:%s;background: %s;color:%s;font-family:%s;" % (
            self.font_size, self.colors['popup_background_color'], self.colors['popup_text_color'], self.font))
        box.setWindowIcon(QtGui.QIcon('send-data.png'))
        box.setWindowTitle("Send Email to Employee")
        box.setWhatsThis("Provide subject and message to send email")
        email_address_label = QLabel(email_address)
        email_subject = QLineEdit()
        email_message = QTextEdit()
        # primary_key_type = QComboBox()
        # column_names = QLineEdit('name,age', )
        # column_types = QLineEdit('text,integer', )
        # primary_key_type.addItems(["text", "integer", "date"])
        #
        send_btn = QPushButton("Send Email")
        cancel_btn = QPushButton("Cancel")
        lay = QFormLayout(box)
        lay.addRow("Email: ", email_address_label)
        lay.addRow("Subject:", email_subject)
        lay.addRow("Message", email_message)
        # lay.addRow("Primary key Data Type:", primary_key_type)
        # lay.addRow("Other Column Names(e.g name,age):", column_names)
        # lay.addRow("Other Column Data Types(e.g text,integer):", column_types)
        lay.addRow(send_btn)
        lay.addRow(cancel_btn)
        send_btn.clicked.connect(
            lambda: self.get_info_for_sending_email(box, employee_name, employee_lname, email_address,
                                                    email_subject.text(), email_message.toPlainText()))
        cancel_btn.clicked.connect(box.reject)
        # lay.addWidget(first)
        return box

    def draw_textbox(self, place_holder="", text=""):
        field = QLineEdit(text)
        field.setPlaceholderText(place_holder)
        field.setFixedWidth(160)

        field.setStyleSheet("QLineEdit{color: %s;" % (self.colors['textbox_color']) +
                            "border: 3px solid %s;" % (self.colors['textbox_border']) +
                            "background-color: %s;" % (self.colors['textbox_background']) +
                            "margin-right:f'{margin-right}' !important;" +
                            "height:30px;" +
                            'font-size:18px;' +
                            "font-family:'%s';}" % self.font
                            )
        widgets['employee_fields'].append(field)
        return field

    def draw_label(self, label_text, width=760, height=300, font_size=25, alignment=QtCore.Qt.AlignCenter):
        label = QLabel()
        label.setFixedWidth(width)
        label.setFixedHeight(height)

        label.setText(label_text)
        label.setAlignment(alignment)
        label.setStyleSheet("font-family:'%s';" % self.font +
                            "font-size: %ipx ;" % font_size +
                            "color: %s;" % (self.colors['label_color']))
        widgets['labels'].append(label)
        return label

    def draw_button(self, btn_text='test', width=165, height=55, icon_path="", tool_tip_text='test'):
        QToolTip.setFont(QFont('Bookman Old Style', 10))
        btn = QPushButton(btn_text)
        btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn.setFixedWidth(width)
        btn.setFixedHeight(height)
        btn.setStyleSheet("QPushButton{border: 2px solid '%s';" % (self.colors['button_border_color']) +
                          "border-radius:45px;" +
                          "font-size:15px;" +
                          "color: %s ;" % (self.colors['button_text_color']) +
                          "padding: 25px 0; " +
                          "font-family:%s;" % self.font +
                          "margin:10px 10px ;}" +
                          "QPushButton:hover{background:'%s';}" % (self.colors['button_on_hover_bacground_color']))
        btn.setIcon(QIcon(icon_path))
        btn.setToolTip(tool_tip_text)
        widgets['buttons'].append(btn)
        return btn

    def draw_radio_btn(self, text='Text'):

        radiobtn = QRadioButton(text)

        radiobtn.country = text

        radiobtn.setStyleSheet("QRadioButton{color: %s;}" % (self.colors['radiobutton_text_color']) +
                               "QRadioButton::indicator:checked {  color:blue;}"
                               )
        widgets['radiobuttons'].append(radiobtn)
        return radiobtn

    # End of Drawing Methods

    # Start of page view methods
    def login_page(self):

        logo = self.draw_label('HT Employee Management System', width=1200, font_size=50)

        logo.setAlignment(QtCore.Qt.AlignCenter)

        widgets['logo'].append(logo)
        # button widget

        user_name_input = QLineEdit()
        user_name_input.setPlaceholderText('Username')
        user_name_input.setStyleSheet(
            "QLineEdit{" "color:%s; border: 4px solid '#008CBA';border-radius:25px;font-size:25px;padding: 25px 0;"
            "margin:20px 350px ;text-align: center;background:%s;font-family:%s;}" % (
                self.colors['button_color'], self.colors['background_color'], self.font))

        widgets['employee_fields'].append(user_name_input)
        password_input = QLineEdit()
        password_input.setPlaceholderText('Password')
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet("*{border: 4px solid '#008CBA';" +
                                     "border-radius:25px;" +
                                     "font-size:25px;" +
                                     "color: '%s';" % (self.colors['button_color']) +
                                     "padding: 25px 0; " +
                                     "font-family:%s;" % self.font +
                                     "background:%s;" % (self.colors['background_color']) +
                                     "margin:20px 350px ;}"
                                     )
        user_name_input.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        password_input.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        widgets['employee_fields'].append(password_input)
        button = QPushButton("Login")
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        button.setStyleSheet("*{border: 4px solid '#808000';" +
                             "font-family:%s;" % self.font +
                             "border-radius:45px;" +
                             "font-size:35px;" +
                             "color: '%s' ;" % (self.colors['button_color']) +
                             "padding: 25px 0; " +
                             "margin:20px 250px ;}" +
                             "*:hover{background:'#808000';}")
        widgets['buttons'].append(button)
        button.clicked.connect(self.authenticate)

        # adding to grid
        # in pyqt5 index 0 does not always work, so -1 is better option
        self.layout.addWidget(widgets['logo'][-1], 0, 0, 1, 2)
        self.layout.addWidget(user_name_input, 1, 0, 1, 2)
        self.layout.addWidget(password_input, 2, 0, 1, 2)
        self.layout.addWidget(widgets['buttons'][-1], 3, 0, 1, 2)

    def home_page(self):
        gen, length = self.prepare_data_from_sql()
        tablewidget = self.draw_table(length)

        for q in range(length):
            row = next(gen)
            for j in range(len(row)):
                tablewidget.setItem(q, j, QTableWidgetItem(str(row[j]), ))

        # Creating Buttons
        reload_btn = self.draw_button(btn_text='Reload', tool_tip_text="Press to reload the table",
                                      icon_path='reload.png')
        logout_btn = self.draw_button(btn_text='Logout', tool_tip_text="Press to logout from the system",
                                      icon_path='logout.png')
        search_btn = self.draw_button(btn_text="Search", tool_tip_text="Go to search page", icon_path='search.png')
        add_employee_btn = self.draw_button(btn_text="Add Employee", tool_tip_text="Go to add employee page",
                                            icon_path='add_employee.png')
        now = datetime.now()
        cur_time = now.strftime("%B %d, %Y  %H:%M:%S")
        welcome_text = self.draw_label("Welcome " + "<b style='color:#32CD32'>" + usr + "</b> ", height=20, width=150,
                                       font_size=17)
        date_text = self.draw_label(cur_time, height=25, width=1100,
                                    font_size =17)



        # Connecting Buttons
        reload_btn.clicked.connect(self.reload_page)
        search_btn.clicked.connect(self.go_to_search_page)
        add_employee_btn.clicked.connect(self.go_to_add_employee_page)
        logout_btn.clicked.connect(self.go_to_login_page)
        self.timer.timeout.connect(lambda: self.update_label(date_text))
        self.timer.start(1000)
        # Draw in Layout for homepage
        self.layout.addWidget(welcome_text, 0, 0, 1, 0)
        self.layout.addWidget(date_text, 0, 1)
        self.layout.addWidget(tablewidget, 1, 0)
        self.layout.addWidget(reload_btn, 2, 0)
        self.layout.addWidget(logout_btn, 3, 0)
        self.layout.addWidget(search_btn, 2, 2)
        self.layout.addWidget(add_employee_btn, 3, 2)


    def update_label(self,lbl):
        now = datetime.now()
        cur_time = now.strftime("%B %d, %Y  %H:%M:%S")
        lbl.setText(cur_time)



    def search_page(self):
        search_textbox = QLineEdit()
        search_textbox.setPlaceholderText("Search by name/lastname/id")
        # search_textbox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        search_textbox.setStyleSheet("QLineEdit{color: black;" +
                                     "border: 2px solid %s;" % (self.colors['search_textbox_border_color']) +
                                     "background-color: white;" +
                                     "margin-right:700px;" +
                                     "height:30px;" +
                                     "font-family:'Bookman Old Style';}"
                                     )

        # Drawing Buttons
        id_radio_button = self.draw_radio_btn("By ID")
        name_radio_button = self.draw_radio_btn("By Name")
        last_name_radio_button = self.draw_radio_btn("By Lastname")
        search_btn = self.draw_button(btn_text='Search', tool_tip_text='Search the record', icon_path='search.png')
        back_btn = self.draw_button(btn_text='Back', tool_tip_text='Back to Home', icon_path='back.png')

        # adding an empty table in widgets dictionary
        widgets['searched_table'].append(QTableWidget())
        widgets['employee_fields'].append(search_textbox)

        # connecting search page buttons
        back_btn.clicked.connect(self.go_to_home_page)
        search_btn.clicked.connect(lambda: self.search_query(search_textbox.text(), [id_radio_button, name_radio_button,
                                                                                     last_name_radio_button]))

        # Draw in Layout for searchpage

        self.layout.addWidget(search_textbox, 0, 0)
        self.layout.addWidget(id_radio_button, 1, 0)
        self.layout.addWidget(name_radio_button, 2, 0)
        self.layout.addWidget(last_name_radio_button, 3, 0)
        self.layout.addWidget(search_btn, 4, 0)
        self.layout.addWidget(widgets['searched_table'][0], 5, 0)
        self.layout.addWidget(back_btn, 6, 0)

    def plot_page(self):
        browser = QtWebEngineWidgets.QWebEngineView(self)
        browser.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        employee_plt_btn = self.draw_button(btn_text='Employee per Position',
                                            tool_tip_text='Display Employee per Position Pie Chart',
                                            icon_path='pie-chart.png', width=230)
        salary_per_positon = self.draw_button(btn_text='Salary per Position',
                                              tool_tip_text='Display Salary per Position Scatter Chart',
                                              icon_path='scatter_chart.png', width=230)
        avg_salary_plt_btn = self.draw_button(btn_text='Avg Salary per Position',
                                              tool_tip_text='Display Average Salary per Position Bar Chart',
                                              icon_path='bar_char.png', width=230)
        back_btn = self.draw_button(btn_text='Back', tool_tip_text='Back to add employee page', icon_path='back.png',
                                    width=200)

        employee_plt_btn.clicked.connect(lambda: self.get_plt(browser, 'employee_number'))
        salary_per_positon.clicked.connect(lambda: self.get_plt(browser, 'salary_per_pos'))
        avg_salary_plt_btn.clicked.connect(lambda: self.get_plt(browser, 'avg_salary'))
        back_btn.clicked.connect(self.go_to_add_employee_page)
        employee_numbers = number_of_employee()

        fig = go.Figure(data=go.Pie(values=[i[1] for i in employee_numbers], labels=[i[0] for i in employee_numbers],
                                    title="Employee per Position Pie Plot"), )

        fig.update_layout(
            font_family="%s" % self.font,
            font_color="%s" % (self.colors['button_color']),
            font_size=24,
            title_font_family="%s" % self.font,
            title_font_color="black",
            paper_bgcolor='%s' % (self.colors['background_color']),

        )
        browser.setHtml(fig.to_html(include_plotlyjs='cdn', config={'displaylogo': False}))
        browser.setFixedWidth(1180)

        widgets['plots'].append(browser)

        self.layout.addWidget(employee_plt_btn, 0, 0)
        self.layout.addWidget(salary_per_positon, 0, 1)
        self.layout.addWidget(avg_salary_plt_btn, 0, 2)

        self.layout.addWidget(browser, 3, 0, 2, 0)
        self.layout.addWidget(back_btn, 5, 0)

    def get_plt(self, browser, plot_name='employee_number'):
        if plot_name == 'employee_number':
            employee_numbers = number_of_employee()
            fig = go.Figure(
                data=go.Pie(values=[i[1] for i in employee_numbers], labels=[i[0] for i in employee_numbers],
                            title="Employee per Position Pie Plot"))
            fig.update_layout(
                font_family="%s" % self.font,
                font_color="%s" % (self.colors['button_color']),
                font_size=24,
                title_font_family="%s" % self.font,
                title_font_color="black",
                paper_bgcolor='%s' % (self.colors['background_color'])
            )
            browser.setHtml(fig.to_html(include_plotlyjs='cdn', config={'displaylogo': False, }))
            self.layout.addWidget(browser, 3, 0, 2, 0)
        if plot_name == 'avg_salary':
            avg_salary = avg_salary_per_pos()
            fig = go.Figure(data=go.Bar(x=[i[0] for i in avg_salary], y=[i[1] for i in avg_salary],
                                        marker={'color': ['red', 'purple', 'blue', 'green'],
                                                'colorscale': 'Viridis'}))
            fig.update_layout(
                font_family="%s" % self.font,
                font_color="%s" % (self.colors['button_color']),
                font_size=24,
                title_font_family="%s" % self.font,
                title_font_color="black",
                title="Average Salary per Position Bar Plot",
                paper_bgcolor='%s' % (self.colors['background_color']),
                plot_bgcolor='%s' % (self.colors['background_color']),

            )
            browser.setHtml(fig.to_html(include_plotlyjs='cdn', config={'displaylogo': False}))
            self.layout.addWidget(browser, 3, 0, 2, 0)
        if plot_name == 'salary_per_pos':
            salary = total_salary()
            fig = go.Figure(data=go.Scatter(x=[i[0] for i in salary], y=[i[1] for i in salary], mode='markers',
                                            marker=dict(size=[int(i[1] / 400) for i in salary],
                                                        color=[0, 1, 2, 3]), ))
            fig.update_layout(
                font_family="%s" % self.font,
                font_color="%s" % (self.colors['button_color']),
                font_size=24,
                title_font_family="%s" % self.font,
                title_font_color="%s" % (self.colors['button_color']),
                title="Salary per Position Scatter Plot",
                paper_bgcolor='%s' % (self.colors['background_color']),
                plot_bgcolor='%s' % (self.colors['background_color'])
            )
            browser.setHtml(fig.to_html(include_plotlyjs='cdn', config={'displaylogo': False}))
            self.layout.addWidget(browser, 3, 0, 2, 0)

    def add_employee_page(self):

        title_label = self.draw_label("Enter Required Information", width=690)
        employee_info, salary, avg_salary = self.get_intersting_info()

        employee_label = self.draw_label(label_text=employee_info, width=400, alignment=QtCore.Qt.AlignLeft)
        salary_label = self.draw_label(label_text=salary, width=400, alignment=QtCore.Qt.AlignLeft)
        avg_label = self.draw_label(label_text=avg_salary, width=400, alignment=QtCore.Qt.AlignLeft)
        id_field = self.draw_textbox(text="172XX861XX")
        id_field.setToolTip("ID will be generated automatically")
        id_field.setReadOnly(True)
        name_field = self.draw_textbox("Enter Name")
        lname_field = self.draw_textbox("Enter LastName")
        age_field = self.draw_textbox("Enter Age")
        salary_field = self.draw_textbox("Enter Salary")
        pos_field = QComboBox()
        pos_field.setStyleSheet("QComboBox{color: %s;" % (self.colors['textbox_color']) +
                                "border: 3px solid %s;" % (self.colors['textbox_border']) +
                                "background-color: %s;" % (self.colors['textbox_background']) +
                                "margin-right:f'{margin-right}' !important;" +
                                "height:30px;" +

                                "font-family:'%s';}" % self.font +
                                "QListView{background-color : %s;}" % (self.colors['textbox_background'])
                                )
        pos_field.addItems(["Employee", "Seller", 'Supervisor', 'Manager'])
        # pos_field=self.draw_textbox("Enter Position")
        email_field = self.draw_textbox("Enter Email")
        widgets['employee_fields'].append(pos_field)

        # creating buttons
        back_btn = self.draw_button(btn_text='Back', tool_tip_text='Back to Home', icon_path='back.png')
        add_employee_btn = self.draw_button(btn_text='Add Employee',
                                            tool_tip_text='Press to add employee to the records',
                                            icon_path='add_employee.png')
        plot_btn = self.draw_button(btn_text='Show Plots', tool_tip_text='Display plots', icon_path='plot.png')

        # connect add_employee_page buttons
        back_btn.clicked.connect(self.go_to_home_page)
        add_employee_btn.clicked.connect(
            lambda: self.add_employee_to_the_record(id_field, name_field.text(), lname_field.text(),
                                                    age_field.text(), salary_field.text(), pos_field.currentText(),
                                                    email_field.text()))
        plot_btn.clicked.connect(self.go_to_plot_page)

        self.layout.addWidget(title_label, 0, 1)
        self.layout.addWidget(id_field, 1, 0)
        self.layout.addWidget(name_field, 1, 1)
        self.layout.addWidget(lname_field, 1, 2)

        self.layout.addWidget(age_field, 1, 3)
        self.layout.addWidget(salary_field, 1, 4)
        self.layout.addWidget(pos_field, 1, 5)
        self.layout.addWidget(email_field, 1, 6)
        self.layout.addWidget(employee_label, 2, 0)
        self.layout.addWidget(salary_label, 2, 2)
        self.layout.addWidget(avg_label, 2, 4)

        self.layout.addWidget(add_employee_btn, 3, 6)
        self.layout.addWidget(plot_btn, 4, 6)
        self.layout.addWidget(back_btn, 3, 0)

    # End of page view methods

    # start of query methods

    def get_intersting_info(self):
        all_employees = number_of_employee()
        salary_per_positon = total_salary()
        avg_sal_per_position = avg_salary_per_pos()
        total_emp = 0
        employee_info = "Number of Employees\n-----\n"
        total_sal = 0
        pos_salary = "Salary\n-----\n"
        total_avg = 0
        avg_text = "Average Salary\n-----\n"
        for pos, n in all_employees:
            employee_info += pos + ": " + str(n) + "\n"
            total_emp += n
        employee_info += "------\nTotal: " + f'{total_emp}'
        for pos, salary in salary_per_positon:
            pos_salary += pos + ": " + str(salary) + " $\n"
            total_sal += salary
        pos_salary += "------\nTotal: " + f'{total_sal} $'
        for pos, avg in avg_sal_per_position:
            
            avg_text += pos + ": " + str(avg) + " $\n"
            total_avg += avg
            total_avg = round(total_avg, 2)
        avg_text += "------\nTotal: " + f'{total_avg} $'

        return employee_info, pos_salary, avg_text

    def add_employee_to_the_record(self, id_field, emp_name, emp_lname, emp_age, emp_salary, emp_pos, emp_email):
        import random
        if validate_email(emp_email):
            try:

                emp_id = str(random.choice(range(100, 999)))+emp_name[:2]+str(random.choice(range(100, 999)))+emp_lname[: 2]+str(random.choice(range(10,99)))
                id_field.setText(emp_id)
                # emp_id = int(emp_id)
                emp_age = int(emp_age)
                emp_salary = int(emp_salary)
                new_employee = create_employee_object(emp_id, emp_name, emp_lname, emp_age, emp_salary, emp_pos,
                                                      emp_email)
                emp_sginal, employee_acceptance_msg = insert_data(new_employee)
                if emp_sginal:
                    self.display_popup('Done', employee_acceptance_msg, QMessageBox.Information)
                    self.add_employee_page()
                else:
                    self.display_popup('ID Error', str(employee_acceptance_msg))
            except ValueError:
                self.display_popup('Value Error', "ID/age/salary must be integer number")
            except TypeError as te:
                self.display_popup('Value issue', str(te))
        else:
            self.display_popup('Email Error', "Email is not Valid")

    def search_query(self, the_search, radio_buttons):
        search_values.clear()
        search_values.extend([the_search, radio_buttons])
        the_field = self.check_radio_buttons(radio_buttons)
        if the_search == "":
            self.display_popup('Search Failed', 'Please enter what do you need to search', QMessageBox.Critical)
        else:
            self.clear_widget()
            searched_query = search_employee(the_search, the_field)
            if len(searched_query) > 0:
                gen = self.generator(searched_query)
                tablewidget = self.draw_table(len(searched_query))
                for q in range(len(searched_query)):
                    row = next(gen)
                    for j in range(len(row)):
                        tablewidget.setItem(q, j, QTableWidgetItem(str(row[j]), ))

                widgets['searched_table'] = []
                widgets['searched_table'].append(tablewidget)
                self.search_page()

            else:
                self.search_page()
                self.display_popup('Search Complete', 'Nothing Found!', QMessageBox.Information)

    def display_right_clicked_menu(self, pos):
        # pass
        menu = QMenu()
        current_row = widgets['tableWidget'][0].currentRow()
        emp_id = widgets['tableWidget'][0].item(current_row, 0).text()
        current_column = widgets['tableWidget'][0].currentColumn()
        current_item = widgets['tableWidget'][0].currentItem().text()
        # current_column_name = header_dic[widgets['tableWidget'][0].horizontalHeaderItem(current_column).text()]
        delete_btn = menu.addAction('Delete Row')
        delete_btn.setIcon(QIcon("delete.png"))

        # print(current_item,current_column_name,emp_id)
        delete_btn.triggered.connect(lambda: self.delete_query(current_item, emp_id))
        update_btn = menu.addAction('Update Cell')
        update_btn.setIcon(QIcon("update.png"))

        update_btn.triggered.connect(lambda: self.display_update_query_popup(current_row, current_column))
        send_mail_btn = menu.addAction('Send Email')
        send_mail_btn.setIcon(QIcon("send-data.png"))
        send_mail_btn.triggered.connect(lambda: self.send_email_popup(current_row))
        menu.exec_(widgets['tableWidget'][0].mapToGlobal(pos))

    def delete_query(self, del_value, emp_id):
        # pass
        # print(del_value,del_field,emp_id)
        msg = QMessageBox()
        msg.setWindowTitle("Delete a record")
        msg.setText(
            f'Are you sure about deleting "<b style="color:red">{del_value}</b>"? The row with Employee ID "'
            f'<b style="color:red">{emp_id}</b>" will be deleted')
        # # #print(del_value,del_field)
        msg.addButton(msg.Yes)
        msg.addButton(msg.No)
        msg.button(msg.Yes).clicked.connect(lambda: delete_employee(emp_id, 'emp_id'))
        msg.setStyleSheet("width:100px;height:50px;background: %s;color:%s;font-family:%s;font-size:%s" % (
                         self.colors['popup_background_color'],
                         self.colors['popup_text_color'], self.font, self.font_size))
        msg.setWindowIcon(QIcon("delete.png"))
        msg.exec_()
        # print(del_value,del_field,emp_id)

        self.reload_page() if CURRENT_PAGE == 'Home' else self.search_query(search_values[0], search_values[1])

    def send_email_popup(self, row):
        global CURRENT_PAGE
        email_address = widgets['tableWidget'][0].item(row, 6).text()
        employee_name = widgets['tableWidget'][0].item(row, 1).text()
        employee_lname = widgets['tableWidget'][0].item(row, 2).text()
        box = self.draw_form_dialog(employee_name, employee_lname, email_address)
        box.exec_()

        # print(email_address)

    def display_profile_dialog(self):
        global CURRENT_PAGE
        if CURRENT_PAGE == "Login":
            self.display_popup("Profile Error", "Please login to your account first")
        else:
            box = QDialog()
            box.setStyleSheet("font-size:%s;background: %s;color:%s;font-family:%s;" % (
                    self.font_size, self.colors['popup_background_color'], self.colors['popup_text_color'], self.font))
            box.setWindowIcon(QtGui.QIcon('profile.png'))
            box.setWindowTitle("Profile Details")
            box.setFixedWidth(600)
            box.setFixedHeight(400)
            box.setWhatsThis("Your Profile Details")
            img_label = QLabel()
            img_label.setStyleSheet(f"border-image: url('{usr}.png');background-color: black;border-radius: 50%")
            img_label.setFixedHeight(100)
            img_label.setFixedWidth(100)
            now = datetime.now()
            cur_time = now.strftime("%B %d,%Y %H:%M:%S")
            usr_label = QLabel(f"User: {usr}\n\nPosition: System Administrator\n\nLast Login: {cur_time}")
            usr_label.setAlignment(QtCore.Qt.AlignLeft)


            usr_label.setStyleSheet("font-family:'%s';" % self.font +
                                    "margin-left:20px;"
                                    "color: %s;" % (self.colors['label_color']))
            lay = QGridLayout(box)
            lay.addWidget(img_label, 0, 0)
            lay.addWidget(usr_label, 0, 1)
            box.exec_()

    def display_update_query_popup(self, row, col):
        global CURRENT_PAGE

        item = widgets['tableWidget'][0].currentItem().text()
        col_header_name = header_dic[widgets['tableWidget'][0].horizontalHeaderItem(col).text()]
        emp_id = widgets['tableWidget'][0].item(row, 0).text()
        if col_header_name == "emp_id":
            self.display_popup('Error', 'Employee ID can not be changed')

        else:
            msg = QInputDialog()
            msg.setStyleSheet("width:200px;height:50px;background: %s;color:%s;font-family:%s;font-size:%s" % (
                              self.colors['input_dialog_background_color'],
                              self.colors['input_dialog_text_color'], self.font,
                              self.font_size))
            msg.setWindowTitle("Update the Value")
            msg.setTextValue(str(item))
            msg.setLabelText(widgets['tableWidget'][0].horizontalHeaderItem(col).text())
            msg.setOkButtonText('Update value')
            msg.setWindowIcon(QIcon("update.png"))
            msg.setWhatsThis("You can update the cell value")
            msg.exec_()
            if msg.result():
                new_value = msg.textValue()

                if self.check_value_integrity(col_header_name, new_value):
                    update_employee(col_header_name, new_value, emp_id)
                    self.reload_page() if CURRENT_PAGE == 'Home' else self.search_query(search_values[0],
                                                                                        search_values[1])
                else:
                    pass
            else:
                pass

    def check_value_integrity(self, col_header_name, new_value):
        if col_header_name == "email":
            if validate_email(new_value):
                return True
            else:
                self.display_popup('Email Error', "Not a Valid Email Address")
                return False

        if col_header_name == 'age':
            try:
                if 18 < int(new_value) < 70:
                    return True
                else:
                    self.display_popup('Age Error', "the age must be integer number and 18<age<70")
                    return False
            except ValueError:
                self.display_popup('Value Error', "Inavild value, the age must be integer number and 18<age<70")
                return False

        if col_header_name == 'position':
            if new_value in ["Employee", "Seller", 'Supervisor', 'Manager']:
                return True
            else:
                self.display_popup('Position Error',
                                   "Only  Employee,Seller,Supervisor,Manager for Position Column are accepted")
                return False

        if col_header_name == 'salary':
            try:
                if int(new_value):
                    return True
            except ValueError:
                self.display_popup('Value Error', "Inavild value, the salary must be integer number")
                return False
        else:
            return True

    def get_info_for_sending_email(self, box, employee_name, employee_lname, email_address, email_subject,
                                   email_message):
        if all([email_address, email_subject, email_message]):
            send_email_to_employee(employee_name, employee_lname, email_address, email_subject, email_message)
            box.close()

        else:
            self.display_popup("Error", "Provide subject and message")

    # end of query methods

    # start of changing page methods
    def go_to_home_page(self):
        global CURRENT_PAGE
        CURRENT_PAGE = 'Home'
        # print(CURRENT_PAGE)
        self.clear_widget()

        self.home_page()

    def go_to_login_page(self):
        global CURRENT_PAGE
        CURRENT_PAGE = 'Login'
        # print(CURRENT_PAGE)
        self.clear_widget()

        self.login_page()

    def go_to_plot_page(self):
        global CURRENT_PAGE
        CURRENT_PAGE = 'Plot'

        # print(CURRENT_PAGE)
        self.clear_widget()

        self.plot_page()

    def go_to_add_employee_page(self):
        global CURRENT_PAGE
        CURRENT_PAGE = 'Add_Employee'
        # print(CURRENT_PAGE)
        self.clear_widget()

        self.add_employee_page()

    def go_to_search_page(self):
        global CURRENT_PAGE
        CURRENT_PAGE = 'Search'
        # print(CURRENT_PAGE)
        self.clear_widget()

        self.search_page()

    # end of changing page methods

    # start of Handy Methods

    def display_popup(self, window_title, message, icon=QMessageBox.Critical):
        msg = QMessageBox()
        msg.setStyleSheet("font-size:%s;background: %s;color:%s;font-family:%s;" % (
                          self.font_size, self.colors['popup_background_color'],
                          self.colors['popup_text_color'], self.font))
        msg.setWindowIcon(QtGui.QIcon('app-icon.ico'))
        msg.setIcon(icon)
        msg.setWindowTitle(window_title)
        msg.setText(message)
        msg.exec_()

    def reload_page(self):
        """It will Reload the home page to get the latest update of table """
        self.clear_widget()
        self.home_page()

    def check_radio_buttons(self, radio_buttons):
        radio_btn_dic = {'By ID': 'emp_id', 'By Name': 'name', 'By Lastname': 'lname'}
        for rd_btn in radio_buttons:
            if rd_btn.isChecked():
                return radio_btn_dic[rd_btn.text()]
        return 'name'

    def check_page(self):
        if CURRENT_PAGE == "Login":
            self.go_to_login_page()
        if CURRENT_PAGE == "Home":
            self.go_to_home_page()
        if CURRENT_PAGE == "Search":
            self.go_to_search_page()
        if CURRENT_PAGE == "Add_Employee":
            self.go_to_add_employee_page()
        if CURRENT_PAGE == "Plot":
            self.go_to_plot_page()

    def clear_widget(self):
        for widget in widgets:
            if widgets[widget] != []:
                for i in range(0, len(widgets[widget])):
                    widgets[widget][i].hide()
            for i in range(0, len(widgets[widget])):
                widgets[widget].pop()
            # print(widgets)

    def authenticate(self):
        global usr
        try:
            signal, user = check_user(widgets['employee_fields'][0].text(), widgets['employee_fields'][1].text())
            if signal:
                usr = user.capitalize()
                self.go_to_home_page()
            else:
                self.display_popup('Authentication Failed', 'Wrong Username or Passowrd')
        except TypeError:
            self.display_popup('Authentication Failed', 'Please Enter Username and Password')

    # end of Handy Methods


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()
    sys.exit(app.exec_())
