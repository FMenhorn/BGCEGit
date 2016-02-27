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

    QDoubleValidator* doubleValidator = new QDoubleValidator(0, 10000000000, 5, this);
    doubleValidator->setNotation(QDoubleValidator::StandardNotation);
    ui->ForceEdit->setValidator(doubleValidator);
    ui->FairnessWeight->setValidator(doubleValidator);
    ui->VertsPerPatch->setValidator(new QIntValidator(1, 1000000, this));
    ui->RefinementEdit->setValidator(new QIntValidator(0, 10, this));
    ui->Coarsening->setValidator(new QIntValidator(0, 10000000, this));

    ui->IGSFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/OpenCascade/TestGeometry/CantileverColoredNew/CantiLeverWithLoadAtEndSmallerMovedLoad.igs");
    ui->STEPFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/OpenCascade/TestGeometry/CantileverColoredNew/CantiLeverWithLoadAtEndSmallerMovedLoad.stp");

    ui->BooleanFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/PYTHON/Back2CAD/Cone.step");
    ui->STEPOutput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/GUI/build-testGui-Desktop-Debug/testBitch.step");
    igsFile = ui->IGSFileInput->text();
    stpFile = ui->STEPFileInput->text();
    booleanFile = ui->BooleanFileInput->text();
    stepOutputFile = ui->STEPFileInput->text();
    ui->RefinementEdit->setText("0");
    ui->ForceEdit->setText("1");
    ui->Coarsening->setText("2");
    ui->FairnessWeight->setText("0.5");
    this->hide_ErrorFields();
    //this->ui->progressBar->setMinimum(0);
    //this->ui->progressBar->setMaximum(0);
    //this->ui->progressBar->hide();
    //connect(&this->FutureWatcher, SIGNAL (finished()), this, SLOT (slot_finished()));

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
    //this->ui->progressBar->hide();
}

void MainWindow::on_STEPFileSelector_clicked()
{
    QStringList fileNames;
    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("STP File (*.stp)"));
    if (fileNames.size() == 1) {
        stpFile = fileNames.first();
        ui->STEPFileInput->setText(StringHelper::cropText(ui->STEPFileInput, stpFile));
        ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");
    } else {
        ui->STEPFileInput->setText("Select ONE stp input file!");
        ui->STEPFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::on_IGSFileSelector_clicked()
{
    QStringList fileNames;
    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("IGS File (*.igs)"));
    if (fileNames.size() == 1) {
        igsFile = fileNames.first();
        ui->IGSFileInput->setText(StringHelper::cropText(ui->IGSFileInput, igsFile));
        ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    } else {
        ui->IGSFileInput->setText("Select ONE igs input file!");
        ui->IGSFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::on_runButton_clicked()
{
    ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");
    this->hide_ErrorFields();


    QString igsPath, igsName;
    QString stpPath, stpName;

    StringHelper::getPathAndName(stpFile, stpName, stpPath);
    StringHelper::getPathAndName(igsFile, igsName, igsPath);

    //if (this->checkInput(igsName, stpName)){
        QString forceScaling = ui->ForceEdit->text();
        QString refinementLevel = ui->RefinementEdit->text();

        //this->ui->progressBar->show();

        /** Start the Voxelization Script **/
        std::string parameterString = stpPath.toStdString() + " " + stpName.toStdString() + " " + forceScaling.toStdString() + " " + refinementLevel.toStdString();
        std::string scriptCADToVoxel = "./../../CADTopOp.sh " + parameterString;
        std::cout << scriptCADToVoxel << std::endl;
        system(scriptCADToVoxel.c_str());

        //QFuture<void> future = QtConcurrent::run(&this->scriptCaller, &ScriptCaller::callScript, scriptCADToVoxel);
        //this->FutureWatcher.setFuture(future);

        /** Start ToPy **/
        parameterString = stpName.toStdString();
        std::string scriptToPy = "./../../ToPyRunner.sh " + parameterString;
        system(scriptToPy.c_str());

        /** Start the Surface Fitting, Extraction and Back2CAD **/
        std::string cellsAndDimensionsPath = "./../../PYTHON/NURBSReconstruction";
        std::string outputFileString = stepOutputFile.toStdString();
        std::string booleanFileString = booleanFile.toStdString();
        std::string fairnessWeight = ui->FairnessWeight->text().toStdString();
        std::string coarseningFactor = ui->Coarsening->text().toStdString();
        parameterString = cellsAndDimensionsPath + " " + outputFileString + " " + fairnessWeight + " " + coarseningFactor + " " + booleanFileString;
        std::string scriptPython = "python ./../../PYTHON/NURBSReconstruction/runningScript.py " + parameterString;
        std::cout << scriptPython << std::endl;
        system(scriptPython.c_str());
   //}
}

bool MainWindow::checkInput(QString igsName, QString stpName){
    InputVerificator verificator;
    QString boolName, boolPath;
    StringHelper::getPathAndName(booleanFile, boolName, boolPath);

    bool flag = true;

    flag = flag && verificator.isEmpty(ui->Coarsening, ui->ErrorField_coarsening, "Please enter the coarsening");
    flag = verificator.isEmpty(ui->FairnessWeight, ui->ErrorField_fairness, "Please enter the fairness weight") && flag;
    flag = verificator.isEmpty(ui->ForceEdit, ui->ErrorField_force, "Please enter the force") && flag;
    flag = verificator.isEmpty(ui->RefinementEdit, ui->ErrorField_refinement, "Please enter the refinement") && flag;

    flag = verificator.areSame(stpName, igsName, ui->STEPFileInput, ui->IGSFileInput) && flag;
    flag = verificator.checkFileName(this->stpFile, stpName, ".stp", ui->STEPFileInput) && flag;
    flag = verificator.checkFileName(this->igsFile, igsName, ".igs", ui->IGSFileInput) && flag;
    flag = verificator.checkFileName(this->booleanFile, boolName, ".step", ui->BooleanFileInput) && flag;
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

void MainWindow::on_BooleanFileSelector_clicked()
{
    QStringList fileNames;
    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("STEP File (*.step)"));
    if (fileNames.size() == 1 && fileNames.first().size() > 0) {
        booleanFile = fileNames.first();
        ui->BooleanFileInput->setText(StringHelper::cropText(ui->BooleanFileInput, booleanFile));
        ui->BooleanFileInput->setStyleSheet("QLabel { Color : black }");
    } else {
        booleanFile = "";
        ui->BooleanFileInput->setText("Select ONE step input file!");
        ui->BooleanFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::hide_ErrorFields(){
    ui->ErrorField_force->hide();
    ui->ErrorField_refinement->hide();
    ui->ErrorField_coarsening->hide();
    ui->ErrorField_fairness->hide();
}
