if not console?
  console = {};
  console.log = console.info = console.warn = console.error = -> 

_plural = (value, str, withNum=no) ->
  ifWithNum = (n) -> if withNum then "#{value} #{n}" else n

  [one, two, five] = str.split(',')
  number = Math.abs(value)
  number %= 100
  return ifWithNum(five) if number >= 5 and number <= 20
  number %= 10
  return ifWithNum(one) if number is 1
  return ifWithNum(two) if number >= 2 and number <= 4
  ifWithNum five

_cash = (value) ->
  num = accounting.formatNumber value, 0, " "
  label = _plural value, "рубль,рубля,рублей"
  "#{num} #{label}"

Numeral =
  cash: _cash,
  plural: _plural

PowerBall =
  Numeral: Numeral

window.PowerBall = PowerBall