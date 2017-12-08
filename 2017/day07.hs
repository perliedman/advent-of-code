import qualified Text.Regex as Re
import Data.List.Split
import Data.Maybe
import qualified Data.Map.Strict as Map
import Debug.Trace

data Tower a b = Program a b | Disc a b [Tower a b] deriving (Show, Eq, Ord)

makeAllKnown [] parts rest = (parts, rest)
makeAllKnown ((name, weight, []):xs) parts rest = makeAllKnown xs (Map.insert name (Program name weight) parts) rest
makeAllKnown ((name, weight, children):xs) parts rest = let
  childTowers = catMaybes $ map (\x -> Map.lookup x parts) children
  allChildrenKnown = length childTowers == length children
  partsWithoutChildren = foldl (\m x -> Map.delete x m) parts children
  in if allChildrenKnown then makeAllKnown xs (Map.insert name (Disc name weight childTowers) partsWithoutChildren) rest else makeAllKnown xs parts ((name, weight, children):rest)

makeTower [] parts = fst $ head $ Map.toList parts
makeTower defs parts = let
  (nextParts, rest) = makeAllKnown defs parts []
  in makeTower rest nextParts

definitions input = let
  parseChildren children = filter (not . null) $ splitOn ", " children
  f [name, weight, _, childStr] = (name, read weight :: Int, parseChildren childStr)
  in map f input

lineExp = Re.mkRegex "^([a-z]+) \\(([0-9]+)\\)( -> (.*)|)$"
parseInput input = catMaybes $ map (Re.matchRegex lineExp) $ lines input

main = do
  contents <- getContents
  -- putStr (show $ buildTower (definitions $ parseInput contents) Map.empty)
  putStr (show $ makeTower (definitions $ parseInput contents) Map.empty)
  -- putStr (show $ tower contents)
  putStr "\n"
