from PySide6.QtWidgets import ( QLabel ,QHBoxLayout ,
 QVBoxLayout , QCheckBox , QApplication , QMainWindow  ,
  QPushButton , QWidget , QListWidget , QFileDialog , QListView , QComboBox , QTextEdit 
  , QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem ,QMessageBox , QStackedWidget)
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt , Signal
import sys
import random
import csv


final_result = "" #output
win = [] #windows opened
vert = 0 #vertices number
adj = []
w=0

# adjency list =  [[1,2,3],[0,2],[0,1],[0]]  where in index i there is all nodes adjacent to i

#the main algorithme
def is_chordal_tarjan(adj):
    n = len(adj)
    W = list(range(n))  
    N = []             

    while len(W) > 0:
        max_common = -1
        chosen = W[0]

        for i in range(len(W)):
            v = W[i]
            count = 0
            for u in adj[v]:
                if u in N:
                    count += 1
            if count > max_common:
                max_common = count
                chosen = v

        neighbors_in_N = []
        for j in range(len(N)):
            for i in range(len(adj[chosen])):
                u = adj[chosen][i]
                if u == N[j]:
                    neighbors_in_N.append(u)
                    break

        for i in neighbors_in_N:
            for j in  neighbors_in_N:
                if j in adj[i] :
                    0
                else:
                    if i!=j:
                       return False

        N.append(chosen)

        for i in range(len(W)):
            if W[i] == chosen:
                W.pop(i)
                break

    return True


def handle_data(a,b):
    global adj, vert
    adj = a
    vert = b

#the function called when pressed fill
def fill():
    global adj , vert
    w = choose()                
    w.setWindowModality(Qt.ApplicationModal)
    w.show()
    win.append(w)
    w.data.connect(handle_data)   

#drawing the graph
class graph(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.canvas = QGraphicsScene()
        self.setScene(self.canvas)
    def drawing(self,n,adj):
        self.clean()
        nodes = [i for i in range(0,n)]
        arcs = [(i, k) for i in range(n) for k in range(n) if k in adj[i]]
        lines = [0 for i in range(n) for k in range(n) if k in adj[i]]

        r = True
        x=[]
        y=[]
        rn = 10 if n< 150 else  11
        diff = 16 if n < 150 else (8 if n < 4000 else 6)
        for i in range(0,n): 
            x_t = random.randint(1+i,i*rn+100)
            y_t = random.randint(1+i,i*rn+100)
            while r :
                if all(abs(x_t - xi) >= diff for xi in x):
                    x.append(x_t)
                    y.append(y_t)
                    r = False
                    break
                elif all(abs(y_t - yi) >= diff for yi in y):
                    x.append(x_t)
                    y.append(y_t)
                    r = False
                    break
                else:
                        x_t = random.randint(1+i,i*10+250)
                        y_t = random.randint(1+i,i*10+250)
            r = True


            nodes[i] = QGraphicsEllipseItem( x[i], y[i], 10, 10)
            nodes[i].setBrush(QBrush(Qt.red))                   
            nodes[i].setPen(QPen(Qt.black, 1))  
            self.canvas.addItem(nodes[i])
            s = x
            f = y
        b=0
        for f in arcs:
            lines[b] = QGraphicsLineItem(x[f[0]]+5, y[f[0]]+5, x[f[1]]+5, y[f[1]]+5)
            lines[b].setPen(QPen(Qt.black, 2))
            lines[b].setZValue(-1)
            self.canvas.addItem(lines[b])
            

            b=b+1


    def clean(self):
        self.canvas.clear()


#windows used for filling data
class choose(QWidget):
    data = Signal(list, int)
    def __init__(self):
        super().__init__()
        layoutv = QVBoxLayout()
        layouth = QHBoxLayout()
        text = QLabel("choose the mthode of filling")
        b3 = QPushButton("using csv file",self)
        b4 = QPushButton("using input",self)
        layoutv.addWidget(text)
        layoutv.addLayout(layouth)
        layoutv.addStretch()
        layouth.addWidget(b3)
        layouth.addWidget(b4)
        b3.clicked.connect(self.csv_func)
        self.setLayout(layoutv)
        self.setWindowTitle("fill")
        self.resize(400,100)
        self.destroyed.connect(self.closed)

        self.n = 0
        self.adja = None

    def closed(self):
        del win[index(self)]

    def csv_func(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Get data file", "", "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)")
        if not file_path:
            return
        
        try:
            with open(file_path, "r") as file:
                read = list(csv.reader(file))
                self.n = int(read[0][0])
                read.pop(0) 
                self.adj = [[] for _ in range(self.n)]
                for row in read:
                    if len(row) >= 2:
                        u = int(row[0])
                        v = int(row[1])
                        if v not in self.adj[u]:
                            self.adj[u].append(v)
                        if u not in self.adj[v]:
                            self.adj[v].append(u)
                self.data.emit(self.adj, self.n)
                QMessageBox.information(window, "Success", "Data imported Successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {str(e)}")


#function called when clicked run algorithme                
def run_algo(gh,rw):
    if vert == 0:
        QMessageBox.warning(window,"Warning" , "You must select a file first!")
    else :
        gh.drawing(vert,adj)
        sol = is_chordal_tarjan(adj)
        if sol == True:
            final_result = "this graph is chrodal"
        else :
            final_result = "this graph is not chrodal"
        rw.clear()
        rw.append(final_result)

#main-code 
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    cen_wid = QWidget()

    main_layout = QHBoxLayout()
    butt_layout = QHBoxLayout()
    choose_layout = QHBoxLayout()
    result_layout = QHBoxLayout()
    left_layout = QVBoxLayout()
    right_layout = QVBoxLayout()

    #text = QLabel("CHECK BOX")
    b1 = QPushButton("Start Algorithme",window)
    b2 = QPushButton("Fill Data",window)
    algo_list = QComboBox()
    algo_list.addItems(["Tarjan","Fulk-gurson"])
    #check = QCheckBox()
    result = QTextEdit("Results will appear here...")
    result.setReadOnly(True) 
    view = graph()

    result_layout.addWidget(result)

    choose_layout.addWidget(algo_list)
    choose_layout.addStretch()
    #choose_layout.addWidget(text)
    #choose_layout.addWidget(check)

    butt_layout.addWidget(b2)
    butt_layout.addWidget(b1)

    right_layout.addWidget(view)

    left_layout.addLayout(butt_layout)
    left_layout.addLayout(choose_layout)
    left_layout.addLayout(result_layout)

    main_layout.addLayout(left_layout)
    main_layout.addLayout(right_layout)

    cen_wid.setLayout(main_layout)

    b1.clicked.connect(lambda: run_algo(view,result))
    b2.clicked.connect(fill)

    window.setCentralWidget(cen_wid)
    window.setWindowTitle("Chrodal Graph")
    window.resize(800,600)

    window.show()
    app.exec()


