#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "inputverificator.h"

#include <QFileDialog>
#include <QMessageBox>
#include <QFuture>
#include <QtConcurrent/QtConcurrent>
#include <QtGui>
#include <QFont>
#include <QThreadPool>

#include "stringhelper.h"

#include <iostream>

#include <stdlib.h>     //for using the function sleep
#include <stdio.h>
#include <time.h>
#include <unistd.h>

#include <chrono>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QDoubleValidator* doubleValidator = new QDoubleValidator(0, 10000000000, 5, this);
    doubleValidator->setNotation(QDoubleValidator::StandardNotation);
    ui->ForceEdit->setValidator(doubleValidator);
    ui->FairnessWeight->setValidator(doubleValidator);
    ui->RefinementEdit->setValidator(new QIntValidator(0, 10, this));
    ui->Coarsening->setValidator(new QIntValidator(0, 10000000, this));

   /* ui->IGSFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/OpenCascade/TestGeometry/CantileverColoredNew/CantiLeverWithLoadAtEndSmallerMovedLoad.igs");
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
    ui->FairnessWeight->setText("0.5");*/
    this->hide_ErrorFields();
    //this->ui->progressBar->setMinimum(0);
    //this->ui->progressBar->setMaximum(0);
    //this->ui->progressBar->hide();
    this->ui->startFreeCadButton->hide();

    this->ui->VoxelizerDial->setValue(0);
    this->ui->VoxelizerDial->setDisabled(true);
    this->ui->ToPyDial->setValue(0);
    this->ui->ToPyDial->setDisabled(true);
    this->ui->NurbsDial->setValue(0);

    this->ui->NurbsDial->setDisabled(true);
    //connect(&this->FutureWatcher, SIGNAL (finished()), this, SLOT (slot_finished()));

    this->ui->logoView->setScene(&logoScene);
    logoItem.setPixmap(*logoPicture);
    logoScene.addItem(&logoItem);
    this->ui->logoView->show();

    /*ui->IGSFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/OpenCascade/TestGeometry/CantileverColoredNew/CantiLeverWithLoadAtEndSmallerMovedLoad.igs");
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
    ui->FairnessWeight->setText("0.5");*/
}

MainWindow::~MainWindow()
{
    delete this->logoPicture;
    delete ui;
}

