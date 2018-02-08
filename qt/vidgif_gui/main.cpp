#include "vidgif_gui.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    vidgif_gui w;
    w.show();

    return a.exec();
}
