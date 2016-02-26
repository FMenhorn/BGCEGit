#ifndef INPUTVERIFICATOR_H
#define INPUTVERIFICATOR_H

#include "mainwindow.h"
#include <QString>

class InputVerificator
{
private:
    QString styleSheet = "QLabel {color : red}";
    MainWindow* ui;

public:
    InputVerificator(MainWindow* ui);

    static bool checkInputTopologyOptimization(QString igsName, QString igsPath, QString stpName, QString stpPath);

    static bool checkInputSurfaceFitting();
};

#endif // INPUTVERIFICATOR_H
