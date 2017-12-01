import Data.Char

inverseCaptcha x =
  let digits = map digitToInt x
  in sum [fst i | i <- zip digits (tail digits ++ [head digits]), fst i == snd i]
