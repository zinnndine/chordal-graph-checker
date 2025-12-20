from PySide6.QtWidgets import ( QLabel ,QHBoxLayout ,
 QVBoxLayout  , QApplication , QMainWindow  ,
  QPushButton , QWidget  , QFileDialog  , QComboBox , QTextEdit 
  , QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,QStackedWidget ,QGraphicsLineItem ,QMessageBox )
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt , Signal
import sys
import random
import csv
import networkx
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
 
final_result = "" #output
win = [] #windows opened
vert = 0 #vertices number
adj = []
txt = ""
w=0

def remove_window(w):
    global win
    if w in win:
        win.remove(w)

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
    w.destroyed.connect(lambda :remove_window(w))
    w.data.connect(handle_data)   

#drawing the graph
class graph(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.canvas = QGraphicsScene()
        self.setScene(self.canvas)
    def drawing(self,n,adj):
        self.canvas = QGraphicsScene()
        self.setScene(self.canvas)
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
        print(2)
    def drawing_math(self,n,adj):
        self.canvas = QGraphicsScene()
        self.setScene(self.canvas)
        self.clean()
        nodes = [i for i in range(0,n)]
        arcs = [(i, k) for i in range(n) for k in range(n) if k in adj[i]]
        G = networkx.Graph()
        G.add_edges_from(arcs)
        G.add_nodes_from(nodes)
        s = 300
        f = 10
        positions = networkx.spring_layout(G,seed=4)
        for u , v in G.edges():
            x ,y = positions[u]
            z ,k = positions[v]
            edge = QGraphicsLineItem(x*s,y*s,z*s,k*s)
            edge.setPen(QPen(Qt.black,4))
            self.canvas.addItem(edge)
        for v in G.nodes():
            x,y = positions[v]
            node = QGraphicsEllipseItem(x*s-f,y*s-f,f*2,f*2)
            node.setBrush(QBrush(Qt.blue))
            self.canvas.addItem(node)

    def clean(self):
        self.canvas.clear()


class pilot(QWidget):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        llm=QVBoxLayout()
        self.setLayout(llm)
        llm.addWidget(self.canvas)

    def drawing_lib(self,n,adj):
        self.ax.clear()
        nodes = [i for i in range(0,n)]
        arcs = [(i, k) for i in range(n) for k in range(n) if k in adj[i] and i!=k]
        G = networkx.Graph()
        G.add_edges_from(arcs)
        G.add_nodes_from(nodes)
        pos = networkx.spring_layout(G,seed=4)  
        networkx.draw(G, pos, ax=self.ax, with_labels=False, node_color='skyblue', edge_color='gray', node_size=500)
        self.canvas.draw()

class input_window(QWidget):
    er = Signal(list, int)
    clo = Signal(int)
    def __init__(self):
        super().__init__()
        llm = QHBoxLayout()
        self.text = QTextEdit()
        self.text.setPlaceholderText("ex:[[0,1,1],[1,0,1],[1,1,0]]")
        xt = QLabel("write down adj matrix:")
        cmm = QVBoxLayout()
        cmm.addWidget(xt)
        cmm.addLayout(llm)
        botton = QPushButton("save")
        self.setLayout(cmm)
        llm.addWidget(self.text)
        llm.addWidget(botton)
        self.adja = []
        self.n = 0
        botton.clicked.connect(lambda: self.add_botton())
    def add_botton(self):
        g = self.text.toPlainText()
        rows = g.split("],[")
        for row in rows:
            row = row.replace("[","").replace("]","").replace(" ","")
            self.adja.append([int(x) for x in row.split(",")])
        self.n= len(self.adja[0])
        self.er.emit(self.adja, self.n)

        r =QMessageBox.information(self, "information", "Data is Saved!")
        if r == QMessageBox.StandardButton.Ok:
                self.close()
                self.clo.emit(0)



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
        b4.clicked.connect(self.inp)

        self.setLayout(layoutv)
        self.setWindowTitle("fill")
        self.setFixedSize(400,100)

        self.n = 0
        self.adja = None



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
                print(self.n)
                self.data.emit(self.adj, self.n)
                r= QMessageBox.information(self, "Success", "Data imported Successfully!")
                if r == QMessageBox.StandardButton.Ok:
                    self.close()
                    

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {str(e)}")
    
    def vvv(self):
        self.close()

    def inp(self):
        s= input_window()
        win.append(s)
        s.setWindowModality(Qt.ApplicationModal)
        s.er.connect(handle_data)
        s.show()
        s.destroyed.connect(lambda :remove_window(s))
        s.clo.connect(lambda: self.vvv())
        """QMessageBox.warning(self, "warning", "this feature is still in develepment!")"""

#function called when clicked run algorithme                
def run_algo(combo_vis,math,gh,rw,vis,):
    if vert == 0:
        QMessageBox.warning(window,"Warning" , "You must import Data first!")
    else :
        if vis == "only Qt" :
            gh.drawing(vert,adj)
            combo_vis.setCurrentIndex(0)
        elif vis == "using networkx":
            gh.drawing_math(vert,adj)
            combo_vis.setCurrentIndex(0)
        elif vis== "matpilot":
            combo_vis.setCurrentIndex(1)
            math.drawing_lib(vert,adj)


        sol = is_chordal_tarjan(adj)
        if sol == True:
            final_result = "this graph is chrodal"
        else :
            final_result = "this graph is not chrodal"
        rw.clear()
        rw.append(final_result)


def fix():
    if algo_list.currentIndex() == 1 :   
        QMessageBox.warning(window,"warning" ,"this methode is still in Dev")
        algo_list.setCurrentIndex(0)

def chang():
    global txt
    txt = visulazation.currentText()

#maincode
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
        
    visulazation = QComboBox()
    visulazation.addItems(["matpilot","only Qt","using networkx"])

    #check = QCheckBox()
    result = QTextEdit("Results will appear here...")
    result.setReadOnly(True) 
    view_new = QStackedWidget()
    view = graph()
    view_new.addWidget(view)
    math = pilot()
    view_new.addWidget(math)
    view_new.setFixedWidth(550)
    result_layout.addWidget(result)

    choose_layout.addWidget(algo_list)
    choose_layout.addWidget(visulazation)

    choose_layout.addStretch()
    #choose_layout.addWidget(text)
    #choose_layout.addWidget(check)

    butt_layout.addWidget(b2)
    butt_layout.addWidget(b1)

    right_layout.addWidget(view_new)

    left_layout.addLayout(butt_layout)
    left_layout.addLayout(choose_layout)
    left_layout.addLayout(result_layout)

    main_layout.addLayout(left_layout)
    main_layout.addLayout(right_layout)

    cen_wid.setLayout(main_layout)
    txt = visulazation.currentText()
    b1.clicked.connect(lambda: run_algo(view_new,math,view,result,txt))
    visulazation.currentTextChanged.connect(chang)

    b2.clicked.connect(fill)

    window.setCentralWidget(cen_wid)
    window.setWindowTitle("Chrodal Graph")
    window.resize(800,600)

    window.show()
    algo_list.currentTextChanged.connect(fix)

    app.exec()


