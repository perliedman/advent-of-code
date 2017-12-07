import Data.Array
import qualified Data.Set as S

maxIndex xs = let
  (maxVal, i, _) = foldl (\(maxVal, maxIndex, i) x -> if x > maxVal then (x, i, i + 1) else (maxVal, maxIndex, i + 1)) (-1, -1, 0) xs
  in (i, maxVal)

spread amount step xs = let
  f (rest, ys) x = let
    s = if rest > step then step else rest
    in (rest - s, ys ++ [x + s])
  in foldl f (amount, []) xs

nextState xs = let
  l = length xs
  (mIndex, mVal) = maxIndex xs
  value = max 1 $ if mVal `mod` l == 0 then mVal `div` l else mVal `div` (l - 1)
  (tr, t) = spread mVal value $ drop (mIndex + 1) xs
  (remainder, h) = spread tr value $ take mIndex xs
  in h ++ [remainder] ++ t
  -- in (h ++ [remainder] ++ t, mIndex, mVal, value, remainder, h, t)

countCycles xs seen count = let
  hasBeenSeen = S.member xs seen
  in if hasBeenSeen then count else countCycles (nextState xs) (S.insert xs seen) (count + 1)

genStates _ 0 = []
genStates xs n = xs : genStates (nextState xs) (n - 1)

a xs = countCycles xs S.empty 0
b xs = let
  state = last $ genStates xs (a xs + 1)
  in a state
