import jsonpickle

jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4, encoding='utf-8', ensure_ascii=False)
