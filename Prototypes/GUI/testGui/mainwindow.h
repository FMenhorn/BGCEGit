#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QLabel>
#include <QString>
#include <QFutureWatcher>

#include <QMainWindow>

#include <QImage>
#include <QPixmap>
#include <QGraphicsPixmapItem>
#include <QGraphicsScene>

#include "ScriptCaller.h"

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

    void on_runButton_clicked();

    void slot_finished();

    bool checkInput(QString igsName, QString stpName);

    void on_Output_selector_clicked();

    void on_BooleanFileSelector_clicked();

    void hide_ErrorFields();

private:
    Ui::MainWindow *ui;

    QFutureWatcher<void> FutureWatcher;
    QString stpFile;
    QString igsFile;
    QString booleanFile = "";
    QString stepOutputFile;

    ScriptCaller scriptCaller;

    QGraphicsScene logoScene;
    QPixmap* logoPicture = new QPixmap("../testGui/images/bgceCSEsccs_logo.png");
    QGraphicsPixmapItem logoItem;
};

#endif // MAINWINDOW_H
