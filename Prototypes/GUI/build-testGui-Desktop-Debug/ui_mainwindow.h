/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QPushButton *STEPFileSelector;
    QLabel *STEPFileInput;
    QPushButton *IGSFileSelector;
    QLabel *IGSFileInput;
    QWidget *layoutWidget;
    QFormLayout *formLayout_2;
    QLabel *label_2;
    QLineEdit *RefinementEdit;
    QPushButton *runButton;
    QWidget *widget;
    QFormLayout *formLayout;
    QLabel *label;
    QLineEdit *ForceEdit;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(689, 300);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        STEPFileSelector = new QPushButton(centralWidget);
        STEPFileSelector->setObjectName(QStringLiteral("STEPFileSelector"));
        STEPFileSelector->setGeometry(QRect(15, 40, 111, 31));
        STEPFileInput = new QLabel(centralWidget);
        STEPFileInput->setObjectName(QStringLiteral("STEPFileInput"));
        STEPFileInput->setGeometry(QRect(150, 50, 521, 21));
        STEPFileInput->setWordWrap(false);
        IGSFileSelector = new QPushButton(centralWidget);
        IGSFileSelector->setObjectName(QStringLiteral("IGSFileSelector"));
        IGSFileSelector->setGeometry(QRect(15, 100, 111, 31));
        IGSFileInput = new QLabel(centralWidget);
        IGSFileInput->setObjectName(QStringLiteral("IGSFileInput"));
        IGSFileInput->setGeometry(QRect(150, 100, 521, 21));
        layoutWidget = new QWidget(centralWidget);
        layoutWidget->setObjectName(QStringLiteral("layoutWidget"));
        layoutWidget->setGeometry(QRect(20, 180, 221, 29));
        formLayout_2 = new QFormLayout(layoutWidget);
        formLayout_2->setSpacing(6);
        formLayout_2->setContentsMargins(11, 11, 11, 11);
        formLayout_2->setObjectName(QStringLiteral("formLayout_2"));
        formLayout_2->setHorizontalSpacing(16);
        formLayout_2->setContentsMargins(0, 0, 0, 0);
        label_2 = new QLabel(layoutWidget);
        label_2->setObjectName(QStringLiteral("label_2"));
        QFont font;
        font.setPointSize(14);
        font.setBold(true);
        font.setWeight(75);
        label_2->setFont(font);

        formLayout_2->setWidget(0, QFormLayout::LabelRole, label_2);

        RefinementEdit = new QLineEdit(layoutWidget);
        RefinementEdit->setObjectName(QStringLiteral("RefinementEdit"));

        formLayout_2->setWidget(0, QFormLayout::FieldRole, RefinementEdit);

        runButton = new QPushButton(centralWidget);
        runButton->setObjectName(QStringLiteral("runButton"));
        runButton->setGeometry(QRect(30, 210, 99, 27));
        widget = new QWidget(centralWidget);
        widget->setObjectName(QStringLiteral("widget"));
        widget->setGeometry(QRect(20, 150, 221, 29));
        formLayout = new QFormLayout(widget);
        formLayout->setSpacing(6);
        formLayout->setContentsMargins(11, 11, 11, 11);
        formLayout->setObjectName(QStringLiteral("formLayout"));
        formLayout->setHorizontalSpacing(72);
        formLayout->setContentsMargins(0, 0, 0, 0);
        label = new QLabel(widget);
        label->setObjectName(QStringLiteral("label"));
        label->setFont(font);

        formLayout->setWidget(0, QFormLayout::LabelRole, label);

        ForceEdit = new QLineEdit(widget);
        ForceEdit->setObjectName(QStringLiteral("ForceEdit"));

        formLayout->setWidget(0, QFormLayout::FieldRole, ForceEdit);

        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 689, 25));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0));
        STEPFileSelector->setText(QApplication::translate("MainWindow", "Select STP File", 0));
        STEPFileInput->setText(QApplication::translate("MainWindow", "STEP File", 0));
        IGSFileSelector->setText(QApplication::translate("MainWindow", "Select IGS File", 0));
        IGSFileInput->setText(QApplication::translate("MainWindow", "IGS File", 0));
        label_2->setText(QApplication::translate("MainWindow", "Refinement:", 0));
        runButton->setText(QApplication::translate("MainWindow", "Run", 0));
        label->setText(QApplication::translate("MainWindow", "Force:", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
