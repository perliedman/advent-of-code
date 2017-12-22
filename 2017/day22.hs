import qualified Data.Map.Strict as Map

type Grid = Map.Map (Int, Int) Char
type State = (Grid, (Int, Int), (Int, Int), Int)

step :: State -> State
step (grid, (x, y), (dx, dy), infections) = 
  (Map.insert (x, y) (invert n) grid, (x+nx, y+ny), (nx, ny), if n == '.' then infections+1 else infections)
  where
    n = Map.findWithDefault '.' (x, y) grid
    invert '#' = '.'
    invert '.' = '#'
    (nx, ny) = if n == '#' then
      -- right
      (-dy, dx) 
    else
      -- left
      (dy, -dx)

runSteps n state = foldl (\s _ -> step s) state [1..n]

gridMiddle :: Grid -> (Int, Int)
gridMiddle grid = (mx `div` 2, my `div` 2) where ((mx, my), _) = Map.findMax grid

initState :: Grid -> State
initState grid = (grid, gridMiddle grid, (0, -1), 0)

parse :: [String] -> Grid
parse = let
  insertLine row grid nodes = foldl (\grid (x,n) -> Map.insert (x,row) n grid) grid (zip [0..] nodes)
  in snd . foldl (\(row, grid) line -> (row+1, insertLine row grid line)) (0, Map.empty)

printState :: State -> String
printState (grid, _, _, infections) = let
  gridBounds = foldl (\((minx, maxx), (miny, maxy)) (x, y) -> ((min minx x, max maxx x), (min miny y, max maxy y))) ((0, 0), (0, 0)) . Map.keys
  toLine grid y (minx, maxx) = map (\c -> Map.findWithDefault '.' c grid) $ zip [minx..maxx] (cycle [y])
  toLines grid (xb, (miny, maxy)) = map (\y -> toLine grid y xb) [miny..maxy]
  in unlines ((toLines grid $ gridBounds grid) ++ ["Infections:" ++ show infections])


main = do
  contents <- getContents
  putStr (printState $ runSteps 10000 $ initState $ parse $ lines contents)