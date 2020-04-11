from xml.dom import pulldom
#import pickledb
import json
import cProfile


idAgente = 0
idPublicacion = 0
agentes = {}
agentesInverso = {}
agentesPublicaciones = {}
enlaces = {}
enlacesInverso = {}
enlacesSinAsignar = {}


class AbstractReference:
    def __init__(self):
        global idPublicacion 
        # atributos comunes para todas las referencias
        # author|editor|title|booktitle|pages|year|address|journal|volume|number|month|url|ee|cdrom|cite|publisher|note|crossref|isbn|series|school|chapter|publnr
        idPublicacion += 1
        self._id = idPublicacion
        self.key = None
        self.mdate = None
        self.publtype = None
        self.cdate = None        
        self.authors = None
        self.editors = None                
        self.title = None
        self.booktitle = None
        self.pages = None
        self.year = None   
        #self.yearInicial = None
        #self.yearFinal = None
        self.address = None
        self.journal = None
        self.volume = None
        self.number = None
        self.month = None
        self.url = None
        self.ee = None
        self.cdrom = None
        self.cite = None
        self.publisher = None
        self.note = None
        self.crossref = None
        self.isbn = None
        self.series = None
        self.school = None
        self.chapter = None
        self.publnr = None       
      
    def serialize(self,fileHandler,listOfTypes):
        global agentesPublicaciones 
        global agentes
        #if type(self) in listaElementosValidados:
        if any(isinstance(self, x) for x in listaElementosValidados):
            if self.authors is not None:
                for i in self.authors:
                    agentesPublicaciones[i] = agentes[i]
                    agentes[i].addPublication(self)
            else:
                None
                
            if self.editors is not None:
                for i in self.editors:
                    agentesPublicaciones[i] = agentes[i]
                    agentes[i].addPublication(self)
            else:
                None    
                
            if fileHandler is None:
                print(json.dumps(clean_nones(self.__dict__)))
                return True
            else:
                fileHandler.write("%s\r\n" % json.dumps(clean_nones(self.__dict__)))
                return True
        else:
            return False
           
    def create(self,node):
        #print(node.toxml())
        if len(node.getAttribute("key")) > 0: 
            self.key = node.getAttribute("key")
        if len(node.getAttribute("mdate")) > 0:
            self.mdate  = node.getAttribute("mdate")
        if len(node.getAttribute("publtype")) > 0:   
            self.publtype = node.getAttribute("publtype")
        if len(node.getAttribute("cdate")) > 0:
            self.cdate = node.getAttribute("cdate")       
        self.authors = procesaAutores(node.getElementsByTagName("author"))
        self.editors = procesaAutores(node.getElementsByTagName("editor"),True) 
        titulo = None
        booktitulo = None
        if len(node.getElementsByTagName("title")) > 0:
            titulo = obtenTextoNodo(node.getElementsByTagName("title")[0])   
        if  len(node.getElementsByTagName("booktitle")) > 0: 
            booktitulo =   obtenTextoNodo(node.getElementsByTagName("booktitle")[0])  
        self.title = titulo
        self.booktitle = booktitulo
        if len(node.getElementsByTagName("pages")) > 0:
            self.pages = obtenTextoNodo(node.getElementsByTagName("pages")[0])
        try :
            if len(node.getElementsByTagName("year"))>0:
            #self.yearInicial, self.yearFinal = procesaFechas(node)
                self.year =  int(obtenTextoNodo(node.getElementsByTagName("year")[0]))
        except :
            print("Error convertiendo agno para registro "+self.key)
                   
        
        if len(node.getElementsByTagName("address")) > 0: 
            self.address =  obtenTextoNodo(node.getElementsByTagName("address")[0])  
        if len(node.getElementsByTagName("journal")) > 0: 
            self.journal =  obtenTextoNodo(node.getElementsByTagName("journal")[0])
        if len(node.getElementsByTagName("volume")) > 0: 
            self.volume =  obtenTextoNodo(node.getElementsByTagName("volume")[0]) 
        if len(node.getElementsByTagName("number")) > 0: 
            self.number =  obtenTextoNodo(node.getElementsByTagName("number")[0])
        if len(node.getElementsByTagName("month")) > 0: 
            self.month =  obtenTextoNodo(node.getElementsByTagName("month")[0]) 
        if len(node.getElementsByTagName("url")) > 0: 
            self.url =  obtenerMultipleNodos(node.getElementsByTagName("url"))
        if len(node.getElementsByTagName("ee")) > 0: 
            self.ee =  obtenTextoNodo(node.getElementsByTagName("ee")[0])
        if len(node.getElementsByTagName("cdrom")) > 0: 
            self.cdrom =  obtenTextoNodo(node.getElementsByTagName("cdrom")[0])
        if len(node.getElementsByTagName("cite")) > 0: 
            self.cite =  obtenerMultipleNodos(node.getElementsByTagName("cite"))
        if len(node.getElementsByTagName("publisher")) > 0: 
            self.publisher =  obtenTextoNodo(node.getElementsByTagName("publisher")[0])
        if len(node.getElementsByTagName("note")) > 0: 
            self.note =  obtenerMultipleNodos(node.getElementsByTagName("note"))
        if len(node.getElementsByTagName("crossref")) > 0: 
            self.crossref =  obtenerMultipleNodos(node.getElementsByTagName("crossref"))
        if len(node.getElementsByTagName("isbn")) > 0: 
            self.isbn =  obtenTextoNodo(node.getElementsByTagName("isbn")[0])
        if len(node.getElementsByTagName("series")) > 0: 
            self.series =  obtenTextoNodo(node.getElementsByTagName("series")[0])
        if len(node.getElementsByTagName("school")) > 0: 
            self.school =  obtenTextoNodo(node.getElementsByTagName("school")[0])
        if len(node.getElementsByTagName("chapter")) > 0: 
            self.chapter =  obtenTextoNodo(node.getElementsByTagName("chapter")[0])
        if len(node.getElementsByTagName("publnr")) > 0: 
            self.publnr =  obtenTextoNodo(node.getElementsByTagName("publnr")[0])
        
        #print(json.dumps(clean_nones(self.__dict__)))

