#include "vidgif_gui.h"
#include "ui_vidgif_gui.h"

vidgif_gui::vidgif_gui(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::vidgif_gui)
{
    ui->setupUi(this);
}

vidgif_gui::~vidgif_gui()
{
    delete ui;
}
