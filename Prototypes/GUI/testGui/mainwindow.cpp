#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFileDialog>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->ForceEdit->setValidator( new QDoubleValidator(0, 100000, 5, this));
    ui->RefinementEdit->setValidator(new QIntValidator(0, 10, this));
   // ui->pushButton;
}
MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_STEPFileSelector_clicked()
{
    QStringList fileNames;
    while(fileNames.size() != 1){
        fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("STP File (*.stp)"));
        if(fileNames.size() != 1){
            QMessageBox messageBox;
            messageBox.critical(0,"Error","Please select ONE stp input file!");
            messageBox.setFixedSize(500,200);
        }
    }
    ui->STEPFileInput->setText(this->cropText(ui->STEPFileInput, fileNames.first()));
}

void MainWindow::on_IGSFileSelector_clicked()
{
    QStringList fileNames;
    while(fileNames.size() != 1){
        fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("IGS File (*.igs)"));
        if(fileNames.size() != 1){
            QMessageBox messageBox;
            messageBox.critical(0,"Error","Please select ONE igs input file!");
            messageBox.setFixedSize(500,200);
        }
    }
    ui->IGSFileInput->setText(this->cropText(ui->IGSFileInput, fileNames.first()));
}

QString MainWindow::cropText(QLabel* curLabel, QString toCropString){
    int width = curLabel->width();
    QFontMetrics metrics = curLabel->fontMetrics();
    QString croppedText = metrics.elidedText(toCropString, Qt::ElideLeft, width);
    return croppedText;
}

/*void MainWindow::on_lineEdit_textChanged(const QString &arg1)
{

}

void MainWindow::on_pushButton_clicked()
{

}*/
