import Data.Char

inverseCaptcha x =
  let digits = map digitToInt x
      halfLen = length digits `div` 2
  in sum [fst i | i <- zip digits (drop halfLen digits ++ take halfLen digits), fst i == snd i]
