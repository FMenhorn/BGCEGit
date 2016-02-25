#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QLabel>
#include <QString>

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_STEPFileSelector_clicked();

//    void on_lineEdit_textChanged(const QString &arg1);

    void on_IGSFileSelector_clicked();


    void on_runButton_clicked();

    void on_ForceEdit_textChanged(const QString &arg1);

    void on_RefinementEdit_textChanged(const QString &arg1);

    void checkInput();

private:
    Ui::MainWindow *ui;
    QString stpFile;
    QString igsFile;

    QString cropText(QLabel* curLabel, QString toCropString);
};

#endif // MAINWINDOW_H
