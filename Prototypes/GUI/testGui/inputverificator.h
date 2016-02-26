#ifndef INPUTVERIFICATOR_H
#define INPUTVERIFICATOR_H

#include <QMainWindow>
#include <QString>
#include <QLineEdit>
#include <QLabel>
class InputVerificator
{
private:
    QString styleSheet = "QLabel {color : red}";

public:
    InputVerificator();
    bool isEmpty(QLineEdit*& qlineEdit, QLabel*& qlabel, QString errorMessage);
    bool checkFileName(QString file, QString name, QString type, QLabel*& errorField);
    bool areSame(QString stpName, QString igsName, QLabel*& STEPFileInput, QLabel*& IGSFileInput);

};

#endif // INPUTVERIFICATOR_H
