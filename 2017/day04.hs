import Data.Char
import Data.List
import Data.List.Split

hasNoDups x = let
  xs = splitOn " " x
  in (length . nub) xs == length xs

hasNoAnagrams s = let
  words = splitOn " " s
  pairs = [(x, y) | x <- words, y <- words, x /= y]
  anagrams (x, y) = sort x == sort y
  in hasNoDups s && (not $ any anagrams pairs)

numValidPassPhrases x pred = length $ filter (\x -> x /= "" && pred x) $ splitOn "\n" x

main = do
  contents <- getContents
  putStr "Valid Part One: "
  putStr (show $ numValidPassPhrases contents hasNoDups)
  putStr "\n"
  putStr "Valid Part Two: "
  putStr (show $ numValidPassPhrases contents hasNoAnagrams)
  putStr "\n"
