def get_coordenadas(departamento):
    
    coordenadas = {
        'Lima': [-12.046374, -77.042793],
        'Arequipa': [-16.409047, -71.537450],
        'Cusco': [-13.518333, -71.978056],
        'La Libertad': [-8.108333, -79.021944],
        'Piura': [-5.194490, -80.632820],
        'Lambayeque': [-6.771428, -79.840167],
        'Junín': [-11.158889, -75.994444],
        'Puno': [-15.840000, -70.021944],
        'Ancash': [-9.119722, -77.034167],
        'Ica': [-14.067778, -75.728056],
        'Tacna': [-18.012739, -70.245812],
        'Loreto': [-3.749028, -73.247831],
        'Ucayali': [-8.379147, -74.553909],
        'San Martín': [-6.500000, -76.333333],
        'Madre de Dios': [-12.592761, -69.183088],
        'Amazonas': [-6.232976, -77.874962],
        'Pasco': [-10.686389, -76.263056],
        'Huancavelica': [-12.785278, -74.976111],
        'Ayacucho': [-13.158889, -74.223611],
        'Tumbes': [-3.566944, -80.454722],
        'Moquegua': [-17.195556, -70.935833],
        'Huánuco': [-9.932222, -76.241111],
        'Apurímac': [-14.030833, -73.002222],
        'Cajamarca': [-7.163788, -78.500000],
        'Callao': [-12.056722, -77.118722],
        'Iquitos': [-3.743673, -73.251317]
    }
    return coordenadas.get(departamento, [0, 0])

