-- import Data.Map (Map)
-- import qualified Data.Map as Map
import qualified Data.HashMap.Strict as M


leastOddSquare x = let
  makeOdd x = 2 * x + 1
  in head [(makeOdd k, k) | k <- [1..], x <= ((^2) $ makeOdd k)]

coord :: Integer -> (Integer, Integer)
coord 1 = (0, 0)
coord v
  | v == n²                           = (k, k)
  | n²-(n-1) <= v   && v < n²         = (k - n² + v, k)
  | n²-2*(n-1) <= v && v < n²-(n-1)   = (k - n + 1, k - (n²-(n-1)) + v)
  | n²-3*(n-1) <= v && v < n²-2*(n-1) = (k + (n²-3*(n-1)) - v, k - n + 1)
  | (n-2)^2+1 <= v && v < n²-3*(n-1)  = (k, k + (n-2)^2 - v)
  where
    (n, k) = leastOddSquare v
    n² = n^2

distance x = (abs $ fst c) + (abs $ snd c) where c = coord x

firstWithXLessThan x = head $ dropWhile (\c -> (fst $ fst c) < x) [(coord v, v) | v <- [1..]]

memVal 1 = (1, M.singleton (0, 0) 1)
memVal v = let
  (_, previous) = memVal (v - 1)
  c = coord v
  calcVal v previous = let
    add (x, y) (dx, dy) = (x+dx, y+dy)
    neighbors = map (add c) [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    in sum [M.lookupDefault 0 c previous | c <- neighbors]
  value = calcVal v previous
  in (value, M.insert c value previous)

firstMemValGreaterThan x = head $ dropWhile (\v -> fst v <= x) [(fst $ memVal v, v) | v <- [1..]]
