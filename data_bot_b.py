address_fil = [
    [{'text': 'пр-т Рокосcовского, 44    ФОК "Серебрянка"', 'callback_data': 'adr_rokosovskogo'},
     [[{'text': '10.00 - 10.50 понедельник, среда (группа 7-14 лет)', 'callback_data': 'fil_rokosovskogo_1'}],
      [{'text': '18.00 - 18.50 вторник, четверг (группа 7-14 лет)', 'callback_data': 'fil_rokosovskogo_2'}]
      ]
     ],
    [{'text': 'ул. Налибокская, 1  ТЦ "Караван"  (К.Горка)', 'callback_data': 'adr_nalibokskaya'},
     [[{'text': '17.00 - 17.50 вторник, четверг (группа 7-14 лет)', 'callback_data': 'fil_nalibokskaya_1'}]
      ]
     ],
    [{'text': 'ул. Шугаева, 19/1    СШ № 177   (Уручье)', 'callback_data': 'adr_shugaevo'},
     [[{'text': '15.30 - 16.20 вторник, четверг (группа 7-10 лет)', 'callback_data': 'fil_shugaevo_1'}],
      [{'text': '16.30 - 17.20 вторник, четверг (группа 11-16 лет)', 'callback_data': 'fil_shugaevo_2'}]
      ]
     ],
    [{'text': 'ул. Жудро, 15    СШ № 125     (м. Спортивная)', 'callback_data': 'adr_zhudro'},
     [[{'text': '18.00-18.50 понедельник, среда (группа 7-14 лет)', 'callback_data': 'fil_zhudro_1'}]
      ]
     ],
    [{'text': 'ул. Михаловская, 14     (м. Михалово)', 'callback_data': 'adr_mixalovskaya'},
     [[{'text': '16.00-16.50 понедельник, среда (группа 7-10 лет)', 'callback_data': 'fil_mixalovskaya_1'}],
      [{'text': '17.00-17.50 понедельник, среда (группа 11-16 лет)', 'callback_data': 'fil_mixalovskaya_2'}]
      ]
     ],
    [{'text': 'ул. Острошицкая, 7     (Уручье)', 'callback_data': 'adr_ostroshitskaya'},
     [[{'text': '16.00-16.50 понедельник, среда (группа 7-14 лет)', 'callback_data': 'fil_ostroshitskaya_1'}]
      ]
     ],
    [{'text': 'ул. Никифорова, 12     (Уручье)', 'callback_data': 'adr_nikiforova'},
     [[{'text': '10.00-10.50 понедельник, среда (группа 7-14 лет)', 'callback_data': 'fil_nikiforova_1'}]
      ]
     ],
    # [{'text': 'пр-т. Победителей, 133', 'callback_data': 'adr_pobeditelei'},
    #    [   {'text': '17.00-17.50 понедельник, среда (группа 7-14 лет)', 'callback_data': 'fil_pobeditelei_1'}
    #    ]
    # ],
    [{'text': 'ул. Братская, 1    (Минск - Мир)', 'callback_data': 'adr_bratskaya'},
     [[{'text': '10.00 - 10.50 вторник, четверг (группа 7-14 лет)', 'callback_data': 'fil_bratskaya_1'}],
      [{'text': '15.30 - 16.20 понедельник, среда (группа 7-10 лет)', 'callback_data': 'fil_bratskaya_2'}],
      [{'text': '16.30 - 17.20 понедельник, среда (группа 11-16 лет)', 'callback_data': 'fil_bratskaya_3'}]
      ]
     ],
    [{'text': 'пр-т Дзержинского, 125    (м. Малиновка)', 'callback_data': 'adr_dzerwinskogo'},
     [[{'text': '16.00 - 16.50 понедельник, среда (группа 7-10 лет)', 'callback_data': 'fil_dzerwinskogo_1'}],
      [{'text': '17.00 - 17.50 понедельник, среда (группа 11-16 лет)', 'callback_data': 'fil_dzerwinskogo_2'}]
      ]
     ]
]


def addres_fil_b():
    adr = []
    for adr_i in address_fil:
        adr.append([adr_i[0]])
    return adr

def grupp_f():
    gru = {}

    for gru_i in address_fil:
        gru[gru_i[0]['callback_data']] = gru_i[1]
    return gru

def address_text(call):
    fill = addres_fil_b()
    for i in fill:
        if i[0]['callback_data'] == call:
            return i[0]['text']


def grupp_text(call, adres_call):
    gru = grupp_f()
    for i in gru[adres_call]:
        if i[0]['callback_data'] == call:
            return i[0]['text']
