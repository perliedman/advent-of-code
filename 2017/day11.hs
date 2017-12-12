import Data.List.Split
import qualified Data.Map.Strict as Map
import Data.Maybe

dirs = Map.fromList [
    ("n", (1, -1, 0)),
    ("ne", (0, -1, 1)),
    ("se", (-1, 0, 1)),
    ("s", (-1, 1, 0)),
    ("sw", (0, 1, -1)),
    ("nw", (1, 0, -1))
  ]

dist (x, y, z) = div ((abs x) + (abs y) + (abs z)) 2

move ms = let
  c1 (x, _, _) = x
  c2 (_, x, _) = x
  c3 (_, _, x) = x
  in (sum $ map c1 ms, sum $ map c2 ms, sum $ map c3 ms)

maxdist m c [] = max (dist c) m
maxdist m c ((dx, dy, dz):ms) = let
  (x, y, z) = c
  nc = (x+dx, y+dy, z+dz)
  in maxdist (max m (dist c)) nc ms

stepList = catMaybes . map (\x -> Map.lookup x dirs)
dirList = splitOn ","

a = dist . move . stepList . dirList
b = (maxdist 0 (0,0,0)) . stepList . dirList
