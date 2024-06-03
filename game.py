import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt
import random


class GameWidget(QWidget):
    def __init__(self, player_name, parent=None):
        super().__init__(parent)
        self.player_name = player_name
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Score layout
        score_layout = QHBoxLayout()
        self.player_score_label = QLabel('玩家: 0', self)
        self.player_score_label.setFixedSize(200, 50)
        self.player_score_label.setAlignment(Qt.AlignLeft)
        font = QFont("KaiTi", 24)
        self.player_score_label.setFont(font)
        self.player_score_label.setStyleSheet("color: white;")
        score_layout.addWidget(self.player_score_label)

        self.computer_score_label = QLabel('电脑: 0', self)
        self.computer_score_label.setFixedSize(200, 50)
        self.computer_score_label.setAlignment(Qt.AlignRight)
        font = QFont("KaiTi", 24)
        self.computer_score_label.setFont(font)
        self.computer_score_label.setStyleSheet("color: white;")
        score_layout.addWidget(self.computer_score_label)
        main_layout.addLayout(score_layout)

        # Character images layout
        character_layout = QHBoxLayout()
        self.player_image = QLabel(self)
        self.player_image.setFixedSize(300, 250)
        self.player_image.setPixmap(QPixmap('src/player.png').scaled(self.player_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.player_image.setAlignment(Qt.AlignCenter)
        character_layout.addWidget(self.player_image, alignment=Qt.AlignCenter)

        self.computer_image = QLabel(self)
        self.computer_image.setFixedSize(325, 310)
        self.computer_image.setPixmap(QPixmap('src/computer.png').scaled(self.computer_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.computer_image.setAlignment(Qt.AlignCenter)
        character_layout.addWidget(self.computer_image, alignment=Qt.AlignCenter)
        main_layout.addLayout(character_layout)

        # Choices layout
        choices_layout = QHBoxLayout()
        choices = ['剪刀', '石头', '布', '斯波克', '蜥蜴']
        images = ['src/jd.jpg', 'src/st.jpg', 'src/b.jpg', 'src/sbk.jpg', 'src/xy.jpg']

        for choice, image in zip(choices, images):
            button = QPushButton(choice, self)
            button.setFixedSize(170, 240)
            button.setStyleSheet(f"""
                QPushButton {{
                    color: white;
                    background-image: url({image});
                    background-repeat: no-repeat;
                    background-position: center;
                    border: none;
                }}
            """)
            button.clicked.connect(lambda _, c=choice: self.make_choice(c))
            choices_layout.addWidget(button)
        main_layout.addLayout(choices_layout)

        self.setLayout(main_layout)
        self.player_score = 0
        self.computer_score = 0

    def make_choice(self, player_choice):
        choices = ['剪刀', '石头', '布', '斯波克', '蜥蜴']
        computer_choice = random.choice(choices)
        result = self.determine_winner(player_choice, computer_choice)
        if result == 'player':
            self.player_score += 1
            self.player_score_label.setText(f'玩家: {self.player_score}')
        elif result == 'computer':
            self.computer_score += 1
            self.computer_score_label.setText(f'电脑: {self.computer_score}')
        QMessageBox.information(self, '结果', f'你选择了: {player_choice}\n电脑选择了: {computer_choice}\n{self.get_result_message(result)}')

        if self.player_score + self.computer_score == 5:
            if self.player_score > self.computer_score:
                QMessageBox.information(self, '游戏结束', '你赢了！')
                self.reset_game()
            else:
                QMessageBox.information(self, '游戏结束', '电脑赢了！')
                self.reset_game()

    def determine_winner(self, player_choice, computer_choice):
        rules = {
            '剪刀': ['布', '蜥蜴'],
            '石头': ['剪刀', '蜥蜴'],
            '布': ['石头', '斯波克'],
            '斯波克': ['剪刀', '石头'],
            '蜥蜴': ['布', '斯波克']
        }
        if player_choice == computer_choice:
            return 'tie'
        elif computer_choice in rules[player_choice]:
            return 'player'
        else:
            return 'computer'

    def get_result_message(self, result):
        if result == 'player':
            return '你赢了这局！'
        elif result == 'computer':
            return '电脑赢了这局！'
        else:
            return '这一局是平局！'

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_score_label.setText('玩家: 0')
        self.computer_score_label.setText('电脑: 0')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameWidget('玩家1')
    ex.show()
    sys.exit(app.exec_())

