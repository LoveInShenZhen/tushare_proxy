import jsonpickle

jsonpickle.set_encoder_options('simplejson',
                               sort_keys = True,
                               indent = 4,
                               encoding = 'utf-8',
                               ensure_ascii = False,
                               unpicklable = False,
                               use_decimal = True)

jsonpickle.set_decoder_options('simplejson',
                               encoding = 'utf-8',
                               use_decimal = True)

jsonpickle.set_preferred_backend('simplejson')
