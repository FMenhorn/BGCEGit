#include "inputverificator.h"
#include <QMessageBox>
#include <QString>
#include <QLineEdit>

InputVerificator::InputVerificator()
{

}


bool InputVerificator::isEmpty(QLineEdit*& qlineEdit, QLabel*& errorField, QString errorString){
    QString text = qlineEdit->text();
    errorField->hide();
    bool flag = true;

    if (text.isEmpty()){
        errorField->setText(errorString);
        errorField->setStyleSheet(styleSheet);
        errorField->show();
        flag = false;
    }

    return flag;
}

bool InputVerificator::areSame(QString stpName, QString igsName, QLabel*& STEPFileInput, QLabel*& IGSFileInput)
{
    QMessageBox messageBox;
    bool flag = true;

    if(stpName.compare(igsName)!=0){
        STEPFileInput->setStyleSheet(styleSheet);
        IGSFileInput->setStyleSheet(styleSheet);
        messageBox.critical(0, "Error", "Filenames are not equal!");
        messageBox.setFixedSize(500,200);
        flag = false;
    }
    return flag;
}

bool InputVerificator::checkFileName(QString file, QString name, QString type, QLabel*& errorField)
{
    bool flag = true;

    if (!file.endsWith(type)){
        errorField->setText("Please choose the " + type + " file!");
        errorField->setStyleSheet(styleSheet);
        flag = false;
    } else {
        if (name.contains(".")){
            errorField->setText("Filename can not contain a dot!");
            errorField->setStyleSheet(styleSheet);
            flag = false;
        }
    }
    return flag;

}
