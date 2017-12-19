import Data.Array

toComplexArray :: [[a]] -> Array(Int, Int) a
toComplexArray grid = array ((0,0),((length $ grid !! 0) - 1,(length grid) - 1))  entries  
  where entries = concatMap (\z -> map (\y -> ((fst y, fst z), snd y))  (snd z)) $ zip [0..] $ map (\x -> zip [0..] x) grid

row y a = [(x, a ! (x, y)) | x <- [0..w]]
  where (_, (w, _)) = bounds a

findStart :: Array(Int, Int) Char -> (Int, Int)
findStart a = let
  (_, (w, h)) = bounds a
  in (foldl (\m (x, v) -> if v /= ' ' then x else m) (-1) (row 0 a), 0)

runMaze seed reduce maze = let
  move ls (x, y) (dx, dy)
    | p == '+' = move reduced (x+nx, y+ny) (nx, ny)
    | p == ' ' = ls
    | otherwise = move reduced (x+dx, y+dy) (dx, dy)
    where
    reduced = reduce ls p
    p = m (x, y)
    m (x, y) = if x >= 0 && y >= 0 && x < w && y < h then maze ! (x, y) else ' '
    (nx, ny) = if dx == 0 then
        if m (x+1, y) /= ' ' then (1, 0) else (-1, 0)
      else
        if m (x, y+1) /= ' ' then (0, 1) else (0, -1)
    (_, (w, h)) = bounds maze
  in move seed (findStart maze) (0, 1)

collectLetters ls p = if p >= 'A' && p <= 'Z' then (p:ls) else ls
collectSteps :: Int -> Char -> Int
collectSteps ls _ = ls + 1

main = do
  contents <- getContents
  putStr (show $ reverse $ runMaze [] collectLetters $ toComplexArray $ lines contents)
  putStr ("\n")
  putStr (show $ runMaze 0 collectSteps $ toComplexArray $ lines contents)
  putStr ("\n")