def procesaAutores(nodes, editor = False):
    global agentesInverso
    global agentes    
    if len(nodes) == 0:
        #if not editor:
            #print("nodo sin autores")            
        return None
    else:
        autores=[]
        for node in nodes:
            elementAuthor = AuthorMetadata()
            elementAuthor.create(node)
            if not elementAuthor.name in agentesInverso.keys():
                if not editor:
                    nuevoAutor = Autor(elementAuthor)
                    agentesInverso[elementAuthor.name] = nuevoAutor
                    agentes[nuevoAutor._id] = nuevoAutor
                    autores.append(nuevoAutor._id)
                else:
                    nuevoEditor = Publisher(elementAuthor)
                    agentesInverso[elementAuthor.name] = nuevoEditor
                    agentes[nuevoEditor._id] = nuevoEditor
                    autores.append(nuevoEditor._id)
            else:
                #if not editor:
                autores.append(agentesInverso[elementAuthor.name]._id)
                #else:
                    
        if len(autores) == 0:
            print("no se han conseguido autores")   
        return autores


def procesaTagAutores(nodes):
    if len(nodes) == 0:
        return None
    else:
        autores=[]
        for node in nodes:
            nameOfAuthor = obtenTextoNodo(node)            
        return autores


def clean_nones(value):
    """
    Recursivamente elimina todos los nones de un objeto para hacer
    el json lo mas recogido posible
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clean_nones(val)
            for key, val in value.items() if val is not None
        }
    else:        
        return value

def obtenerMultipleNodos(nodes):
    if len(nodes) == 0:
        return None
    else:
        ret=[]
        for node in nodes:
            ret.append(obtenTextoNodo(node))
        return ret

def obtenTextoNodo(node):
    if node.nodeType ==  node.TEXT_NODE:
            return node.data
    else:
            text_string = ""
            for child_node in node.childNodes:
                text_string += obtenTextoNodo( child_node )
            return text_string
    


class AbstractProperty:
    def __init__(self):
        self.aux = None
        self.label = None
        self.type = None
                   
# definimos de forma abstracta la entidad agente
#<!ELEMENT person ((author*, (note|url|cite)*)|crossref) > 
#<!ATTLIST person key CDATA #REQUIRED
#          mdate CDATA #IMPLIED
#          cdate CDATA #IMPLIED
#>

#<!ELEMENT author    (#PCDATA)>
#<!ATTLIST author
#                    aux CDATA #IMPLIED
#                    bibtex CDATA #IMPLIED
#                    orcid CDATA #IMPLIED
#                    label CDATA #IMPLIED
#                    type CDATA #IMPLIED 
#>

class AuthorMetadata(dict):
    def __init__(self):
         self.aux = None
         self.bibtex = None
         self.orcid = None
         self.label = None
         self.type = None
         self.name = None
    #def __init__(self,name):
    #    self.__init__()
    #    self.name = name
    def create(self,node):
        if len(node.getAttribute("aux")) > 0: 
            self.aux = node.getAttribute("aux")
        if len(node.getAttribute("bibtex")) > 0: 
            self.bibtex = node.getAttribute("bibtex")
        if len(node.getAttribute("orcid")) > 0: 
            self.orcid = node.getAttribute("orcid")
        if len(node.getAttribute("label")) > 0: 
            self.label = node.getAttribute("label")
        if len(node.getAttribute("type")) > 0: 
            self.type = node.getAttribute("type")
        self.name = obtenTextoNodo(node)
    
    def toJson(self):
        return json.dumps(clean_nones(self), default=lambda o: o.__dict__)

class Agent:
    def __init__(self, authorMetadata = None):
        global idAgente
        idAgente += 1
        self._id = idAgente
        self.key = None
        self.mdate = None
        self.cdate = None        
        self.urlpt= None  
        self.homePage = None        
        self.note = None
        self.url = None
        self.crossref = None    
        self.publicationsRelated = None
        if authorMetadata != None:
            self.authors = [authorMetadata]
            self.name = authorMetadata.name
        else:
             self.authors = None
             self.name = None        
    def create(self,node):
        if len(node.getAttribute("key")) > 0: 
            self.key = node.getAttribute("key")
        if len(node.getAttribute("mdate")) > 0:
            self.mdate  = node.getAttribute("mdate")
        if len(node.getAttribute("publtype")) > 0:   
            self.publtype = node.getAttribute("publtype")
        if len(node.getAttribute("cdate")) > 0:
            self.cdate = node.getAttribute("cdate")     
        # cuidado, aqui se podrian meter duplicados  
        self.authors = procesaTagAutores(node.getElementsByTagName("author"))
        if len(node.getElementsByTagName("note")) > 0: 
            self.note =  obtenerMultipleNodos(node.getElementsByTagName("note"))
        if len(node.getElementsByTagName("url")) > 0: 
            self.url =  obtenerMultipleNodos(node.getElementsByTagName("url"))
        if len(node.getElementsByTagName("cite")) > 0: 
            self.cite =  obtenerMultipleNodos(node.getElementsByTagName("cite"))
        if len(node.getAttribute("crossref")) > 0:
            self.cdate = node.getAttribute("crossref")
    def addPublication(self,publication):
        if self.publicationsRelated is None:
           self.publicationsRelated = []
        if publication._id not in self.publicationsRelated:
           self.publicationsRelated.append(publication._id)
    def isEmpty(self):
        if self.key is None:
            return True
        else: 
            return False 
    def serialize(self,fileHandler):
        if fileHandler is None:
            print(json.dumps(clean_nones(self.__dict__)))
        else:
            fileHandler.write("%s\r\n" % json.dumps(clean_nones(self.__dict__)))            
        
# definimos la clase agente
class Autor(Agent):
    def __init__(self,authorNode = None):
        super().__init__(authorNode)
    #def __init__(self,authorNode):
    #    super().__init__(authorNode)
    def create(self,node):
        #print(node.toxml())
        super().create(node)
        self.personType = "author"  

# definimos la clase publicador
class Publisher(Agent):
    def __init__(self,authorNode = None):
        super().__init__(authorNode)
    #def __init__(self,authorNode):
    #    super().__init__(authorNode)
    def create(self,node):
        #print(node.toxml())
        super().create(node)
        self.personType = "publisher" 

        
class Article(AbstractReference):
    def __init__(self):
        super().__init__()
        self.reviewid = None
        self.rating = None
    def create(self,node):
        #print(node.toxml())
        super().create(node)
        self.reviewid = node.getAttribute("reviewid")
        self.rating =  node.getAttribute("rating")
        self.publicationType = "article"
  
class Inproceedings(AbstractReference):
    def __init__(self):
        super().__init__()
    def create(self,node):
        #print(node.toxml())
        super().create(node)
        self.publicationType = "inproceedings"   
    
class Proceedings(AbstractReference):
    def __init__(self):
        super().__init__()
    def create(self,node):
        #print(node.toxml()) 
        super().create(node)
        self.publicationType = "proceedings" 

class Book(AbstractReference):
    def __init__(self):
        super().__init__()
    def create(self,node):
        #print(node.toxml())
        super().create(node)
        self.publicationType = "book"
        
class Incollection(AbstractReference):
    def __init__(self):
        super().__init__()
    def create(self,node):
        #print(node.toxml()) 
        super().create(node)
        self.publicationType = "incollection"

class Phdthesis(AbstractReference):
    def __init__(self):
        super().__init__()
    def create(self,node):
        #print(node.toxml())
        super().create(node)
        self.publicationType = "phdthesis"   

class Mastersthesis(AbstractReference):
    def __init__(self):
        super().__init__()
    def create(self,node):
        #print(node.toxml())
        super().create(node)
        self.publicationType = "mastersthesis"

class WWWLink(AbstractReference):
    def __init__(self):
        super().__init__()
    def create(self,node):
        #print(node.toxml()) 
        super().create(node)
        self.publicationType = "www"
 

listaElementosValidados =  [Article,Inproceedings,Incollection]

if __name__ == "__main__":
    doc = pulldom.parse('/mnt/c/Users/msalc/Qsync/docmaster/curso/basesDatosNoConvencionales/practicaMongo/dblp.xml')
    #db = pickledb.load('/mnt/c/Users/msalc/Qsync/docmaster/curso/basesDatosNoConvencionales/practicaMongo/authors.db',False)
    numberOfPublications = 10000000000000
    numberOfFlush = 10000
    currentPublication = 0
    filePublications= open("/mnt/f/publications.json","w")
    fileAuthors= open("/mnt/f/authors.json","w")    
    for event, node in doc:
        currentElement = None
        if event == pulldom.START_ELEMENT and node.tagName == 'article':
            actualArticle = Article()            
            doc.expandNode(node)
            actualArticle.create(node)
            currentElement = actualArticle
        elif event == pulldom.START_ELEMENT and node.tagName == 'inproceedings':
            actualInproceedings = Inproceedings()            
            doc.expandNode(node)
            actualInproceedings.create(node)
            currentElement = actualInproceedings
        elif event == pulldom.START_ELEMENT and node.tagName == 'proceedings':
            #actualProceedings = Proceedings()            
            #doc.expandNode(node)
            #actualProceedings.create(node)
            #currentElement = actualProceedings
            None
        elif event == pulldom.START_ELEMENT and node.tagName == 'book':
            #actualBook = Book()            
            #doc.expandNode(node)
            #actualBook.create(node)
            #currentElement = actualBook
            None
        elif event == pulldom.START_ELEMENT and node.tagName == 'incollection':
            actualIncollection = Incollection()            
            doc.expandNode(node)
            actualIncollection.create(node)   
            currentElement = actualIncollection
        elif event == pulldom.START_ELEMENT and node.tagName == 'phdthesis':
            #actualPhdthesis = Phdthesis()            
            #doc.expandNode(node)
            #actualPhdthesis.create(node)
            #currentElement = actualPhdthesis
            None   
        elif event == pulldom.START_ELEMENT and node.tagName == 'mastersthesis':
            #actualMastersthesis = Mastersthesis()            
            #doc.expandNode(node)
            #actualMastersthesis.create(node)
            #currentElement = actualMastersthesis 
            None   
        elif event == pulldom.START_ELEMENT and node.tagName == 'www':
            #actualWWWLink = WWWLink()            
            #doc.expandNode(node)
            #actualWWWLink.create(node)
            #currentElement = actualWWWLink
            None
        #else:
        #    print("error procesando nodo "+node.tagName)
        # elemento a procesar   
        if currentElement is not None:    
            if currentElement.serialize(filePublications,listaElementosValidados):
                currentPublication = currentPublication +1
        if currentPublication > numberOfPublications:
            break
        if currentPublication > 0 and currentPublication%numberOfFlush == 0:
            print('flusing on '+str(currentPublication))
            filePublications.flush()
    for agent in agentesInverso.values():
        agent.serialize(fileAuthors)  
    
    filePublications.close()
    fileAuthors.close()