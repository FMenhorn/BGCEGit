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

    void on_IGSFileSelector_clicked();

private:
    Ui::MainWindow *ui;

    QString cropText(QLabel* curLabel, QString toCropString);
};

#endif // MAINWINDOW_H
