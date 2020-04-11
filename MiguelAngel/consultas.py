from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb://localhost:27017/")
db=client.practica
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

def crearIndiceNombreAutor():
    global db



def consultaNumero1(nombreAutor):
    global db
    ret = db.autores.aggregate( [
                {
                    '$match': {
                        'name': 'Paul Kocher'
                    }
                }, {
                    '$unwind': {
                        'path': '$publicationsRelated', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$lookup': {
                        'from': 'publicaciones', 
                        'localField': 'publicationsRelated', 
                        'foreignField': 'id_', 
                        'as': 'publication'
                    }
                }, {
                    '$project': {
                        'publication': 1, 
                        '_id': 0
                    }
                }, {
                    '$unwind': {
                        'path': '$publication'
                    }
                }
    ])


    ret = db.autores.aggregate([
    {
        '$match': {
            'name': 'Paul Kocher'
        }
    }, {
        '$lookup': {
            'from': 'publicaciones', 
            'localField': 'id_', 
            'foreignField': 'authors', 
            'as': 'publicaciones'
        }
    }, {
        '$project': {
            'publicaciones': 1, 
            '_id': 0
        }
    }, {
        '$unwind': {
            'path': '$publicaciones'
        }
    }
])

def consultaNumero2(nombreAutor):
    global db
    ret = db.autores.aggregate( [
    {
        '$match': {
            'name': 'Paul Kocher'
        }
    }, {
        '$lookup': {
            'from': 'publicaciones', 
            'localField': 'id_', 
            'foreignField': 'authors', 
            'as': 'publicaciones'
        }
    }, {
        '$project': {
            'numeroPublicaciones': {
                '$size': '$publicaciones'
            }, 
            '_id': 0
        }
    }
])

def consultaNumero3():
    global db
    ret = db.publicaciones.aggregate([
    {
        '$match': {
            '$and': [
                {
                    'publicationType': {
                        '$eq': 'article'
                    }
                }, {
                    'year': {
                        '$eq': 2018
                    }
                }
            ]
        }
    }, {
        '$count': 'id_'
    }
    ])



def consultaNumero4(nombreAutor):
    global db
    ret = db.publicaciones.aggregate([
    {
        '$unwind': {
            'path': '$authors', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$project': {
            'authors': 1
        }
    }, {
        '$group': {
            '_id': '$authors', 
            'totalDocumentos': {
                '$sum': 1
            }
        }
    }, {
        '$match': {
            'totalDocumentos': {
                '$lt': 5
            }
        }
    }, {
        '$count': 'totalCount'
    }
    ])



    ret = db.autores.aggregate([
    {
        '$project': {
            'lessThanFive': {
                '$and': [
                    {
                        '$lt': [
                            {
                                '$size': '$publicationsRelated'
                            }, 5
                        ]
                    }, {
                        '$gt': [
                            {
                                '$size': '$publicationsRelated'
                            }, 0
                        ]
                    }
                ]
            }
        }
    }, {
        '$match': {
            'lessThanFive': True
        }
    }, {
        '$count': 'numeroLessThanFive'
    }
    ])

def consultaNumero5(nombreAutor):
    global db
    ret = db.autores.aggregate([
    {
        '$unwind': {
            'path': '$authors', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$group': {
            '_id': '$authors', 
            'totalDocumentos': {
                '$sum': 1
            }, 
            'documentTypes': {
                '$push': {
                    'publicationType': '$publicationType'
                }
            }
        }
    }, {
        '$sort': {
            'totalDocumentos': -1
        }
    }, {
        '$limit': 10
    }, {
        '$lookup': {
            'from': 'autores', 
            'localField': '_id', 
            'foreignField': 'id_', 
            'as': 'autor'
        }
    }, {
        '$addFields': {
            'numeroArticulos': {
                '$size': {
                    '$filter': {
                        'input': '$documentTypes.publicationType', 
                        'cond': {
                            '$eq': [
                                '$$this', 'article'
                            ]
                        }
                    }
                }
            }, 
            'numeroInProceedigs': {
                '$size': {
                    '$filter': {
                        'input': '$documentTypes.publicationType', 
                        'cond': {
                            '$eq': [
                                '$$this', 'inproceedings'
                            ]
                        }
                    }
                }
            }
        }
    }, {
        '$project': {
            'totalDocumentos': 1, 
            'numeroArticulos': 1, 
            'numeroInProceedigs': 1, 
            'autor': {
                '$arrayElemAt': [
                    '$autor', 0
                ]
            }, 
            '_id': 0
        }
    }
    ])

