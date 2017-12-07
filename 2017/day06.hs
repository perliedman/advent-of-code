import Data.Array
import qualified Data.Set as S

maxIndex xs = let
  (maxVal, i, _) = foldl (\(maxVal, maxIndex, i) x -> if x > maxVal then (x, i, i + 1) else (maxVal, maxIndex, i + 1)) (-1, -1, 0) xs
  in (i, maxVal)

cycleMaxFirst xs = let
  (mIndex, mVal) = maxIndex xs
  h = drop (mIndex + 1) xs
  t = take mIndex xs
  in mVal : h ++ t

nextState (x:xs) = let
  l = length xs
  spread = x `div` l
  remainder = x `mod` l
  in remainder : (map (\x -> x + spread) xs)

countCycles xs seen count = let
  cycled = cycleMaxFirst xs
  hasBeenSeen = S.member cycled seen
  in if hasBeenSeen then count else countCycles (nextState cycled) (S.insert cycled seen) (count + 1)

genStates _ 0 = []
genStates xs n = let c = cycleMaxFirst xs in c : genStates (nextState c) (n - 1)
