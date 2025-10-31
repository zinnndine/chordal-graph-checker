from PySide6.QtWidgets import ( QLabel ,QHBoxLayout ,
 QVBoxLayout , QCheckBox , QApplication , QMainWindow  ,
  QPushButton , QWidget , QListWidget , QFileDialog , QListView , QComboBox , QTextEdit 
  , QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem , QStackedWidget)
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt
import sys
import random
import csv


final_result = ""
win = []
w=0

# adjency list  [[1,2,3],[0,2],[0,1],[0]]

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





def fill():
    w = choose()                
    w.setWindowModality(Qt.ApplicationModal)
    w.show()
    win.append(w)
    

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

class choose(QWidget):
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


    def closed():
        del self.win[index(w)]

    def csv_func(self):
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Get data file", "", "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)")
            if not file_path:
                return
            with open(file_path, "r") as file:
                read = list(csv.reader(file))
                n =int(read[0][0])
                read.pop(0)
                adja = [[] for i in range(n)]
                for row in read :
                    if len(row)>=2: 
                        if int(row[1]) not in  adja[int(row[0])] :
                            adja[int(row[0])].append(int(row[1])) 
                        if int(row[0]) not in  adja[int(row[1])] : 
                            adja[int(row[1])].append(int(row[0]))

            return adja
                
def run_algo(gh,rw):
    adj =[[1,3],[0,2],[1,3],[0,2]]
      
    gh.drawing(4,adj)
    sol = is_chordal_tarjan(adj)
    if sol == True:
        final_result = "this graph is chrodal"
    else :
        final_result = "this graph is not chrodal"
    rw.clear()
    rw.append(final_result)
    
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


    text = QLabel("CHECK BOX")
    b1 = QPushButton("Start Algorithme",window)
    b2 = QPushButton("Fill Data",window)
    algo_list = QComboBox()
    algo_list.addItems(["Tarjan","Fulk-gurson"])
    check = QCheckBox()
    result = QTextEdit("Results will appear here...")
    result.setReadOnly(True) 
    view = graph()

    result_layout.addWidget(result)

    choose_layout.addWidget(algo_list)
    choose_layout.addWidget(text)
    choose_layout.addWidget(check)

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


