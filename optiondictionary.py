class OptionDictionary(dict):
    """
    Conveninent class for options
    use OptionDictionary(availableOptions, userOptions)
    - availableOptions: a dictionary of {option_name: default_values}. default_value can be:
        - list-of-possible-values (default listed first)
        - or a single default value (no check)
        - or a type (no check, default is an empty instance of type)
    - userOptions: the dictionary given as argument in your method  {option_name: value}
    """
    def __init__(self, availableOptions, userOptions):
        dict.__init__(self)

        # check user options
        for key in userOptions:
            if key not in availableOptions:
                raise NameError("Option '%s' does not exist" % key)
            if type(availableOptions[key]) in (list, tuple) and userOptions[key] not in availableOptions[key]:
                raise NameError("Invalid value '%s' for option '%s'" % (userOptions[key], key))

        # create dictionary
        for key, value in availableOptions.iteritems():
            try:
                self[key] = userOptions[key]
            except KeyError:
                if type(value) in (list, tuple):
                    self[key] = value[0]
                elif type(value) == type:
                    self[key] = value()
                else:
                    self[key] = value
