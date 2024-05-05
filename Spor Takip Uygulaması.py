import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, QListWidget, QMessageBox
import sqlite3

# Sporcu sınıfı, bir sporcu ve onun antrenman programlarını temsil eder
class Sporcu:
    def __init__(self, adı, spor_dalı):
        self.adı = adı  # Sporcunun adı
        self.spor_dalı = spor_dalı  # Spor dalı
        self.programlar = []  # Sporcunun antrenman programları

    # Sporcuya yeni bir antrenman programı ekler
    def program_oluştur(self, antrenman):
        self.programlar.append(antrenman)

    # Bir antrenman programındaki ilerlemeyi kaydeder
    def ilerleme_kaydet(self, antrenman_adı, ilerleme):
        for program in self.programlar:
            if program.adı == antrenman_adı:
                program.ilerleme = ilerleme

    # Sporcunun antrenman programlarına ilişkin bir rapor oluşturur
    def rapor_al(self):
        rapor = ""
        for program in self.programlar:
            rapor += f"Antrenman Adı: {program.adı}, İlerleme: {program.ilerleme}\n"  # Antrenman adı ve ilerleme
        return rapor

# Antrenman sınıfı, bir antrenmanın adı ve detaylarını temsil eder
class Antrenman:
    def __init__(self, adı, detayları):
        self.adı = adı  # Antrenmanın adı
        self.detayları = detayları  # Antrenmanın detayları
        self.ilerleme = None  # Antrenmanın ilerlemesi

# Spor Takip Uygulaması sınıfı, PyQt5 kullanarak bir grafik arayüz oluşturur
class SporTakipUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spor Takip Uygulaması")  # Arayüz başlığı
        self.setGeometry(100, 100, 600, 400)  # Arayüz boyutu ve konumu

        self.db_manager = DatabaseManager("spor_takip.db")  # Veritabanı yöneticisi
        self.sporcu_veritabani_islemleri = SporcuVeritabaniIslemleri(self.db_manager)  # Sporcu veritabanı işlemleri

        self.initUI()

    # Arayüzün ana bileşenlerini oluşturur
    def initUI(self):
        self.tab_widget = QTabWidget()  # Sekme widget'ı oluşturuldu

        # Sekmeler oluşturuldu ve tabloya eklendi
        self.tab_widget.addTab(self.create_tab_ui("Basketbol"), "Basketbol")
        self.tab_widget.addTab(self.create_tab_ui("Futbol"), "Futbol")
        self.tab_widget.addTab(self.create_tab_ui("Voleybol"), "Voleybol")

        main_layout = QVBoxLayout()  # Ana dikey düzen
        main_layout.addWidget(self.tab_widget)  # Sekmeler ana düzene eklendi
        self.setLayout(main_layout)  # Ana düzen belirlendi

    # Belirli bir spor dalı için sekme arayüzünü oluşturur
    def create_tab_ui(self, spor_dali):
        widget = QWidget()  # Widget oluşturuldu
        layout = QVBoxLayout()  # Dikey düzen oluşturuldu
        layout.addWidget(QLabel(f"{spor_dali} Sporcu Bilgileri"))  # Sporcu bilgileri etiketi eklendi
        
        # Etiketler ve giriş kutuları oluşturuldu
        ad_label = QLabel("Sporcu Adı:")
        ad_input = QLineEdit()
        antrenman_label = QLabel("Antrenman Adı:")
        antrenman_input = QLineEdit()
        detaylar_label = QLabel("Antrenman Detayları:")
        detaylar_input = QTextEdit()
        ilerleme_label = QLabel("İlerleme:")
        ilerleme_input = QLineEdit()
        program_olustur_button = QPushButton("Program Oluştur")
        kaydet_button = QPushButton("İlerleme Kaydet")
        rapor_al_button = QPushButton("Rapor Al")
        rapor_text = QTextEdit()

        # Etiketler ve giriş kutuları düzene eklendi
        layout.addWidget(ad_label)
        layout.addWidget(ad_input)
        layout.addWidget(antrenman_label)
        layout.addWidget(antrenman_input)
        layout.addWidget(detaylar_label)
        layout.addWidget(detaylar_input)
        layout.addWidget(ilerleme_label)
        layout.addWidget(ilerleme_input)
        layout.addWidget(program_olustur_button)
        layout.addWidget(kaydet_button)
        layout.addWidget(rapor_al_button)
        layout.addWidget(rapor_text)

        # Butonlara tıklama olayları bağlandı
        program_olustur_button.clicked.connect(lambda: self.program_olustur(ad_input.text(), antrenman_input.text(), detaylar_input.toPlainText(), rapor_text))
        kaydet_button.clicked.connect(lambda: self.ilerleme_kaydet(antrenman_input.text(), ilerleme_input.text(), rapor_text))
        rapor_al_button.clicked.connect(lambda: self.rapor_al(rapor_text))

        widget.setLayout(layout)  # Widget'a düzen eklendi
        return widget

    # Bir sporcu için yeni bir antrenman programı oluşturur
    def program_olustur(self, sporcu_adi, antrenman_adi, detaylar, rapor_text):
        if sporcu_adi and antrenman_adi and detaylar:
            self.sporcu_veritabani_islemleri.sporcu_ekle(sporcu_adi, self.tab_widget.tabText(self.tab_widget.currentIndex()))
            self.sporcu_veritabani_islemleri.antrenman_ekle(antrenman_adi, detaylar, self.tab_widget.currentIndex() + 1)
            rapor_text.append(f"{sporcu_adi} için {antrenman_adi} adlı antrenman oluşturuldu.")  # Program oluşturuldu mesajı
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen sporcu adı, antrenman adı ve detayları girin.")  # Hata mesajı

    # Bir antrenman programındaki ilerlemeyi kaydeder
    def ilerleme_kaydet(self, antrenman_adı, ilerleme, rapor_text):
        if antrenman_adı and ilerleme:
            self.sporcu_veritabani_islemleri.ilerleme_kaydet(self.tab_widget.currentIndex() + 1, antrenman_adı, ilerleme)
            rapor_text.append(f"{antrenman_adı} için ilerleme kaydedildi.")  # İlerleme kaydedildi mesajı
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen antrenman adı ve ilerlemeyi girin.")  # Hata mesajı

    # Sporcunun antrenman programlarına ilişkin bir rapor oluşturur ve gösterir
    def rapor_al(self, rapor_text):
        if rapor_text.toPlainText():  # Kaydedilen bilgi varsa
            rapor = self.sporcu_veritabani_islemleri.rapor_al(self.tab_widget.currentIndex() + 1)
            QMessageBox.information(self, "Rapor", rapor)  # Rapor alındı mesajı
        else:
            QMessageBox.warning(self, "Uyarı", "Henüz rapor alınacak bilgi yok.")  # Hata mesajı

