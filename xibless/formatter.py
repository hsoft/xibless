from .base import GeneratedItem, const

class NumberStyle(object):
    NoStyle = const.NSNumberFormatterNoStyle
    Decimal = const.NSNumberFormatterDecimalStyle
    Currency = const.NSNumberFormatterCurrencyStyle
    Percent = const.NSNumberFormatterPercentStyle
    Scientific = const.NSNumberFormatterScientificStyle
    SpellOut = const.NSNumberFormatterSpellOutStyle

class NumberFormatter(GeneratedItem):
    OBJC_CLASS = 'NSNumberFormatter'
    PROPERTIES = GeneratedItem.PROPERTIES + ['numberStyle', 'maximumFractionDigits']
    
    def __init__(self, numberStyle):
        GeneratedItem.__init__(self)
        self.numberStyle = numberStyle
    
