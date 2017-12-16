import Data.List
import Data.List.Split

data Instr = Spin Int | Exchange Int Int | Partner Char Char deriving (Show)

swapTwo' f s xs = zipWith (\x y -> 
    if x == f then xs !! s
    else if x == s then xs !! f
    else y) [0..] xs

execute :: [Char] -> [Instr] -> String
execute = let
  e :: [Char] -> Instr -> [Char]
  e xs (Spin x) = (drop front xs) ++ (take front xs) where front = (length xs) - x
  e xs (Exchange a b) = swapTwo' a b xs
  e xs (Partner x y) = swapTwo' a b xs where
    Just a = elemIndex x xs
    Just b = elemIndex y xs
  in foldl e

executeN :: [Instr] -> Int -> String
executeN instr = let
  e s 0 = s
  e s n = e (execute s instr) (n - 1)
  in e ['a'..'p']

findCycle :: [Instr] -> Int
findCycle instr = let
  start = ['a'..'p']
  e s = if next == start then 1 else 1+(e next) where next = execute s instr
  in e start

parse i = let
  p 's' rest = Spin (read rest :: Int)
  p 'x' rest = Exchange (read a :: Int) (read b :: Int) where [a, b] = splitOn "/" rest
  p 'p' rest = Partner (head a) (head b) where [a, b] = splitOn "/" rest
  in p (head i) (tail i)

instructions = splitOn ","

main = do
  contents <- getContents
  putStr (show $ execute ['a'..'p'] $ map parse $ instructions contents)
  putStr ("\n")
  putStr (show $ findCycle $ map parse $ instructions contents)
  putStr (show $ executeN (map parse $ instructions contents) (1000000000 `mod` (findCycle $ map parse $ instructions contents)))
  -- putStr (show $ executeN (map parse $ instructions contents) 18)
  putStr ("\n")
