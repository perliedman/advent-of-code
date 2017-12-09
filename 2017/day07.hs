import qualified Text.Regex as Re
import Data.List.Split
import Data.Maybe
import qualified Data.Map.Strict as Map
import Debug.Trace

data Tower a b = Program a b | Disc a b [Tower a b] deriving (Show, Eq, Ord)

towerName (Program name _) = name
towerName (Disc name _ _) = name

towerSum :: (Num b) => (Tower a b) -> b
towerSum (Program _ w) = w
towerSum (Disc _ w children) = w + sum (map towerSum children)

countUniques :: (Ord a) => (Num b) => [a] -> [(a, b)]
countUniques xs = let
  inc k map = let
    next Nothing = 1
    next (Just c) = c + 1
    in Map.insert k (next $ Map.lookup k map) map
  f [] seen = Map.toList seen
  f (x:xs) seen = f xs (inc x seen)
  in f xs Map.empty

findUnbalancedProgram :: Int -> (Tower b Int) -> (Maybe (b, Int, Int))
findUnbalancedProgram expectedWeight (Program name weight) = if expectedWeight == weight then Nothing else (Just (name, weight, expectedWeight))
findUnbalancedProgram expectedWeight (Disc name weight children) = let
  subTowerWeights = countUniques $ map towerSum children
  subTowersUnbalanced = length subTowerWeights > 1
  balancedWeight = fst $ head $ filter (\(weight, count) -> count > 1) subTowerWeights
  subTowerSum = sum $ map (\(weight, count) -> weight * count) subTowerWeights
  unbalancedTower = head $ filter (\child -> (towerSum child) /= balancedWeight) children
  in if subTowersUnbalanced then
    findUnbalancedProgram (expectedWeight - weight - balancedWeight * ((length children) - 1)) unbalancedTower
  else if subTowerSum + weight /= expectedWeight then
    Just (name, weight, expectedWeight - subTowerSum) 
  else
    Nothing

findUnbalance (Disc _ weight children) = let
  subTowerWeights = countUniques $ map towerSum children
  subTowersUnbalanced = length subTowerWeights > 1
  balancedWeight = fst $ head $ filter (\(weight, count) -> count > 1) subTowerWeights
  subTowerSum = sum $ map (\(weight, count) -> weight * count) subTowerWeights
  unbalancedTower = head $ filter (\child -> (towerSum child) /= balancedWeight) children
  in findUnbalancedProgram balancedWeight unbalancedTower

makeAllKnown [] parts rest = (parts, rest)
makeAllKnown ((name, weight, []):xs) parts rest = makeAllKnown xs (Map.insert name (Program name weight) parts) rest
makeAllKnown ((name, weight, children):xs) parts rest = let
  childTowers = catMaybes $ map (\x -> Map.lookup x parts) children
  allChildrenKnown = length childTowers == length children
  partsWithoutChildren = foldl (\m x -> Map.delete x m) parts children
  in if allChildrenKnown then makeAllKnown xs (Map.insert name (Disc name weight childTowers) partsWithoutChildren) rest else makeAllKnown xs parts ((name, weight, children):rest)

makeTower [] parts = snd $ head $ Map.toList parts
makeTower defs parts = let
  (nextParts, rest) = makeAllKnown defs parts []
  in makeTower rest nextParts

definitions input = let
  parseChildren children = filter (not . null) $ splitOn ", " children
  f [name, weight, _, childStr] = (name, read weight :: Int, parseChildren childStr)
  in map f input

lineExp = Re.mkRegex "^([a-z]+) \\(([0-9]+)\\)( -> (.*)|)$"
parseInput input = catMaybes $ map (Re.matchRegex lineExp) $ lines input

a contents = let
  (Disc name _ _) = makeTower (definitions $ parseInput contents) Map.empty
  in name

b contents = let
  in findUnbalance $ makeTower (definitions $ parseInput contents) Map.empty

main = do
  contents <- getContents
  putStr "A: "
  putStr (show $ a contents)
  putStr "\nB: "
  putStr (show $ b contents)
  putStr "\n"
