import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt
import game  # 导入游戏模块


class LizardLogic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LizardLogic')
        self.setGeometry(100, 100, 1000, 700)
        self.setFixedSize(1000, 700)

        # 居中显示窗口
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # 设置背景图片
        palette = QPalette()
        bg_image = QPixmap('src/bg.jpg').scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(bg_image))
        self.setPalette(palette)

        # 初始化主窗口小部件
        self.init_widget = QWidget(self)
        self.setCentralWidget(self.init_widget)
        self.initUIComponents()

    def initUIComponents(self):
        layout = QVBoxLayout()
        layout.setSpacing(60)

        # 创建标签
        self.label = QLabel('欢迎来的杀戮尖塔! \n\n冒险家，请输入你的姓名：', self.init_widget)
        self.label.setFixedSize(400, 100)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont("KaiTi", 24)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")
        layout.addWidget(self.label, alignment=Qt.AlignCenter, stretch=0)

        # 创建输入框
        self.user_name = QLineEdit(self.init_widget)
        self.user_name.setFixedSize(400, 40)
        font = QFont("KaiTi", 18)
        self.user_name.setFont(font)
        self.user_name.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")
        layout.addWidget(self.user_name, alignment=Qt.AlignCenter, stretch=0)

        # 创建按钮
        self.button = QPushButton('开始冒险', self.init_widget)
        self.button.setFixedSize(400, 40)
        font = QFont("KaiTi", 20)
        self.button.setFont(font)
        self.button.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")
        self.button.clicked.connect(self.button_click)
        layout.addWidget(self.button, alignment=Qt.AlignCenter, stretch=0)

        layout.addStretch(1)  # 添加伸缩空间，确保布局填满窗口
        self.init_widget.setLayout(layout)

    def button_click(self):
        name = self.user_name.text()
        if name:
            QMessageBox.information(self, '欢迎', f'欢迎您，冒险家：{name}!')
            self.start_game(name)
        else:
            QMessageBox.warning(self, '提示', '冒险家，请输入你的姓名：')

    def start_game(self, player_name):
        # 清除初始界面小部件
        self.init_widget.hide()

        # 创建游戏界面
        self.game_widget = game.GameWidget(player_name, self)
        self.setCentralWidget(self.game_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LizardLogic()
    ex.show()
    sys.exit(app.exec_())
