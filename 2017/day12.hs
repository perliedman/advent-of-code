import qualified Text.Regex as Re
import qualified Data.Map.Strict as Map
import qualified Data.Set as Set
import Data.List
import Data.List.Split
import Data.Maybe

type Neighbors = Set.Set Int
data Node = Node Int Neighbors deriving (Show)
type Graph = Map.Map Int Node

nodeName (Node name _) = name
toGraph ns = Map.fromList $ zip (map nodeName ns) ns

parseNode s = let
  lineExp = Re.mkRegex "^([0-9]+) *<-> *(.*)$"
  Just [nodeStr, neighbStr] = Re.matchRegex lineExp s
  nodeName = read nodeStr :: Int
  neighbors = map (\x -> read x :: Int) $ splitOn "," neighbStr
  in Node nodeName (Set.fromList neighbors)

addNeighbor nodeName (Node n ns) = Node n (Set.insert nodeName ns)

addNode g n = let
  (Node name ns) = n
  neighborNodes = toGraph $ n:(map (addNeighbor name) $ catMaybes $ map (\x -> Map.lookup x g) $ Set.toList ns)
  in Map.union neighborNodes g

parseGraph = foldl addNode Map.empty . map parseNode

connectedNodes g n = let
  neighbors g seen n = let
    nseen = Set.insert n seen
    seenList = Set.toList nseen
    (Just (Node _ ns)) = Map.lookup n g
    in seenList ++ (concat $ map (neighbors g nseen) (Set.toList $ Set.difference ns seen))
  in neighbors g Set.empty n

main = do
  contents <- getContents
  putStr (show $ length $ nub $ connectedNodes (parseGraph $ lines contents) 0)
  putStr ("\n")
