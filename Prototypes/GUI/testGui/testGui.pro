#-------------------------------------------------
#
# Project created by QtCreator 2016-02-25T09:57:17
#
#-------------------------------------------------

QT       += core gui

CONFIG += c++11

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = testGui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h \
    ScriptCaller.h

FORMS    += mainwindow.ui
