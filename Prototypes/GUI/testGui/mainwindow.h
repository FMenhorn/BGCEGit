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

    void on_ForceEdit_textChanged(const QString &arg1);

    void on_RefinementEdit_textChanged(const QString &arg1);

    bool checkInput(QString igsName, QString igsPath, QString stpName, QString stpPath);

    void slot_finished();

    void getPathAndName(QString fullPath, QString &name, QString &path);

    void on_Output_selector_clicked();

    void on_Coarsening_textChanged(const QString &arg1);

    void on_FairnessWeight_textChanged(const QString &arg1);

    void on_VertsPerPatch_textChanged(const QString &arg1);

private:
    Ui::MainWindow *ui;

    QFutureWatcher<void> FutureWatcher;
    QString stpFile;
    QString igsFile;
    QString stepOutputFile;

    QString cropText(QLabel* curLabel, QString toCropString);

    ScriptCaller scriptCaller;

    QGraphicsScene logoScene;
    QPixmap* logoPicture = new QPixmap("../testGui/images/bgceCSEsccs_logo.png");
    QGraphicsPixmapItem logoItem;
};

#endif // MAINWINDOW_H
