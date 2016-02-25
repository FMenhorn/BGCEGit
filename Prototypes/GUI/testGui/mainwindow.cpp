#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFileDialog>
#include <QMessageBox>
#include <QFuture>
#include <QtConcurrent/QtConcurrent>
#include <QtGui>
#include <QImage>

#include <iostream>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->ForceEdit->setValidator( new QDoubleValidator(0, 100000, 5, this));
    ui->RefinementEdit->setValidator(new QIntValidator(0, 10, this));
   // ui->pushButton;

    this->ui->progressBar->setMinimum(0);
    this->ui->progressBar->setMaximum(0);
    //this->ui->progressBar->hide();
    connect(&this->FutureWatcher, SIGNAL (finished()), this, SLOT (slot_finished()));
}
MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::slot_finished()
{
    this->ui->progressBar->hide();
}

void MainWindow::on_STEPFileSelector_clicked()
{
    QStringList fileNames;
    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("STP File (*.stp)"));
    if(fileNames.size()==1){
        stpFile = fileNames.first();
        ui->STEPFileInput->setText(this->cropText(ui->STEPFileInput, stpFile));
    }else{
        ui->STEPFileInput->setText("ERROR: Select ONE stp input file!");
    }
}

void MainWindow::on_IGSFileSelector_clicked()
{
    QStringList fileNames;
    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("IGS File (*.igs)"));
    if(fileNames.size()==1){
        igsFile = fileNames.first();
        ui->IGSFileInput->setText(this->cropText(ui->IGSFileInput, igsFile));
    }else{
        ui->IGSFileInput->setText("ERROR: Select ONE igs input file!");
    }
}

QString MainWindow::cropText(QLabel* curLabel, QString toCropString){
    int width = curLabel->width();
    QFontMetrics metrics = curLabel->fontMetrics();
    QString croppedText = metrics.elidedText(toCropString, Qt::ElideLeft, width);
    return croppedText;
}

void MainWindow::on_runButton_clicked()
{

    //CROPPING


    //CHECKING
    this->checkInput();

    QString forceScaling = ui->ForceEdit->text();
    QString refinementLevel = ui->RefinementEdit->text();

    std::string path = "~/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/OpenCascade/TestGeometry/CantileverColoredNew/";
    std::string fileName = "CantiLeverWithLoadAtEndSmallerMovedLoad";
    std::string parameterString = path + " " + fileName + " " + forceScaling.toStdString() + " " + refinementLevel.toStdString();
    std::string script = "./../../CADTopOp.sh " + parameterString;
    std::cout << script << std::endl;

    this->ui->progressBar->show();
    //system(script.c_str());
    QThreadPool pool;
    QFuture<void> future = QtConcurrent::run(&pool, system, script.c_str());
    this->FutureWatcher.setFuture(future);
}

void MainWindow::on_ForceEdit_textChanged(const QString &arg1)
{
    ui->ForceEdit->setText(arg1);
}

void MainWindow::on_RefinementEdit_textChanged(const QString &arg1)
{
    ui->RefinementEdit->setText(arg1);
}

void MainWindow::checkInput(){
    //TODO
}
