#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFileDialog>
#include <QMessageBox>
#include <QFuture>
#include <QtConcurrent/QtConcurrent>
#include <QtGui>

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
        ui->STEPFileInput->setText(this->cropText(ui->STEPFileInput, stpFile));
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
        ui->IGSFileInput->setText(this->cropText(ui->IGSFileInput, igsFile));
        ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    }else{
        ui->IGSFileInput->setText("Select ONE igs input file!");
        ui->IGSFileInput->setStyleSheet("QLabel { Color : red }");
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
    ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");

    QString igsPath, igsName;
    QString stpPath, stpName;

    this->getPathAndName(stpFile, stpName, stpPath);
    this->getPathAndName(igsFile, igsName, igsPath);

    if(this->checkInput(igsName, igsPath, stpName, stpPath) & this->checkInputSurfaceFitting()){

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

bool MainWindow::checkInputSurfaceFitting(){
    QString coarsening = ui->Coarsening->text();
    QString vertsPerPatch = ui->VertsPerPatch->text();
    QString fairnessWeight = ui->FairnessWeight->text();
    QString styleSheet = "QLabel {color : red}";

    bool flag = true;

    if (coarsening.isEmpty()){
        ui->ErrorField_coarsening->setText("Please enter the coarsening!");
        ui->ErrorField_coarsening->setStyleSheet(styleSheet);
        ui->ErrorField_coarsening->show();
        flag = false;
    }

    if (fairnessWeight.isEmpty()){
        ui->ErrorField_fairness->setText("Please enter the fairness weight!");
        ui->ErrorField_fairness->setStyleSheet(styleSheet);
        ui->ErrorField_fairness->show();
        flag = false;
    }

    if (vertsPerPatch.isEmpty()){
        ui->ErrorField_vertsPerPatch->setText("Please enter the No of verts per patch!");
        ui->ErrorField_vertsPerPatch->setStyleSheet(styleSheet);
        ui->ErrorField_vertsPerPatch->show();
        flag = false;
    }
    return flag;

}

bool MainWindow::checkInput(QString igsName, QString igsPath, QString stpName, QString stpPath){
    QMessageBox messageBox;
    QString styleSheet = "QLabel {color : red}";
    QString forceScaling = ui->ForceEdit->text();
    QString refinement = ui->RefinementEdit->text();
    ui->ErrorField_force->hide();
    ui->ErrorField_refinement->hide();

    bool flag = true;

    if (forceScaling.isEmpty()) {
        ui->ErrorField_force->setText("Please enter the force!");
        ui->ErrorField_force->setStyleSheet(styleSheet);
        ui->ErrorField_force->show();
        flag = false;
    }

    if (refinement.isEmpty()) {
        ui->ErrorField_refinement->setText("Please enter the refinement!");
        ui->ErrorField_refinement->setStyleSheet(styleSheet);
        ui->ErrorField_refinement->show();
        flag = false;
    }

    if (!igsFile.endsWith(".igs")){
        ui->IGSFileInput->setText("Please choose the .igs file!");
        ui->IGSFileInput->setStyleSheet(styleSheet);
        flag = false;
    } else {

        if (igsName.contains(".")){
            ui->IGSFileInput->setText("Filename can not contain a dot!");
            ui->IGSFileInput->setStyleSheet(styleSheet);
            flag = false;
        }
    }

    if (!stpFile.endsWith(".stp")){
        ui->STEPFileInput->setText("Please choose the .stp file!");
        ui->STEPFileInput->setStyleSheet(styleSheet);
        messageBox.setFixedSize(500,200);
        flag = false;
    } else {

        if (stpName.contains(".")){
            ui->STEPFileInput->setText("Filename can not contain a dot!");
            ui->STEPFileInput->setStyleSheet(styleSheet);
            flag = false;
        }
    }

    if(stpName.compare(igsName)!=0){
        ui->STEPFileInput->setStyleSheet(styleSheet);
        ui->IGSFileInput->setStyleSheet(styleSheet);
        messageBox.critical(0, "Error", "Filenames are not equal!");
        messageBox.setFixedSize(500,200);
        flag = false;
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

void MainWindow::on_Output_selector_clicked()
{
    QString fileName;
    fileName = QFileDialog::getSaveFileName(this, tr("Save File"), QDir::currentPath(),tr("STEP File (*.step)"));
    if(fileName.size()>=1){
        if(!(fileName.endsWith(".step"))){
            fileName = fileName + tr(".step");
        }
        stepOutputFile = fileName;
        ui->STEPOutput->setText(this->cropText(ui->STEPOutput, stepOutputFile));
        ui->STEPOutput->setStyleSheet("QLabel { Color : black }");
    }else{
        ui->STEPOutput->setText("Select ONE stp input file!");
        ui->STEPOutput->setStyleSheet("QLabel { Color : red }");
    }
}