# Veritabanı yönetimi sınıfı
class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    # Tabloları oluşturma işlevi
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sporcular (
                id INTEGER PRIMARY KEY,
                adı TEXT,
                spor_dalı TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS antrenmanlar (
                id INTEGER PRIMARY KEY,
                adı TEXT,
                detayları TEXT,
                sporcu_id INTEGER,
                FOREIGN KEY (sporcu_id) REFERENCES sporcular(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS raporlar (
                id INTEGER PRIMARY KEY,
                sporcu_id INTEGER,
                antrenman_id INTEGER,
                ilerleme TEXT,
                FOREIGN KEY (sporcu_id) REFERENCES sporcular(id),
                FOREIGN KEY (antrenman_id) REFERENCES antrenmanlar(id)
            )
        """)
        self.connection.commit()

    # Yeni bir sporcu ekler
    def add_sporcu(self, adı, spor_dalı):
        self.cursor.execute("INSERT INTO sporcular (adı, spor_dalı) VALUES (?, ?)", (adı, spor_dalı))
        self.connection.commit()

    # Yeni bir antrenman ekler
    def add_antrenman(self, adı, detayları, sporcu_id):
        self.cursor.execute("INSERT INTO antrenmanlar (adı, detayları, sporcu_id) VALUES (?, ?, ?)", (adı, detayları, sporcu_id))
        self.connection.commit()

    # İlerlemeyi kaydeder
    def add_ilerleme(self, sporcu_id, antrenman_id, ilerleme):
        self.cursor.execute("INSERT INTO raporlar (sporcu_id, antrenman_id, ilerleme) VALUES (?, ?, ?)", (sporcu_id, antrenman_id, ilerleme))
        self.connection.commit()

    # Veritabanı bağlantısını kapatma işlevi
    def close(self):
        self.connection.close()

# Sporcu veritabanı işlemleri
class SporcuVeritabaniIslemleri:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # Yeni bir sporcu ekler
    def sporcu_ekle(self, adı, spor_dalı):
        self.db_manager.add_sporcu(adı, spor_dalı)

    # Yeni bir antrenman ekler
    def antrenman_ekle(self, adı, detayları, sporcu_id):
        self.db_manager.add_antrenman(adı, detayları, sporcu_id)

    # İlerlemeyi kaydeder
    def ilerleme_kaydet(self, sporcu_id, antrenman_id, ilerleme):
        self.db_manager.add_ilerleme(sporcu_id, antrenman_id, ilerleme)

    # Sporcunun antrenman programlarına ilişkin bir rapor oluşturur
    def rapor_al(self, sporcu_id):
        self.db_manager.cursor.execute("""
            SELECT antrenmanlar.adı, raporlar.ilerleme
            FROM raporlar
            JOIN antrenmanlar ON raporlar.antrenman_id = antrenmanlar.id
            WHERE raporlar.sporcu_id = ?
        """, (sporcu_id,))
        raporlar = self.db_manager.cursor.fetchall()
        rapor_text = ""
        for rapor in raporlar:
            rapor_text += f"Antrenman Adı: {rapor[0]}, İlerleme: {rapor[1]}\n"
        return rapor_text

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Uygulama oluşturuldu
    window = SporTakipUygulamasi()  # Ana pencere oluşturuldu
    window.show()  # Ana pencere gösterildi
    sys.exit(app.exec_())  # Uygulama çalıştırıldı ve çıkış kodu alındı
