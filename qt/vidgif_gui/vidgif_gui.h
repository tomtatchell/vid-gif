#ifndef VIDGIF_GUI_H
#define VIDGIF_GUI_H

#include <QMainWindow>

namespace Ui {
class vidgif_gui;
}

class vidgif_gui : public QMainWindow
{
    Q_OBJECT

public:
    explicit vidgif_gui(QWidget *parent = 0);
    ~vidgif_gui();

private:
    Ui::vidgif_gui *ui;
};

#endif // VIDGIF_GUI_H
