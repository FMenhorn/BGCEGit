#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "inputverificator.h"

#include <QFileDialog>
#include <QMessageBox>
#include <QFuture>
#include <QtConcurrent/QtConcurrent>
#include <QtGui>

#include "stringhelper.h"

#include <iostream>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->ForceEdit->setValidator( new QDoubleValidator(0, 100000, 7, this));
    ui->FairnessWeight->setValidator(new QDoubleValidator(0, 100000, 7, this));
    ui->VertsPerPatch->setValidator(new QIntValidator(1, 1000000, this));
    ui->RefinementEdit->setValidator(new QIntValidator(0, 10, this));
    ui->Coarsening->setValidator(new QIntValidator(0, 10000000, this));

    this->ui->progressBar->setMinimum(0);
    this->ui->progressBar->setMaximum(0);
    this->ui->progressBar->hide();
    connect(&this->FutureWatcher, SIGNAL (finished()), this, SLOT (slot_finished()));
    ui->ErrorField_force->hide();
    ui->ErrorField_refinement->hide();
    ui->ErrorField_coarsening->hide();
    ui->ErrorField_fairness->hide();
    ui->ErrorField_vertsPerPatch->hide();

    this->ui->logoView->setScene(&logoScene);
    logoItem.setPixmap(*logoPicture);
    logoScene.addItem(&logoItem);
    this->ui->logoView->show();
}
MainWindow::~MainWindow()
{
    delete this->logoPicture;
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
        ui->STEPFileInput->setText(StringHelper::cropText(ui->STEPFileInput, stpFile));
        ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");
    }else{
        ui->STEPFileInput->setText("Select ONE stp input file!");
        ui->STEPFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::on_IGSFileSelector_clicked()
{
    QStringList fileNames;
    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("IGS File (*.igs)"));
    if(fileNames.size()==1){
        igsFile = fileNames.first();
        ui->IGSFileInput->setText(StringHelper::cropText(ui->IGSFileInput, igsFile));
        ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    }else{
        ui->IGSFileInput->setText("Select ONE igs input file!");
        ui->IGSFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::on_runButton_clicked()
{
    ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");

    QString igsPath, igsName;
    QString stpPath, stpName;

    StringHelper::getPathAndName(stpFile, stpName, stpPath);
    StringHelper::getPathAndName(igsFile, igsName, igsPath);

    if (this->checkInput()){
        QString forceScaling = ui->ForceEdit->text();
        QString refinementLevel = ui->RefinementEdit->text();

        std::string parameterString = stpPath.toStdString() + " " + stpName.toStdString() + " " + forceScaling.toStdString() + " " + refinementLevel.toStdString();
        std::string script = "./../../CADTopOp.sh " + parameterString;
        std::cout << script << std::endl;

        this->ui->progressBar->show();
        QFuture<void> future = QtConcurrent::run(&this->scriptCaller, &ScriptCaller::callScript, script);
        this->FutureWatcher.setFuture(future);
        //system(script.c_str());
    }
}

void MainWindow::on_ForceEdit_textChanged(const QString &arg1)
{
    ui->ForceEdit->setText(arg1);
}

void MainWindow::on_RefinementEdit_textChanged(const QString &arg1)
{
    ui->RefinementEdit->setText(arg1);
}

void MainWindow::on_Coarsening_textChanged(const QString &arg1)
{
    ui->Coarsening->setText(arg1);
}

void MainWindow::on_FairnessWeight_textChanged(const QString &arg1)
{
    ui->FairnessWeight->setText(arg1);
}

void MainWindow::on_VertsPerPatch_textChanged(const QString &arg1)
{
    ui->VertsPerPatch->setText(arg1);
}

bool MainWindow::checkInput(){
    InputVerificator verificator;
    bool flag = true;
    QString igsPath, igsName;
    QString stpPath, stpName;

    this->getPathAndName(stpFile, stpName, stpPath);
    this->getPathAndName(igsFile, igsName, igsPath);
    flag = flag && verificator.isEmpty(ui->Coarsening, ui->ErrorField_coarsening, "Please enter the coarsening!");
    flag = verificator.isEmpty(ui->FairnessWeight, ui->ErrorField_fairness, "Please enter the fairness weight") && flag;
    flag = verificator.isEmpty(ui->ForceEdit, ui->ErrorField_force, "Please enter the force") && flag;
    flag = verificator.isEmpty(ui->RefinementEdit, ui->ErrorField_refinement, "Please enter the refinement") && flag;
    flag = verificator.isEmpty(ui->VertsPerPatch, ui->ErrorField_vertsPerPatch, "Please enter the number of vertices per patch!") && flag;

    flag = verificator.areSame(stpName, igsName, ui->STEPFileInput, ui->IGSFileInput) && flag;
    flag = verificator.checkFileName(this->stpFile, stpName, ".stp", ui->STEPFileInput) && flag;
    flag = verificator.checkFileName(this->igsFile, igsName, ".igs", ui->IGSFileInput) && flag;
    return flag;


}

void MainWindow::on_Output_selector_clicked()
{
    QString fileName;
    fileName = QFileDialog::getSaveFileName(this, tr("Save File"), QDir::currentPath(),tr("STEP File (*.step)"));
    if(fileName.size()>=1){
        if(!(fileName.endsWith(".step"))){
            fileName = fileName + tr(".step");
        }
        stepOutputFile = fileName;
        ui->STEPOutput->setText(StringHelper::cropText(ui->STEPOutput, stepOutputFile));
        ui->STEPOutput->setStyleSheet("QLabel { Color : black }");
    } else {
        ui->STEPOutput->setText("Select ONE stp input file!");
        ui->STEPOutput->setStyleSheet("QLabel { Color : red }");
    }
}