void MainWindow::on_STEPFileSelector_clicked()
{
    QStringList fileNames;

    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("STEP File (*.step)"));
    if(fileNames.size()==1){
        stpFile = fileNames.first();
        ui->STEPFileInput->setText(StringHelper::cropText(ui->STEPFileInput, stpFile));
        ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");
    }else{
        ui->STEPFileInput->setText("Select ONE step input file!");
        ui->STEPFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::on_IGSFileSelector_clicked()
{
    QStringList fileNames;

    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("IGES File (*.iges)"));
    if(fileNames.size()==1){
        igsFile = fileNames.first();
        ui->IGSFileInput->setText(StringHelper::cropText(ui->IGSFileInput, igsFile));
        ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    }else{
        ui->IGSFileInput->setText("Select ONE iges input file!");
        ui->IGSFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::on_runButton_clicked()
{
    ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");
    this->hide_ErrorFields();
    this->resetDials();

    QString igsPath, igsName;
    QString stpPath, stpName;
    QString stpOutputPath, stpOutputName;

    StringHelper::getPathAndName(stpFile, stpName, stpPath);
    StringHelper::getPathAndName(stepOutputFile, stpOutputName, stpOutputPath);
    StringHelper::getPathAndName(igsFile, igsName, igsPath);

    //if (this->checkInput(igsName, stpName)){

    //std::cout << "CHECK STILL DISABLED" << std::endl;
    //this->checkInput(igsName, stpName)
    if (this->checkInput(igsName, stpName)){
        QString forceScaling = ui->ForceEdit->text();
        QString refinementLevel = ui->RefinementEdit->text();

        QFont boldFont("Cantarell", 11, QFont::Bold);
        QFont normalFont("Cantarell", 11, QFont::Normal);
        QThreadPool qpool;
        QFuture<void> future;

        /** Start the Voxelization Script **/
        std::string parameterString = stpPath.toStdString() + " " + stpName.toStdString() + " " + forceScaling.toStdString() + " " + refinementLevel.toStdString() + " " + (isFixtureFileSupplied ? "1" : "0");
        std::string scriptCADToVoxel = "./../../CADTopOp.sh " + parameterString;

        future = QtConcurrent::run(&qpool, &this->scriptCaller, &ScriptCaller::callScript, scriptCADToVoxel);

        this->ui->voxelizationLabel->setFont( boldFont );
        this->rotateDial(this->ui->VoxelizerDial, future);
        this->ui->voxelizationLabel->setFont( normalFont );
        /**                                 **/

        /** Start ToPy **/
        parameterString = stpName.toStdString();
        std::string scriptToPy = "./../../ToPyRunner.sh " + parameterString;

        future = QtConcurrent::run(&qpool, &this->scriptCaller, &ScriptCaller::callScript, scriptToPy);

        this->ui->topologyOptimizationLabel->setFont( boldFont );
        this->rotateDial(this->ui->ToPyDial, future);
        this->ui->topologyOptimizationLabel->setFont( normalFont );
        /**                                 **/


        std::chrono::time_point<std::chrono::system_clock> start;
        std::chrono::time_point<std::chrono::system_clock> end;
        std::chrono::duration<double> elapsedSeconds;
        start = std::chrono::system_clock::now();
        /** Start the Surface Fitting, Extraction and Back2CAD **/
        std::string cellsAndDimensionsPath = "./../../PYTHON/NURBSReconstruction";
        std::string outputFileString = stpOutputPath.toStdString()+"/"+stpOutputName.toStdString();
        std::string fairnessWeight = ui->FairnessWeight->text().toStdString();
        std::string coarseningFactor = ui->Coarsening->text().toStdString();
        std::string fixedFileFullPathNameString = this->isFixtureFileSupplied ? stpPath.toStdString() + stpName.toStdString() + "_Fixed.step" : "";
        std::string booleanFileString = this->isOptimizationDomainSupplied ? stpPath.toStdString() + stpName.toStdString() + "_ToOptimize.step" : "";
        parameterString = cellsAndDimensionsPath + " " + outputFileString + " " + fairnessWeight + " " + coarseningFactor + " "+ fixedFileFullPathNameString + " " + booleanFileString;
        std::string scriptPython = "python ./../../PYTHON/NURBSReconstruction/runningScript.py " + parameterString;

        std::cout << scriptPython << std::endl;
        system(scriptPython.c_str());
   //}


        future = QtConcurrent::run(&qpool, &this->scriptCaller, &ScriptCaller::callScript, scriptPython);

        this->ui->surfaceFittingLabel->setFont( boldFont );
        this->rotateDial(this->ui->NurbsDial, future);
        this->ui->surfaceFittingLabel->setFont( normalFont );
        /**                                 **/
        end = std::chrono::system_clock::now();
        elapsedSeconds = end-start;
        std::cout << "###SURFACE-Fitting: Elapsed Time: " << elapsedSeconds.count() << " Ref: " << refinementLevel.toStdString() << std::endl;

        this->ui->startFreeCadButton->show();
    }
}

void MainWindow::resetDials(){
    this->ui->VoxelizerDial->setStyleSheet( "QDial {background:transparent }" );
    this->ui->ToPyDial->setStyleSheet( "QDial {background:transparent }" );
    this->ui->NurbsDial->setStyleSheet( "QDial {background:transparent }" );
}


void MainWindow::rotateDial(QDial* dial, const QFuture<void>& future){
     int rotationDirection = 1;
     dial->setStyleSheet( "QDial {background-color : orange }" );
     while(future.isRunning()){
         if( dial->value() == dial->maximum()){
             rotationDirection = -1;
         }else if( dial->value() == dial->minimum()){
             rotationDirection = 1;
         }
         dial->setValue(dial->value()+rotationDirection );
         QCoreApplication::processEvents();
         usleep(70000);
     }
     while(dial->value() < dial->maximum()){
         dial->setValue( dial->value()+1 );
         QCoreApplication::processEvents();
         usleep(7000);
     }
     dial->setStyleSheet( "QDial {background-color : green }" );
     dial->setValue(dial->maximum());
     QCoreApplication::processEvents();
}

void MainWindow::setValueOfToPyDial(int value){
    std::cout << "We are actually using this function with value: " << value << std::endl;
    this->ui->ToPyDial->setValue(value % (this->ui->ToPyDial->maximum()+1));
}

bool MainWindow::checkInput(QString igsName, QString stpName){
    InputVerificator verificator;
    QString boolName, boolPath;

    bool flag = true;

    flag = flag && verificator.isEmpty(ui->Coarsening, ui->ErrorField_coarsening, "Please enter the coarsening");
    flag = verificator.isEmpty(ui->FairnessWeight, ui->ErrorField_fairness, "Please enter the fairness weight") && flag;
    flag = verificator.isEmpty(ui->ForceEdit, ui->ErrorField_force, "Please enter the force") && flag;
    flag = verificator.isEmpty(ui->RefinementEdit, ui->ErrorField_refinement, "Please enter the refinement") && flag;

    flag = verificator.areSame(stpName, igsName, ui->STEPFileInput, ui->IGSFileInput) && flag;

    flag = verificator.checkFileName(this->stpFile, stpName, ".step", ui->STEPFileInput) && flag;
    flag = verificator.checkFileName(this->igsFile, igsName, ".iges", ui->IGSFileInput) && flag;
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

void MainWindow::hide_ErrorFields(){
    ui->ErrorField_force->hide();
    ui->ErrorField_refinement->hide();
    ui->ErrorField_coarsening->hide();
    ui->ErrorField_fairness->hide();
}

void MainWindow::on_startFreeCadButton_clicked()
{
    QString outputFile;
    QString outputPath;
    StringHelper::getPathAndName(stepOutputFile, outputFile, outputPath);
    std::string freeCADCommand = "freecad " + outputFile.toStdString() + ".step " + " FusionForBoolean.step &";
    system(freeCADCommand.c_str());
}

void MainWindow::on_checkBox_stateChanged(int newState)
{
    if(newState){
        this->ui->checkBoxWarningLabel->setText("Make sure that fixture file name is of the form \'StepFileName\'_Fixed.step!");
        this->ui->checkBoxWarningLabel->setStyleSheet("QLabel { Color : red }");
        this->isFixtureFileSupplied = 1;
    }else{
        this->ui->checkBoxWarningLabel->setText("");
        this->isFixtureFileSupplied = 0;
    }
}

void MainWindow::on_checkBox_2_stateChanged(int newState)
{
    if(newState){
        this->ui->checkBoxWarningLabel_2->setText("Make sure that fixture file name is of the form \'StepFileName\'_ToOptimize.step!");
        this->ui->checkBoxWarningLabel_2->setStyleSheet("QLabel { Color : red }");
        this->isOptimizationDomainSupplied = 1;
    }else{
        this->ui->checkBoxWarningLabel_2->setText("");
        this->isOptimizationDomainSupplied = 0;
    }
}
