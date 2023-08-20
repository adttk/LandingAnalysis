import sys
import excel2img
import io
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

from Preparation import Preparation
from Viz import Viz
from Model_Evaluate import Model_Evaluate
from KNN_Implement import KNN_Implement

from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class MainGUI(QDialog):

    def __init__(self):
        super(MainGUI, self).__init__()
        loadUi("User_Interface.ui", self)

        self.unseen = None
        self.preparation = Preparation()
        self.viz = Viz()
        self.eval = Model_Evaluate()
        self.KNN = KNN_Implement()

        self.browseRawData.clicked.connect(self.BrowseRawData)
        self.PreparationButton.clicked.connect(self.Preparation)

        self.GenerateVizButton.clicked.connect(self.GenerateViz)
        self.comboBox.activated.connect(self.Visualize)
        self.AnalyzeView.setAlignment(QtCore.Qt.AlignCenter)

        self.BrowseFileEval.clicked.connect(self.BrowseEval)
        self.EvaluationButton.clicked.connect(self.ModelEval)
        self.DisplayDataTrainButton.clicked.connect(self.DisplayTrain)
        self.TestWithPredictionButton.clicked.connect(self.TestWithPrediction)

        self.PredictButton.clicked.connect(self.Predict)

    def printToConsole(self, text):
        cursor = self.textPreparation.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text + "\n"+"\n")
        self.textPreparation.setTextCursor(cursor)
        self.textPreparation.ensureCursorVisible()

    def printToEval(self, text):
        cursor = self.EvalText.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text + "\n")
        self.EvalText.setTextCursor(cursor)
        self.EvalText.ensureCursorVisible()

    def BrowseRawData(self):
        RawData = QFileDialog.getOpenFileName(
            self, 'Open file', 'C:', 'CSV(*.csv)')
        path = RawData[0]
        df = pd.read_csv(path)
        self.preparation.set_raw_data(df)
        self.PathLinePrepare.setText(path)
        self.printToConsole("Load raw data is done ")
        self.printToConsole('Raw data displayed \n')

        model = TableModel(self.preparation.raw_data)
        self.tableViewPreparation.setModel(model)

    def Preparation(self):
        if (self.preparation.raw_data is not None):
            self.preparation.drop_columns()
            self.preparation.get_touchdown()
            self.preparation.get_tier1()
            self.preparation.add_runway()
            self.preparation.data_with_runway.to_csv('clean_data.csv')

            if (self.preparation.data_with_runway is None):
                self.printToConsole('preparations are not finished')

            else:

                model = TableModel(self.preparation.data_with_runway)
                self.tableViewPreparation.setModel(model)
                self.printToConsole('Preparation is done')

                check_data = self.preparation.check_data(
                    self.preparation.data_tier1)
                self.printToConsole(check_data)

        else:
            self.printToConsole('data has not been input by user')

    def GenerateViz(self):

        VizData = QFileDialog.getOpenFileName(
            self, 'Open file', 'C:', 'CSV(*.csv)')
        path = VizData[0]
        df = pd.read_csv(path)
        self.viz.set_dataset(df)
        self.PathLineViz.setText(path)

        if (self.viz.dataset is not None):

            scatter = self.viz.scatter_plot()
            scatter.savefig('Data_Visualization/Scatter/scatter.png')
            scatter.close()

            count_airlines = self.viz.get_pivot_count_airline()
            count_airlines.to_csv(
                "Data_Visualization/Airlines/Count_of_airlines_flight/Count_of_airline_flights.csv", index=False)
            histAirline = self.viz.histogram(count_airlines)
            histAirline.savefig(
                'Data_Visualization/Airlines/Count_of_airlines_flight/Count_of_airline_flights.png')
            histAirline.close()

            count_aircraft = self.viz.get_pivot_count_aircraft()
            count_aircraft.to_csv(
                "Data_Visualization/Aircraft/Count_of_aircraft_Flight/Count_of_aircraft_flights.csv")
            histAircraft = self.viz.histogram(count_aircraft)
            histAircraft.savefig(
                'Data_Visualization/Aircraft/Count_of_aircraft_Flight/Count_of_aircraft_flights.png')
            histAircraft.close()

            count_aircraft = self.viz.get_pivot_count_aircraft()
            count_aircraft.to_csv(
                "Data_Visualization/Aircraft/Count_of_aircraft_Flight/Count_of_aircraft_flights.csv")
            histAircraft = self.viz.histogram(count_aircraft)
            histAircraft.savefig(
                'Data_Visualization/Aircraft/Count_of_aircraft_Flight/Count_of_aircraft_flights.png')
            histAircraft.close()

            airlines_of_all = self.viz.get_pivot_airline_of_all()
            airlines_of_all.to_csv(
                "Data_Visualization/Airlines/Abnormality_by_all_flights/Abnormality_by_all_flights.csv")
            heatmap1 = self.viz.heatmap(airlines_of_all)
            self.viz.adjustExcel(
                airlines_of_all, heatmap1, "Data_Visualization/Airlines/Abnormality_by_all_flights/heatmap1.xlsx")
            excel2img.export_img("Data_Visualization/Airlines/Abnormality_by_all_flights/heatmap1.xlsx",
                                 "Data_Visualization/Airlines/Abnormality_by_all_flights/heatmap1.png")

            aircraft_of_all = self.viz.get_pivot_aircraft_of_all()
            aircraft_of_all.to_csv(
                "Data_Visualization/Aircraft/Abnormality_by_all_flights/Abnormality_by_all_flights.csv")
            heatmap3 = self.viz.heatmap(aircraft_of_all)
            self.viz.adjustExcel(
                aircraft_of_all, heatmap3, "Data_Visualization/Aircraft/Abnormality_by_all_flights/heatmap3.xlsx")
            excel2img.export_img("Data_Visualization/Aircraft/Abnormality_by_all_flights/heatmap3.xlsx",
                                 "Data_Visualization/Aircraft/Abnormality_by_all_flights/heatmap3.png")

            airlines_of_self = self.viz.get_pivot_airline_of_self()
            airlines_of_self.to_csv(
                "Data_Visualization/Airlines/Abnormality_by_airline_flight/Abnormality_by_airline_flights.csv")
            heatmap2 = self.viz.heatmap(airlines_of_self)
            self.viz.adjustExcel(
                airlines_of_self, heatmap2, "Data_Visualization/Airlines/Abnormality_by_airline_flight/heatmap2.xlsx")
            excel2img.export_img("Data_Visualization/Airlines/Abnormality_by_airline_flight/heatmap2.xlsx",
                                 "Data_Visualization/Airlines/Abnormality_by_airline_flight/heatmap2.png")

            aircraft_of_self = self.viz.get_pivot_aircraft_of_self()
            aircraft_of_self.to_csv(
                "Data_Visualization/Aircraft/Abnormality_by_aircraft_flight/Abnormality_by_aircraft_flight.csv")
            heatmap4 = self.viz.heatmap(aircraft_of_self)
            self.viz.adjustExcel(
                aircraft_of_self, heatmap4, "Data_Visualization/Aircraft/Abnormality_by_aircraft_flight/heatmap4.xlsx")
            excel2img.export_img("Data_Visualization/Aircraft/Abnormality_by_aircraft_flight/heatmap4.xlsx",
                                 "Data_Visualization/Aircraft/Abnormality_by_aircraft_flight/heatmap4.png")

            image_path = 'Data_Visualization/Scatter/scatter.png'
            self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))
            self.comboBox.setCurrentIndex(0)
        else:
            return None

    def Visualize(self):

        if (self.viz.dataset is not None):

            if (self.comboBox.currentIndex() == 0):
                image_path = 'Data_Visualization/Scatter/scatter.png'
                self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))

            elif (self.comboBox.currentIndex() == 1):
                image_path = 'Data_Visualization/Airlines/Count_of_airlines_flight/Count_of_airline_flights.png'
                self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))

            elif (self.comboBox.currentIndex() == 2):
                image_path = 'Data_Visualization/Aircraft/Count_of_aircraft_Flight/Count_of_aircraft_flights.png'
                self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))

            elif (self.comboBox.currentIndex() == 3):
                image_path = "Data_Visualization/Airlines/Abnormality_by_all_flights/heatmap1.png"
                self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))

            elif (self.comboBox.currentIndex() == 4):
                image_path = "Data_Visualization/Aircraft/Abnormality_by_all_flights/heatmap3.png"
                self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))

            elif (self.comboBox.currentIndex() == 5):
                image_path = "Data_Visualization/Airlines/Abnormality_by_airline_flight/heatmap2.png"
                self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))

            elif (self.comboBox.currentIndex() == 6):
                image_path = "Data_Visualization/Aircraft/Abnormality_by_aircraft_flight/heatmap4.png"
                self.AnalyzeView.setPixmap(QtGui.QPixmap(image_path))
        else:
            return None

    def BrowseEval(self):
        EvalData = QFileDialog.getOpenFileName(
            self, 'Open file', 'C:', 'CSV(*.csv)')
        path = EvalData[0]
        self.PathLineEval.setText(path)
        df = pd.read_csv(path)
        self.eval.set_dataset(df)
        model = TableModel(df)
        self.tableViewEval.setModel(model)

    def ModelEval(self):

        if (self.eval.df is not None):

            train = float(self.InputTrain.text())
            test = float(self.InputTest.text())
            n = int(self.InputN.text())

            self.eval.KNN(train, test, n)
            KNN_eval = self.eval.KnnEval()
            self.printToEval(KNN_eval)

            image_path = self.eval.confusion_matrix()
            self.EvalView.setPixmap(QtGui.QPixmap(image_path))

        else:
            self.printToEval('data has not been input by user \n \n ')

    def DisplayTrain(self):
        if (self.eval.df is not None):
            model = TableModel(self.eval.df_train)
            self.tableViewEval.setModel(model)
        else:
            self.printToEval('data has not been input by user \n \n ')

    def TestWithPrediction(self):
        if (self.eval.df is not None):
            model = TableModel(self.eval.df_test)
            self.tableViewEval.setModel(model)
        else:
            self.printToEval('data has not been input by user \n \n ')

    def Predict(self):
        unseenData = QFileDialog.getOpenFileName(
            self, 'Open file', 'C:', 'CSV(*.csv)')
        path = unseenData[0]
        self.PathLinePredict.setText(path)
        df = pd.read_csv(path)
        self.KNN.set_unseen(df)

        df_prediction = self.KNN.Predict()
        model = TableModel(df_prediction)
        self.tableViewPredict.setModel(model)


app = QApplication(sys.argv)
mainwindow = MainGUI()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle('Landing Analysis')
widget.setWindowIcon(QIcon('icon/logo.png'))
widget.setFixedHeight(561)
widget.setFixedWidth(1301)
widget.show()
sys.exit(app.exec_())
