import qualified Data.HashMap.Strict as M
import Data.List.Split

moveMaze nextOffset (i, maze, moves) = case M.lookup i maze of
  Nothing -> (Nothing, maze, moves)
  Just offset -> moveMaze nextOffset (i + offset, M.insert i (nextOffset offset) maze, moves + 1)

listToMaze xs = M.fromList $ zip [0..] xs

movesToExit nextOffset xs = let
  (_, _, moves) = moveMaze nextOffset (0, listToMaze xs, 0)
  in moves

a xs = movesToExit succ xs
b xs = let
  next x = if x >= 3 then x - 1 else x + 1
  in movesToExit next xs

main = do
  stdin <- getContents
  putStr (show $ let
    maze = map (\x -> read x :: Int) (filter (\x -> x /= "") $ splitOn "\n" stdin)
    in (a maze, b maze))
