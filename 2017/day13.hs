import Text.Regex
import Debug.Trace
import Data.Maybe

pos depth t = let
  cycle = t `div` (depth - 1)
  p = t `mod` (depth - 1)
  in if cycle `mod` 2 == 0 then p else depth - p - 1

score [] _ = 0
score (Nothing:ds) t = score ds (t+1)
score (Just d:ds) t = let
  s = if pos d t == 0 then d * t else 0
  in s + score ds (t+1)

finddelay ds t = if score ds t == 0 then t else finddelay ds (t+1)

toDepthList _ [] = []
toDepthList r ((p, d):xs) =
  if r == p then
    (Just d):(toDepthList (r+1) xs)
  else
    (Nothing):(toDepthList (r+1) ((p, d):xs))

pattern = mkRegex "^([0-9]+): ([0-9]+)$"
parse = (toDepthList 0) . map (\[a, b] -> (read a :: Int, read b :: Int)) . catMaybes . map (matchRegex pattern) . lines

main = do
  contents <- getContents
  putStr(show $ score (parse contents) 0)
  putStr("\n")
  putStr(show $ finddelay (parse contents) 0)
