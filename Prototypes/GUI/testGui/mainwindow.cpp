#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFileDialog>
#include <QMessageBox>

#include <iostream>

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
    stpFile = fileNames.first();
    ui->STEPFileInput->setText(this->cropText(ui->STEPFileInput, stpFile));
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
    igsFile = fileNames.first();
    ui->IGSFileInput->setText(this->cropText(ui->IGSFileInput, igsFile));
}

QString MainWindow::cropText(QLabel* curLabel, QString toCropString){
    int width = curLabel->width();
    QFontMetrics metrics = curLabel->fontMetrics();
    QString croppedText = metrics.elidedText(toCropString, Qt::ElideLeft, width);
    return croppedText;
}

void MainWindow::on_runButton_clicked()
{
    this->checkInput();

    float forceScaling = ui->ForceEdit->text().toFloat();
    int refinementLevel = ui->RefinementEdit->text().toInt();
}

void MainWindow::on_ForceEdit_textChanged(const QString &arg1)
{
    ui->ForceEdit->setText(arg1);
}

void MainWindow::on_RefinementEdit_textChanged(const QString &arg1)
{
    ui->RefinementEdit->setText(arg1);
}

bool MainWindow::checkInput(QString igsName, QString igsPath, QString stpName, QString stpPath){
    QString forceScaling = ui->ForceEdit->text();
    QString refinement = ui->RefinementEdit->text();
    /*QString igsName;
    QString igsPath;
    QString stpName;
    QString stpPath;*/
    bool flag = true;

    if (forceScaling.isEmpty()) {
        QMessageBox messageBox;
        messageBox.critical(0,"Error","Please enter the force!");
        messageBox.setFixedSize(500,200);
        flag = false;
    }

    if (refinement.isEmpty()) {
        QMessageBox messageBox;
        messageBox.critical(0,"Error","Please enter the refinement!");
        messageBox.setFixedSize(500,200);
        flag = false;
    }

    if (!igsFile.endsWith(".igs")){
        QMessageBox messageBox;
        messageBox.critical(0,"Error","Please choose the .igs file!");
        messageBox.setFixedSize(500,200);
        flag = false;
    } else {
       // getPathAndName(igsFile, igsName, igsPath);
        if (igsName.contains(".")){
            QMessageBox messageBox;
            messageBox.critical(0, "Error", "Filename can not contain a dot! Please, choose another .igs file!");
            messageBox.setFixedSize(500,200);
            flag = false;
        }
    }

    if (!stpFile.endsWith(".stp")){
        QMessageBox messageBox;
        messageBox.critical(0,"Error","Please choose the .stp file!");
        messageBox.setFixedSize(500,200);
        flag = false;
    } else {
       // getPathAndName(stpFile, stpName, stpPath);
        if (stpName.contains(".")){
            QMessageBox messageBox;
            messageBox.critical(0, "Error", "Filename can not contain a dot! Please, choose another .stp file!");
            messageBox.setFixedSize(500,200);
            flag = false;
        }
    }

return flag;
}

void MainWindow::getPathAndName(QString fullPath, QString &name, QString &path){
    QStringList igsPathParsed = fullPath.split( "/" );
    path = "";
    for (int i = 0; i < igsPathParsed.length() - 1; i++){
        path.push_back(igsPathParsed.value(i) + "/");
    }

    name = igsPathParsed.value(igsPathParsed.length() - 1);
    name = name.left(name.length() - 4);

}