def consultaNumero6(nombreAutor):
    global db
    ret = db.autores.aggregate([
    {
        '$addFields': {
            'numeroAutores': {
                '$size': {
                    '$ifNull': [
                        '$authors', []
                    ]
                }
            }
        }
    }, {
        '$project': {
            'publicationType': 1, 
            'numeroAutores': 1
        }
    }, {
        '$group': {
            '_id': '$publicationType', 
            'numeroPublicaciones': {
                '$sum': 1
            }, 
            'numeroMedioAutores': {
                '$avg': '$numeroAutores'
            }
        }
    }
    ])

def consultaNumero7(nombreAutor):
    global db
    ret = db.autores.aggregate(
        [
    {
        '$match': {
            'name': 'Paul Kocher'
        }
    }, {
        '$lookup': {
            'from': 'publicaciones', 
            'localField': 'id_', 
            'foreignField': 'authors', 
            'as': 'publicaciones'
        }
    }, {
        '$project': {
            'id_': 1, 
            'name': 1, 
            'listadosCoautores': {
                '$filter': {
                    'input': {
                        '$reduce': {
                            'input': '$publicaciones.authors', 
                            'initialValue': [], 
                            'in': {
                                '$setUnion': [
                                    '$$value', '$$this'
                                ]
                            }
                        }
                    }, 
                    'as': 'num', 
                    'cond': {
                        '$ne': [
                            '$$num', '$id_'
                        ]
                    }
                }
            }
        }
    }, {
        '$lookup': {
            'from': 'autores', 
            'localField': 'listadosCoautores', 
            'foreignField': 'id_', 
            'as': 'detalleListadoCoautores'
        }
    }
    ])

def consultaNumero8():
    global db
    ret = db.autores.aggregate(
        [
    {
        '$lookup': {
            'from': 'publicaciones', 
            'localField': 'id_', 
            'foreignField': 'authors', 
            'as': 'publicaciones'
        }
    }, {
        '$project': {
            'id_': 1, 
            'name': 1, 
            'difference': {
                '$subtract': [
                    {
                        '$max': '$publicaciones.year'
                    }, {
                        '$min': '$publicaciones.year'
                    }
                ]
            }
        }
    }, {
        '$sort': {
            'difference': -1
        }
    }, {
        '$limit': 5
    }
    ])


def consultaNumero9():
    global db
    ret = db.autores.aggregate(
    [
    {
        '$lookup': {
            'from': 'publicaciones', 
            'localField': 'id_', 
            'foreignField': 'authors', 
            'as': 'publicaciones'
        }
    }, {
        '$project': {
            'id_': 1, 
            'name': 1, 
            'difference': {
                '$subtract': [
                    {
                        '$max': '$publicaciones.year'
                    }, {
                        '$min': '$publicaciones.year'
                    }
                ]
            }
        }
    }, {
        '$match': {
            'difference': {
                '$lt': 5
            }
        }
    }, {
        '$count': 'id_'
    }
    ])


def consultaNumero10():
    global db
    ret = db.autores.aggregate(
    [
    {
        '$group': {
            '_id': '$publicationType', 
            'numeroElementos': {
                '$sum': 1
            }
        }
    }, {
        '$group': {
            '_id': None, 
            'elementos': {
                '$push': {
                    'clave': '$_id', 
                    'valor': '$numeroElementos'
                }
            }, 
            'total': {
                '$sum': '$numeroElementos'
            }
        }
    }, {
        '$unwind': {
            'path': '$elementos', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'elementos.clave': 'article'
        }
    }, {
        '$project': {
            'proporcion': {
                '$divide': [
                    '$elementos.valor', '$total'
                ]
            }
        }
    }
    ]
    )


if __name__ == "__main__":
    resultado = consultaNumero1('hola')
